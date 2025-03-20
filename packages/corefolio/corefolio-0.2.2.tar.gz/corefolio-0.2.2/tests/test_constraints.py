"""Tests for the constraints module."""

import cvxpy as cp
import pandas as pd

from corefolio.constraint import MaxAssetsConstraint


def test_apply_max_assets_constraint():
    x = cp.Variable(3, boolean=True)
    constraint = MaxAssetsConstraint(max_assets=2)
    applied_constraints = constraint.apply_constraint(x, pd.DataFrame())[0]
    assert applied_constraints.args[1].value == 2


def test_max_assets_property():
    constraint = MaxAssetsConstraint(max_assets=5)
    assert constraint.max_assets == 5
