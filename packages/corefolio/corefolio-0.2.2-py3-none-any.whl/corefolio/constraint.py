"""This module contains the Constraints classes, which are used to apply constraints to the optimization problem."""

import cvxpy as cp
from typing import List
from abc import ABC, abstractmethod
import pandas as pd


class Constraint(ABC):
    @abstractmethod
    def apply_constraint(self, variables: List[cp.Variable], df: pd.DataFrame) -> List[cp.Constraint]:
        """
        Applies the constraint to the optimization problem.

        Args:
            variables (List[cp.Variable]): The decision variables.
            df (pd.DataFrame): The DataFrame containing asset data.

        Returns:
            List[cp.Constraint]: The list of constraints.
        """
        pass


class MaxAssetsConstraint(Constraint):
    def __init__(self, max_assets: int = 5) -> None:
        """
        Initializes the MaxAssetsConstraint with a maximum number of assets.

        Args:
            max_assets (int): The maximum number of assets to select.
        """
        self._max_assets = max_assets

    def apply_constraint(self, variables: List[cp.Variable], df: pd.DataFrame) -> List[cp.Constraint]:
        """
        Applies the constraint to the optimization problem.

        Args:
            variables (List[cp.Variable]): The decision variables.
            df (pd.DataFrame): The DataFrame containing asset data.

        Returns:
            List[cp.Constraint]: The list of constraints.
        """
        return [cp.sum(variables) <= self._max_assets]

    @property
    def max_assets(self) -> int:
        """
        Returns the maximum number of assets.

        Returns:
            int: The maximum number of assets.
        """
        return self._max_assets


class MeanConstraint(Constraint):
    def __init__(self, column_name: str, tolerance: float = 0.01) -> None:
        """
        Initializes the MeanConstraint with a column name and tolerance.

        Args:
            column_name (str): The column name to be used for the mean constraint.
            tolerance (float): The tolerance for the mean constraint.
        """
        self._column_name = column_name
        self._tolerance = tolerance

    def apply_constraint(self, variables: List[cp.Variable], df: pd.DataFrame) -> List[cp.Constraint]:
        """
        Applies the mean constraint to the optimization problem.

        Args:
            variables (List[cp.Variable]): The decision variables.
            df (pd.DataFrame): The DataFrame containing asset data.

        Returns:
            List[cp.Constraint]: The list of constraints.
        """
        mean_value = df[self._column_name].mean()
        column_values = df[self._column_name].values
        selected_sum = cp.sum(cp.multiply(variables, column_values))
        selected_count = cp.sum(variables)
        return [selected_sum >= selected_count * (mean_value - self._tolerance),
                selected_sum <= selected_count * (mean_value + self._tolerance)]

    @property
    def column_name(self) -> str:
        """
        Returns the column name for the mean constraint.

        Returns:
            str: The column name for the mean constraint.
        """
        return self._column_name

    @property
    def tolerance(self) -> float:
        """
        Returns the tolerance for the mean constraint.

        Returns:
            float: The tolerance for the mean constraint.
        """
        return self._tolerance
