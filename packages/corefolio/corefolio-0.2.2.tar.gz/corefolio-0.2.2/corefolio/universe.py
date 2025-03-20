"""This module contains the Universe class."""

import pandas as pd


class Universe:
    def __init__(self, df: pd.DataFrame, id_column: str = "ID") -> None:
        """
        Initializes the Universe with a DataFrame and an ID column.

        Args:
            df (pd.DataFrame): The DataFrame containing asset data.
            id_column (str): The column name to be used as the ID column.

        Raises:
            ValueError: If the DataFrame contains NaN values or duplicate IDs.
        """
        self._validate_dataframe(df, id_column)
        self._df = df
        self._id_column = id_column
        self._number_of_assets = df[id_column].nunique()

    def _validate_dataframe(self, df: pd.DataFrame, id_column: str) -> None:
        """
        Validates the DataFrame for NaN values and duplicate IDs.

        Args:
            df (pd.DataFrame): The DataFrame to validate.
            id_column (str): The column name to be used as the ID column.

        Raises:
            ValueError: If the DataFrame contains NaN values or duplicate IDs.
        """
        if df.isna().any().any():
            raise ValueError("DataFrame contains NaN values.")

        if id_column not in df.columns:
            df[id_column] = range(1, len(df) + 1)

        if df[id_column].duplicated().any():
            raise ValueError("DataFrame contains duplicate IDs.")

    @classmethod
    def from_dataframe(cls, df: pd.DataFrame, id_column: str = "ID") -> "Universe":
        """
        Creates a Universe instance from a DataFrame.

        Args:
            df (pd.DataFrame): The DataFrame containing asset data.
            id_column (str): The column name to be used as the ID column.

        Returns:
            Universe: A new Universe instance.
        """
        return cls(df, id_column)

    def to_dataframe(self) -> pd.DataFrame:
        """
        Returns the Universe data as a DataFrame while keeping it protected from modification.

        Returns:
            pd.DataFrame: A copy of the Universe data.
        """
        return self._df.copy()

    @property
    def df(self) -> pd.DataFrame:
        """
        Returns the Universe data as a DataFrame while keeping it protected from modification.

        Returns:
            pd.DataFrame: A copy of the Universe data.
        """
        return self.to_dataframe()

    @property
    def id_column(self) -> str:
        """
        Returns the ID column name.

        Returns:
            str: The ID column name.
        """
        return self._id_column

    @property
    def number_of_assets(self) -> int:
        """
        Returns the number of assets in the Universe.

        Returns:
            int: The number of unique assets.
        """
        return self._number_of_assets
