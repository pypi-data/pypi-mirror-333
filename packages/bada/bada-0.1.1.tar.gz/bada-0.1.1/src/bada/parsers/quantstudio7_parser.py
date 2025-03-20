import pandas as pd

from bada.models import DSFInput, QuantStudio7Raw
from bada.parsers.base_parser import BaseParser


class QuantStudio7Parser(BaseParser):
    def parse(self) -> pd.DataFrame:
        df = self._read_file()
        self._validate_raw_data(df)
        df = self._process_raw_data(df)
        self._validate_processed_data(df)

        return df

    def _read_file(self) -> pd.DataFrame:
        return pd.read_csv(self.file_path, skiprows=21)

    def _validate_raw_data(self, df: pd.DataFrame) -> None:
        QuantStudio7Raw.validate(df)

    def _process_raw_data(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.rename(
            columns={
                "Well Position": "well_position",
                "Temperature": "temperature",
                "Fluorescence": "fluorescence",
            }
        )

        df = df.loc[:, ["well_position", "temperature", "fluorescence"]]

        return df

    def _validate_processed_data(self, df: pd.DataFrame) -> None:
        DSFInput.validate(df)
