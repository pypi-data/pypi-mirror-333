# American Options ANN

> Note: This package uses Torch under ROCM v6.2.4, if you are not using an AMD GPU, you will need to replace the torch dependency with a compatible version for your GPU.

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


This project uses the Python package manager `uv`, this can be installed using the following command:
```bash
$ pip3 install uv
```

> TODO: How to use `uv` and other information, first need to figure out the publishing process.

Refer to the [License](LICENSE) file for licensing information.
