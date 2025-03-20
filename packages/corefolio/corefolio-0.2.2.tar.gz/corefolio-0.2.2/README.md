# CoreFolio

<p align="center">
    <img src="https://github.com/SebastienEveno/corefolio/actions/workflows/python-package.yml/badge.svg?branch=master" />
    <a href="https://pypi.org/project/corefolio" alt="Python Versions">
        <img src="https://img.shields.io/pypi/pyversions/corefolio.svg?logo=python&logoColor=white" /></a>
    <a href="https://pypi.org/project/corefolio" alt="PyPi">
        <img src="https://img.shields.io/pypi/v/corefolio" /></a>
    <a href="https://pepy.tech/project/corefolio" alt="Downloads">
        <img src="https://pepy.tech/badge/corefolio" /></a>
</p>

`corefolio` is a Python package for optimizing asset selection using CVXPY. It allows users to define a universe of assets, apply constraints, and optimize the portfolio based on specified criteria.

## Installation

To install the package, use the following command:

```sh
pip install corefolio
```

## Requirements
- Python >= 3.10
- pandas
- cvxpy >= 1.6.2
- pytest

## Usage

```python
import pandas as pd
from corefolio.optimizer import Optimizer
from corefolio.universe import Universe
from corefolio.constraint import MaxAssetsConstraint, MeanConstraint

# Define your universe and constraints
data = pd.DataFrame(
    {
        "ID": [1, 2, 3, 4], 
        "value": [10, 20, 30, 40], 
        "other_value": [5, 5, 5, 5]
    }
)
universe = Universe(data)
constraints = [
    MaxAssetsConstraint(max_assets=2), 
    MeanConstraint(column_name="other_value", tolerance=0.01)
]

# Create an optimizer instance
optimizer = Optimizer(universe, constraints, sense="maximize", target_column="value")

# Optimize the portfolio
selected_assets = optimizer.optimize()

print("Selected assets:", selected_assets)
```

## License
This project is licensed under the MIT License.
