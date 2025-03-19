import dataclasses
from abc import ABC, abstractmethod
from typing import Any, Self

import polars as pl

from ert.config.parameter_config import CustomDict
from ert.config.parsing import ConfigDict


class InvalidResponseFile(Exception):
    """
    Raised when an input file of the ResponseConfig has
    the incorrect format.
    """


@dataclasses.dataclass
class ResponseConfig(ABC):
    name: str
    input_files: list[str] = dataclasses.field(default_factory=list)
    keys: list[str] = dataclasses.field(default_factory=list)
    has_finalized_keys: bool = False

    @abstractmethod
    def read_from_file(self, run_path: str, iens: int, iter: int) -> pl.DataFrame:
        """Reads the data for the response from run_path.

        Raises:
            FileNotFoundError: when one of the input_files for the
                response is missing.
            InvalidResponseFile: when one of the input_files is
                invalid
        """

    def to_dict(self) -> dict[str, Any]:
        data = dataclasses.asdict(self, dict_factory=CustomDict)
        data["_ert_kind"] = self.__class__.__name__
        return data

    @property
    @abstractmethod
    def expected_input_files(self) -> list[str]:
        """Returns a list of filenames expected to be produced by the forward model"""

    @property
    @abstractmethod
    def response_type(self) -> str:
        """Label to identify what kind of response it is.
        Must not overlap with that of other response configs."""
        ...

    @property
    @abstractmethod
    def primary_key(self) -> list[str]:
        """Primary key of this response data.
        For example 'time' for summary and ['index','report_step'] for gen data"""

    @classmethod
    @abstractmethod
    def from_config_dict(cls, config_dict: ConfigDict) -> Self | None:
        """Creates a config, given an ert config dict.
        A response config may depend on several config kws, such as REFCASE
        for summary."""

    @classmethod
    def display_column(cls, value: Any, column_name: str) -> str:
        """Formats a value to a user-friendly displayable format."""
        return str(value)
