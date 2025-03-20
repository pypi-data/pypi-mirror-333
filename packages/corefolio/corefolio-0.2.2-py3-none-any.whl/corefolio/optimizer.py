"""This module contains the Optimizer class, which is responsible for optimizing the portfolio."""

import cvxpy as cp
import pandas as pd
from typing import List

from corefolio.constraint import Constraint
from corefolio.universe import Universe


class Optimizer:
    def __init__(self, universe: Universe, constraints: List[Constraint], sense: str = "maximize", target_column: str = "value") -> None:
        """
        Initializes the Optimizer with a Universe, Constraints, optimization sense, and target column.

        Args:
            universe (Universe): The Universe containing asset data.
            constraints (List[Constraint]): The list of Constraints to apply during optimization.
            sense (str): The optimization sense, either 'maximize' or 'minimize'.
            target_column (str): The column name to be used for the optimization target.

        Raises:
            ValueError: If the sense is not 'maximize' or 'minimize'.
        """
        self.universe = universe
        self.constraints = constraints
        self.sense = self._parse_sense(sense)
        self.target_column = target_column

    def _parse_sense(self, sense: str) -> int:
        """
        Parses the optimization sense.

        Args:
            sense (str): The optimization sense, either 'maximize' or 'minimize'.

        Returns:
            int: The parsed sense as 1 for 'maximize' and -1 for 'minimize'.

        Raises:
            ValueError: If the sense is not 'maximize' or 'minimize'.
        """
        sense_map = {"maximize": 1, "minimize": -1}
        if sense not in sense_map:
            raise ValueError(
                "Invalid sense value. Choose 'maximize' or 'minimize'.")
        return sense_map[sense]

    def _create_decision_variables(self, num_assets: int) -> cp.Variable:
        """
        Creates decision variables for the optimization problem.

        Args:
            num_assets (int): The number of assets.

        Returns:
            cp.Variable: The decision variables.
        """
        return cp.Variable(num_assets, boolean=True)

    def _create_objective(self, values: pd.Series, x: cp.Variable) -> cp.Maximize:
        """
        Creates the objective function for the optimization problem.

        Args:
            values (pd.Series): The asset values.
            x (cp.Variable): The decision variables.

        Returns:
            cp.Maximize: The objective function.
        """
        return cp.Maximize(self.sense * values @ x)

    def optimize(self) -> List[int]:
        """
        Optimizes the portfolio based on the given Universe and Constraints.

        Returns:
            List[int]: The list of selected asset IDs.
        """
        df = self.universe.to_dataframe()
        ids = df[self.universe.id_column].tolist()
        values = df[self.target_column].values

        # Define decision variables
        x = self._create_decision_variables(len(ids))

        # Define objective
        objective = self._create_objective(values, x)

        # Define constraints
        constraints = []
        for constraint in self.constraints:
            constraints.extend(constraint.apply_constraint(x, df))

        # Solve problem
        problem = cp.Problem(objective, constraints)
        problem.solve()

        # Get results
        if problem.status in ["infeasible", "infeasible_inaccurate"]:
            return []

        selected_ids = [ids[i] for i in range(len(ids)) if x.value[i] > 0.5]

        return selected_ids
