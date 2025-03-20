"""Tests for the Universe class."""

import pytest
import pandas as pd

from corefolio.universe import Universe


def test_universe_initialization():
    data = pd.DataFrame({"ID": [1, 2, 3], "value": [10, 20, 30]})
    universe = Universe(data)
    assert universe.number_of_assets == 3


def test_universe_nan_values():
    data = pd.DataFrame({"ID": [1, 2, None], "value": [10, 20, 30]})
    with pytest.raises(Exception, match="DataFrame contains NaN values."):
        Universe(data)


def test_universe_duplicate_ids():
    data = pd.DataFrame({"ID": [1, 2, 2], "value": [10, 20, 30]})
    with pytest.raises(Exception, match="DataFrame contains duplicate IDs."):
        Universe(data)


def test_universe_from_dataframe():
    data = pd.DataFrame({"ID": [1, 2, 3], "value": [10, 20, 30]})
    universe = Universe.from_dataframe(data)
    assert universe.to_dataframe().equals(data)


def test_universe_custom_id_column():
    data = pd.DataFrame({"Asset_ID": [1, 2, 3], "value": [10, 20, 30]})
    universe = Universe.from_dataframe(data, id_column="Asset_ID")
    assert universe.number_of_assets == 3


def test_universe_create_id_column():
    data = pd.DataFrame({"value": [10, 20, 30]})
    universe = Universe(data)
    assert "ID" in universe.to_dataframe().columns
    assert universe.to_dataframe()["ID"].tolist() == [1, 2, 3]
    assert universe.number_of_assets == 3


def test_universe_id_column_property():
    data = pd.DataFrame({"ID": [1, 2, 3], "value": [10, 20, 30]})
    universe = Universe(data)
    assert universe.id_column == "ID"


def test_universe_number_of_assets_property():
    data = pd.DataFrame({"ID": [1, 2, 3], "value": [10, 20, 30]})
    universe = Universe(data)
    assert universe.number_of_assets == 3


def test_universe_df_property():
    data = pd.DataFrame({"ID": [1, 2, 3], "value": [10, 20, 30]})
    universe = Universe(data)
    df_copy = universe.df
    assert df_copy.equals(data)
    # Ensure the returned DataFrame is a copy and not the original
    df_copy["value"] = [100, 200, 300]
    assert not df_copy.equals(universe.df)
