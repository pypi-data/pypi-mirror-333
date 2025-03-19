from __future__ import annotations

import contextlib
import logging
import os
from collections.abc import Iterable
from datetime import datetime
from functools import cache, lru_cache
from pathlib import Path
from typing import TYPE_CHECKING
from uuid import UUID

import numpy as np
import pandas as pd
import xarray as xr
from pydantic import BaseModel
from typing_extensions import deprecated

from ert.config.gen_kw_config import GenKwConfig
from ert.storage.mode import BaseMode, Mode, require_write

from .realization_storage_state import RealizationStorageState

if TYPE_CHECKING:
    import numpy.typing as npt

    from ert.storage.local_experiment import LocalExperiment
    from ert.storage.local_storage import LocalStorage

logger = logging.getLogger(__name__)

import polars as pl


class _Index(BaseModel):
    id: UUID
    experiment_id: UUID
    ensemble_size: int
    iteration: int
    name: str
    prior_ensemble_id: UUID | None
    started_at: datetime


class _Failure(BaseModel):
    type: RealizationStorageState
    message: str
    time: datetime


def _escape_filename(filename: str) -> str:
    return filename.replace("%", "%25").replace("/", "%2F")


class LocalEnsemble(BaseMode):
    """
    Represents an ensemble within the local storage system of ERT.

    Manages multiple realizations of experiments, including different sets of
    parameters and responses.
    """

    def __init__(
        self,
        storage: LocalStorage,
        path: Path,
        mode: Mode,
    ):
        """
        Initialize a LocalEnsemble instance.

        Parameters
        ----------
        storage : LocalStorage
            Local storage instance.
        path : Path
            File system path to ensemble data.
        mode : Mode
            Access mode for the ensemble (read/write).
        """

        super().__init__(mode)
        self._storage = storage
        self._path = path
        self._index = _Index.model_validate_json(
            (path / "index.json").read_text(encoding="utf-8")
        )
        self._error_log_name = "error.json"

        @cache
        def create_realization_dir(realization: int) -> Path:
            return self._path / f"realization-{realization}"

        self._realization_dir = create_realization_dir

    @classmethod
    def create(
        cls,
        storage: LocalStorage,
        path: Path,
        uuid: UUID,
        *,
        ensemble_size: int,
        experiment_id: UUID,
        iteration: int = 0,
        name: str,
        prior_ensemble_id: UUID | None,
    ) -> LocalEnsemble:
        """
        Create a new ensemble in local storage.

        Parameters
        ----------
        storage : LocalStorage
            Local storage instance.
        path : Path
            File system path for ensemble data.
        uuid : UUID
            Unique identifier for the new ensemble.
        ensemble_size : int
            Number of realizations.
        experiment_id : UUID
            Identifier of associated experiment.
        iteration : int
            Iteration number of ensemble.
        name : str
            Name of ensemble.
        prior_ensemble_id : UUID, optional
            Identifier of prior ensemble.

        Returns
        -------
        local_ensemble : LocalEnsemble
            Instance of the newly created ensemble.
        """

        (path / "experiment").mkdir(parents=True, exist_ok=False)

        index = _Index(
            id=uuid,
            ensemble_size=ensemble_size,
            experiment_id=experiment_id,
            iteration=iteration,
            name=name,
            prior_ensemble_id=prior_ensemble_id,
            started_at=datetime.now(),
        )

        storage._write_transaction(
            path / "index.json", index.model_dump_json(indent=2).encode("utf-8")
        )

        return cls(storage, path, Mode.WRITE)

    @property
    def mount_point(self) -> Path:
        return self._path

    @property
    def name(self) -> str:
        return self._index.name

    @property
    def id(self) -> UUID:
        return self._index.id

    @property
    def experiment_id(self) -> UUID:
        return self._index.experiment_id

    @property
    def ensemble_size(self) -> int:
        return self._index.ensemble_size

    @property
    def started_at(self) -> datetime:
        return self._index.started_at

    @property
    def iteration(self) -> int:
        return self._index.iteration

    @property
    def parent(self) -> UUID | None:
        return self._index.prior_ensemble_id

    @property
    def experiment(self) -> LocalExperiment:
        return self._storage.get_experiment(self.experiment_id)

    @property
    def relative_weights(self) -> str:
        return self._storage.get_experiment(self.experiment_id).relative_weights

    def get_realization_mask_without_failure(self) -> npt.NDArray[np.bool_]:
        """
        Mask array indicating realizations without any failure.

        Returns
        -------
        failures : ndarray of bool
            Boolean array where True means no failure.
        """

        return np.array(
            [
                not {
                    RealizationStorageState.PARENT_FAILURE,
                    RealizationStorageState.LOAD_FAILURE,
                }.intersection(e)
                for e in self.get_ensemble_state()
            ]
        )

    def get_realization_mask_with_parameters(self) -> npt.NDArray[np.bool_]:
        """
        Mask array indicating realizations with associated parameters.

        Returns
        -------
        parameters : ndarray of bool
            Boolean array where True means parameters are associated.
        """

        return np.array(
            [
                bool(
                    {
                        RealizationStorageState.PARAMETERS_LOADED,
                        RealizationStorageState.RESPONSES_LOADED,
                    }.intersection(state)
                )
                for state in self.get_ensemble_state()
            ]
        )

    def get_realization_mask_with_responses(self) -> npt.NDArray[np.bool_]:
        """
        Mask array indicating realizations with associated responses.

        Parameters
        ----------
        key : str, optional
            Response key to filter realizations. If None, all responses are considered.

        Returns
        -------
        masks : ndarray of bool
            Boolean array where True means responses are associated.
        """

        return np.array(
            [
                RealizationStorageState.RESPONSES_LOADED in state
                for state in self.get_ensemble_state()
            ]
        )

    def is_initalized(self) -> list[int]:
        """
        Return the realization numbers where all parameters are internalized. In
        cases where there are parameters which are read from the forward model, an
        ensemble is considered initialized if all other parameters are present

        Returns
        -------
        exists : list[int]
            Returns the realization numbers with parameters
        """

        return [
            i
            for i in range(self.ensemble_size)
            if all(
                (
                    self._realization_dir(i)
                    / (_escape_filename(parameter.name) + ".nc")
                ).exists()
                for parameter in self.experiment.parameter_configuration.values()
                if not parameter.forward_init
            )
        ]

    def has_data(self) -> list[int]:
        """
        Return the realization numbers where all responses are internalized

        Returns
        -------
        exists : list[int]
            Returns the realization numbers with responses
        """

        ensemble_state = self.get_ensemble_state()
        return [
            i
            for i in range(self.ensemble_size)
            if RealizationStorageState.RESPONSES_LOADED in ensemble_state[i]
        ]

    def get_realization_list_with_responses(self) -> list[int]:
        """
        list of realization indices with associated responses.

        Parameters
        ----------
        key : str, optional
            Response key to filter realizations. If None, all responses are considered.

        Returns
        -------
        realizations : list of int
            list of realization indices with associated responses.
        """

        mask = self.get_realization_mask_with_responses()
        return np.where(mask)[0].tolist()

    def set_failure(
        self,
        realization: int,
        failure_type: RealizationStorageState,
        message: str | None = None,
    ) -> None:
        """
        Record a failure for a given realization in ensemble.

        Parameters
        ----------
        realization : int
            Index of realization.
        failure_type : RealizationStorageState
            Type of failure.
        message : str, optional
            Optional message describing the failure.
        """

        filename: Path = self._realization_dir(realization) / self._error_log_name
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        error = _Failure(
            type=failure_type, message=message if message else "", time=datetime.now()
        )
        self._storage._write_transaction(
            filename, error.model_dump_json(indent=2).encode("utf-8")
        )

    def unset_failure(
        self,
        realization: int,
    ) -> None:
        filename: Path = self._realization_dir(realization) / self._error_log_name
        if filename.exists():
            filename.unlink()

    def has_failure(self, realization: int) -> bool:
        """
        Check if given realization has a recorded failure.

        Parameters
        ----------
        realization : int
            Index of realization.

        Returns
        -------
        has_failure : bool
            True if realization has a recorded failure.
        """

        return (self._realization_dir(realization) / self._error_log_name).exists()

    def get_failure(self, realization: int) -> _Failure | None:
        """
        Retrieve failure information for a given realization, if any.

        Parameters
        ----------
        realization : int
            Index of realization.

        Returns
        -------
        failure : _Failure, optional
            Failure information if recorded, otherwise None.
        """

        if self.has_failure(realization):
            return _Failure.model_validate_json(
                (self._realization_dir(realization) / self._error_log_name).read_text(
                    encoding="utf-8"
                )
            )
        return None

    def refresh_ensemble_state(self) -> None:
        self.get_ensemble_state.cache_clear()
        self.get_ensemble_state()

    @lru_cache  # noqa: B019
    def get_ensemble_state(self) -> list[set[RealizationStorageState]]:
        """
        Retrieve the state of each realization within ensemble.

        Returns
        -------
        states : list of RealizationStorageState
            list of realization states.
        """

        response_configs = self.experiment.response_configuration

        def _parameters_exist_for_realization(realization: int) -> bool:
            """
            Returns true if all parameters in the experiment have
            all been saved in the ensemble. If no parameters, return True

            Parameters
            ----------
            realization : int
                Realization index.

            Returns
            -------
            exists : bool
                True if parameters exist for realization.
            """
            if not self.experiment.parameter_configuration:
                return True
            path = self._realization_dir(realization)
            return all(
                (path / (_escape_filename(parameter) + ".nc")).exists()
                for parameter in self.experiment.parameter_configuration
            )

        def _responses_exist_for_realization(
            realization: int, key: str | None = None
        ) -> bool:
            """
            Returns true if there are responses in the experiment and they have
            all been saved in the ensemble

            Parameters
            ----------
            realization : int
                Realization index.
            key : str, optional
                Response key to filter realizations. If None, all responses are considered.

            Returns
            -------
            exists : bool
                True if responses exist for realization.
            """

            if not response_configs:
                return True
            path = self._realization_dir(realization)

            def _has_response(key_: str) -> bool:
                if key_ in self.experiment.response_key_to_response_type:
                    response_type = self.experiment.response_key_to_response_type[key_]
                    return (path / f"{response_type}.parquet").exists()

                return (path / f"{key_}.parquet").exists()

            if key:
                return _has_response(key)

            is_expecting_any_responses = any(
                bool(config.keys) for config in response_configs.values()
            )

            if not is_expecting_any_responses:
                return True

            non_empty_response_configs = [
                response
                for response, config in response_configs.items()
                if bool(config.keys)
            ]

            return all(
                _has_response(response) for response in non_empty_response_configs
            )

        def _find_state(realization: int) -> set[RealizationStorageState]:
            state = set()
            if self.has_failure(realization):
                failure = self.get_failure(realization)
                assert failure
                state.add(failure.type)
            if _responses_exist_for_realization(realization):
                state.add(RealizationStorageState.RESPONSES_LOADED)
            if _parameters_exist_for_realization(realization):
                state.add(RealizationStorageState.PARAMETERS_LOADED)

            if len(state) == 0:
                state.add(RealizationStorageState.UNDEFINED)

            return state

        return [_find_state(i) for i in range(self.ensemble_size)]

    def _load_single_dataset(
        self,
        group: str,
        realization: int,
    ) -> xr.Dataset:
        try:
            return xr.open_dataset(
                self.mount_point
                / f"realization-{realization}"
                / f"{_escape_filename(group)}.nc",
                engine="scipy",
            )
        except FileNotFoundError as e:
            raise KeyError(
                f"No dataset '{group}' in storage for realization {realization}"
            ) from e

    def _load_dataset(
        self,
        group: str,
        realizations: int | np.int64 | npt.NDArray[np.int_] | None,
    ) -> xr.Dataset:
        if isinstance(realizations, int | np.int64):
            return self._load_single_dataset(group, int(realizations)).isel(
                realizations=0, drop=True
            )

        if realizations is None:
            datasets = [
                xr.open_dataset(p, engine="scipy")
                for p in sorted(
                    self.mount_point.glob(f"realization-*/{_escape_filename(group)}.nc")
                )
            ]
        else:
            datasets = [self._load_single_dataset(group, i) for i in realizations]
        return xr.combine_nested(datasets, concat_dim="realizations")

    def load_parameters(
        self, group: str, realizations: int | npt.NDArray[np.int_] | None = None
    ) -> xr.Dataset:
        """
        Load parameters for group and realizations into xarray Dataset.

        Parameters
        ----------
        group : str
            Name of parameter group to load.
        realizations : {int, ndarray of int}, optional
            Realization indices to load. If None, all realizations are loaded.

        Returns
        -------
        parameters : Dataset
            Loaded xarray Dataset with parameters.
        """

        return self._load_dataset(group, realizations)

    def load_cross_correlations(self) -> xr.Dataset:
        input_path = self.mount_point / "corr_XY.nc"

        if not input_path.exists():
            raise FileNotFoundError(
                f"No cross-correlation data available at '{input_path}'. Make sure to run the update with "
                "Adaptive Localization enabled."
            )
        logger.info("Loading cross correlations")
        return xr.open_dataset(input_path, engine="scipy")

    @require_write
    def save_observation_scaling_factors(self, dataset: pl.DataFrame) -> None:
        self._storage._to_parquet_transaction(
            self.mount_point / "observation_scaling_factors.parquet", dataset
        )

    def load_observation_scaling_factors(
        self,
    ) -> pl.DataFrame | None:
        ds_path = self.mount_point / "observation_scaling_factors.parquet"
        if ds_path.exists():
            return pl.read_parquet(ds_path)

        return None

    @require_write
    def save_cross_correlations(
        self,
        cross_correlations: npt.NDArray[np.float64],
        param_group: str,
        parameter_names: list[str],
    ) -> None:
        data_vars = {
            param_group: xr.DataArray(
                data=cross_correlations,
                dims=["parameter", "response"],
                coords={"parameter": parameter_names},
            )
        }
        dataset = xr.Dataset(data_vars)
        file_path = os.path.join(self.mount_point, "corr_XY.nc")
        self._storage._to_netcdf_transaction(file_path, dataset)

    def load_responses(self, key: str, realizations: tuple[int, ...]) -> pl.DataFrame:
        """Load responses for key and realizations into xarray Dataset.

        For each given realization, response data is loaded from the NetCDF
        file whose filename matches the given key parameter.

        Parameters
        ----------
        key : str
            Response key to load.
        realizations : tuple of int
            Realization indices to load.

        Returns
        -------
        responses : DataFrame
            Loaded polars DataFrame with responses.
        """

        return self._load_responses_lazy(key, realizations).collect()

    def _load_responses_lazy(
        self, key: str, realizations: tuple[int, ...]
    ) -> pl.LazyFrame:
        """Load responses for key and realizations into xarray Dataset.

        For each given realization, response data is loaded from the NetCDF
        file whose filename matches the given key parameter.

        Parameters
        ----------
        key : str
            Response key to load.
        realizations : tuple of int
            Realization indices to load.

        Returns
        -------
        responses : DataFrame
            Loaded polars DataFrame with responses.
        """

        select_key = False
        if key in self.experiment.response_configuration:
            response_type = key
        elif key not in self.experiment.response_key_to_response_type:
            raise ValueError(f"{key} is not a response")
        else:
            response_type = self.experiment.response_key_to_response_type[key]
            select_key = True

        loaded = []
        for realization in realizations:
            input_path = self._realization_dir(realization) / f"{response_type}.parquet"
            if not input_path.exists():
                raise KeyError(f"No response for key {key}, realization: {realization}")
            df = pl.scan_parquet(input_path)

            if select_key:
                df = df.filter(pl.col("response_key") == key)

            loaded.append(df)

        return pl.concat(loaded) if loaded else pl.DataFrame().lazy()

    @deprecated("Use load_responses")
    def load_all_summary_data(
        self,
        keys: list[str] | None = None,
        realization_index: int | None = None,
    ) -> pd.DataFrame:
        """
        Load all summary data for realizations into pandas DataFrame.

        Parameters
        ----------
        keys : list of str, optional
            list of keys to load. If None, all keys are loaded.
        realization_index : int, optional

        Returns
        -------
        summary_data : DataFrame
            Loaded pandas DataFrame with summary data.
        """

        realizations = self.get_realization_list_with_responses()
        if realization_index is not None:
            if realization_index not in realizations:
                raise IndexError(f"No such realization {realization_index}")
            realizations = [realization_index]

        try:
            df_pl = self.load_responses("summary", tuple(realizations))

        except (ValueError, KeyError):
            return pd.DataFrame()
        df_pl = df_pl.pivot(
            on="response_key", index=["realization", "time"], sort_columns=True
        )
        df_pl = df_pl.rename({"time": "Date", "realization": "Realization"})

        df_pandas = (
            df_pl.to_pandas()
            .set_index(["Realization", "Date"])
            .sort_values(by=["Date", "Realization"])
        )

        if keys:
            summary_keys = self.experiment.response_type_to_response_keys["summary"]
            summary_keys = sorted(
                [key for key in keys if key in summary_keys]
            )  # ignore keys that doesn't exist
            return df_pandas[summary_keys]

        return df_pandas

    def load_all_gen_kw_data(
        self,
        group: str | None = None,
        realization_index: int | None = None,
    ) -> pd.DataFrame:
        """Loads scalar parameters (GEN_KWs) into a pandas DataFrame
        with columns <PARAMETER_GROUP>:<PARAMETER_NAME> and
        "Realization" as index.

        Parameters
        ----------
        group : str, optional
            Name of parameter group to load.
        relization_index : int, optional
            The realization to load.

        Returns
        -------
        data : DataFrame
            A pandas DataFrame containing the GEN_KW data.

        Notes
        -----
        Any provided keys that are not gen_kw will be ignored.
        """
        if realization_index is not None:
            realizations = np.array([realization_index])
        else:
            ens_mask = (
                self.get_realization_mask_with_responses()
                + self.get_realization_mask_with_parameters()
            )
            realizations = np.flatnonzero(ens_mask)

        dataframes = []
        gen_kws = [
            config
            for config in self.experiment.parameter_configuration.values()
            if isinstance(config, GenKwConfig)
        ]
        if group:
            gen_kws = [config for config in gen_kws if config.name == group]
        for key in gen_kws:
            with contextlib.suppress(KeyError):
                da = self.load_parameters(key.name, realizations)["transformed_values"]
                assert isinstance(da, xr.DataArray)
                da["names"] = np.char.add(f"{key.name}:", da["names"].astype(np.str_))
                df = da.to_dataframe().unstack(level="names")
                df.columns = df.columns.droplevel()
                for parameter in df.columns:
                    if key.shouldUseLogScale(parameter.split(":")[1]):
                        df[f"LOG10_{parameter}"] = np.log10(df[parameter])
                dataframes.append(df)
        if not dataframes:
            return pd.DataFrame()

        dataframe = pd.concat(dataframes, axis=1)
        dataframe.columns.name = None
        dataframe.index.name = "Realization"

        return dataframe.sort_index(axis=1)

    @require_write
    def save_parameters(
        self,
        group: str,
        realization: int,
        dataset: xr.Dataset,
    ) -> None:
        """
        Saves the provided dataset under a parameter group and realization index(es)
        Parameters
        ----------
        group : str
            Parameter group name for saving dataset.
        realization : int or NDArray[int_]
            Realization index(es) for saving group.
        dataset : Dataset
            Dataset to save. It must contain a variable named 'values'
            which will be used when flattening out the parameters into
            a 1d-vector. When saving multiple realizations, dataset must
            have a 'realizations' dimension.
        """
        if "values" not in dataset.variables:
            raise ValueError(
                f"Dataset for parameter group '{group}' must contain a 'values' variable"
            )
        if dataset["values"].size == 0:
            raise ValueError(
                f"Parameters {group} are empty. Cannot proceed with saving to storage."
            )
        if group not in self.experiment.parameter_configuration:
            raise ValueError(f"{group} is not registered to the experiment.")

        path = self._realization_dir(realization) / f"{_escape_filename(group)}.nc"
        path.parent.mkdir(exist_ok=True)
        if "realizations" in dataset.dims:
            data_to_save = dataset.sel(realizations=[realization])
        else:
            data_to_save = dataset.expand_dims(realizations=[realization])
        self._storage._to_netcdf_transaction(path, data_to_save)

    @require_write
    def save_response(
        self, response_type: str, data: pl.DataFrame, realization: int
    ) -> None:
        """
        Save dataset as response under group and realization index.

        Parameters
        ----------
        response_type : str
            A name for the type of response stored, e.g., "summary, or "gen_data".
        realization : int
            Realization index for saving group.
        data : polars DataFrame
            polars DataFrame to save.
        """

        if "values" not in data.columns:
            raise ValueError(
                f"Dataset for response group '{response_type}' "
                f"must contain a 'values' variable"
            )

        if len(data) == 0:
            raise ValueError(
                f"Responses {response_type} are empty. Cannot proceed with saving to storage."
            )

        if "realization" not in data.columns:
            data.insert_column(
                0,
                pl.Series(
                    "realization", np.full(len(data), realization), dtype=pl.UInt16
                ),
            )

        output_path = self._realization_dir(realization)
        Path.mkdir(output_path, parents=True, exist_ok=True)

        self._storage._to_parquet_transaction(
            output_path / f"{response_type}.parquet", data
        )

        if not self.experiment._has_finalized_response_keys(response_type):
            response_keys = data["response_key"].unique().to_list()
            self.experiment._update_response_keys(response_type, response_keys)

    def calculate_std_dev_for_parameter(self, parameter_group: str) -> xr.Dataset:
        if parameter_group not in self.experiment.parameter_configuration:
            raise ValueError(f"{parameter_group} is not registered to the experiment.")

        ds = self.load_parameters(parameter_group)
        return ds.std("realizations")

    def get_parameter_state(
        self, realization: int
    ) -> dict[str, RealizationStorageState]:
        path = self._realization_dir(realization)
        return {
            e: RealizationStorageState.PARAMETERS_LOADED
            if (path / (_escape_filename(e) + ".nc")).exists()
            else RealizationStorageState.UNDEFINED
            for e in self.experiment.parameter_configuration
        }

    def get_response_state(
        self, realization: int
    ) -> dict[str, RealizationStorageState]:
        response_configs = self.experiment.response_configuration
        path = self._realization_dir(realization)
        return {
            e: RealizationStorageState.RESPONSES_LOADED
            if (path / f"{e}.parquet").exists()
            else RealizationStorageState.UNDEFINED
            for e in response_configs
        }

    def get_observations_and_responses(
        self,
        selected_observations: Iterable[str],
        iens_active_index: npt.NDArray[np.int_],
    ) -> pl.DataFrame:
        """Fetches and aligns selected observations with their corresponding simulated responses from an ensemble."""
        observations_by_type = self.experiment.observations

        with pl.StringCache():
            dfs_per_response_type = []
            for (
                response_type,
                response_cls,
            ) in self.experiment.response_configuration.items():
                if response_type not in observations_by_type:
                    continue

                observations_for_type = (
                    observations_by_type[response_type]
                    .filter(
                        pl.col("observation_key").is_in(list(selected_observations))
                    )
                    .with_columns(
                        [
                            pl.col("response_key")
                            .cast(pl.Categorical)
                            .alias("response_key")
                        ]
                    )
                )

                observed_cols = {
                    k: observations_for_type[k].unique()
                    for k in ["response_key", *response_cls.primary_key]
                }

                reals = iens_active_index.tolist()
                reals.sort()
                # too much memory to do it all at once, go per realization
                first_columns: pl.DataFrame | None = None
                realization_columns: list[pl.DataFrame] = []
                for real in reals:
                    responses = self._load_responses_lazy(
                        response_type, (real,)
                    ).with_columns(
                        [
                            pl.col("response_key")
                            .cast(pl.Categorical)
                            .alias("response_key")
                        ]
                    )

                    # Filter out responses without observations
                    for col, observed_values in observed_cols.items():
                        if col != "time":
                            responses = responses.filter(
                                pl.col(col).is_in(observed_values)
                            )

                    pivoted = responses.collect().pivot(
                        on="realization",
                        index=["response_key", *response_cls.primary_key],
                        values="values",
                        aggregate_function="mean",
                    )

                    if pivoted.is_empty():
                        # There are no responses for this realization,
                        # so we explicitly create a column of nans
                        # to represent this. We are basically saying that
                        # for this realization, each observation points
                        # to a NaN response.
                        joined = observations_for_type.with_columns(
                            pl.Series(
                                str(real),
                                [np.nan] * len(observations_for_type),
                                dtype=pl.Float32,
                            )
                        )
                    elif "time" in pivoted:
                        joined = observations_for_type.join_asof(
                            pivoted,
                            by=[
                                "response_key",
                                *[k for k in response_cls.primary_key if k != "time"],
                            ],
                            on="time",
                            strategy="nearest",
                            tolerance="1s",
                        )
                    else:
                        joined = observations_for_type.join(
                            pivoted,
                            how="left",
                            on=["response_key", *response_cls.primary_key],
                        )

                    joined = (
                        joined.with_columns(
                            pl.concat_str(
                                response_cls.primary_key, separator=", "
                            ).alias(
                                "__tmp_index_key__"
                                # Avoid potential collisions w/ primary key
                            )
                        )
                        .drop(response_cls.primary_key)
                        .rename({"__tmp_index_key__": "index"})
                    )

                    if first_columns is None:
                        # The "leftmost" index columns are not yet collected.
                        # They are the same for all iterations, and indexed the same
                        # because we do a left join for the observations.
                        # Hence, we select these columns only once.
                        first_columns = joined.select(
                            [
                                "response_key",
                                "index",
                                "observation_key",
                                "observations",
                                "std",
                            ]
                        )

                    realization_columns.append(joined.select(str(real)))

                if first_columns is None:
                    # Not a single realization had any responses to the
                    # observations. Hence, there is no need to include
                    # it in the dataset
                    continue

                dfs_per_response_type.append(
                    pl.concat([first_columns, *realization_columns], how="horizontal")
                )

            return pl.concat(dfs_per_response_type, how="vertical").with_columns(
                pl.col("response_key").cast(pl.String).alias("response_key")
            )
