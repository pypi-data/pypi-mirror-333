# American Options ANN

> This is still a work in progress, all `v0.1.*` releases are testing releases.

This is a Python package for American Options Pricing using Artificial Neural Networks (ANN)
that assumes the option follows a GARCH process. The package will contain 3 stages of datasets
for 3 GARCH models:

1. HN-GARCH
2. Duan-NGARCH
3. GJR GARCH


## Project Structure
- `main.py`: Contains the main entry point for the program, and is in charge of running the Training and Testing of the ANN model.
- `model.py`: Contains the implementation of the ANN model used for pricing American Options.
- `dataset.py`: Contains parsing the CSV files and preparing the data for training and testing.
- `utils.py`: Contains utility functions for the package.


## Installation

```bash
pip install ao_ann
```

## Running Locally

This project uses the Python package manager `uv`, this can be installed using the following command:
```bash
$ git clone https://github.com/Mustafif/AO_ANN.git
$ cd AO_ANN
$ pip3 install uv # install uv
$ uv sync
$ uv run main.py # run the main.py file
```

## Todo

- Fix the moduleness by `__init__.py`
- Move all ann functions to `ann.py`
