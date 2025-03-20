# deeplp

[![PyPI version](https://img.shields.io/pypi/v/deeplp.svg)](https://pypi.org/project/deeplp)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Build Status](https://github.com/yourusername/deeplp/actions/workflows/ci.yml/badge.svg)](https://github.com/yourusername/deeplp/actions)

**deeplp** is a Python package for solving linear programming problems using deep learning techniques. It leverages PyTorch for its backend computations and provides a simple API for defining problems and training models.

## Features

- Define linear programming problems with a simple API.
- Train deep learning models to solve LPs.
- Built-in support for plotting results and saving models.
- A command-line interface (CLI) for running experiments.
- Available on [PyPI](https://pypi.org/project/deeplp) for easy installation.

## Requirements

**deeplp** requires:
- Python 3.8+
- PyTorch (with GPU support if desired)

### Installing PyTorch

Visit the [PyTorch website](https://pytorch.org/get-started/locally/) for installation instructions. For example, to install PyTorch with CUDA 11.3 support on Windows:

```bash
pip install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu118
```

For CPU-only support, run:

```bash
pip install torch torchvision torchaudio
```

## Installation

You can install **deeplp** either from PyPI or directly from GitHub.

### Installing from PyPI

```bash
pip install deeplp
```

### Installing from GitHub

```bash
pip install git+https://github.com/yourusername/deeplp.git
```

If you're using Poetry for dependency management, add it to your `pyproject.toml` like so:

```toml
[tool.poetry.dependencies]
deeplp = "^0.1.0"  # or use the Git URL for the latest version
```

## Basic Usage

### Defining a Problem

Use the provided `createProblem` function to define your linear programming problem. For example:

```python
from deeplp import createProblem

# Define your problem data:
c = [1.0, 2.0]                # Objective coefficients
A = [
    [3, -5],
    [3, -1],
    [3,  1],
    [3,  4],
    [1,  3]
]                           # Constraint matrix
b = [15, 21, 27, 45, 30]      # Right-hand side values
tspan = (0.0, 10.0)           # Time span

# Create the problem (if no name is provided, a name is generated automatically)
problem = createProblem(c, A, b, tspan, name=None, test_points=None)
```

### Training a Model

The main training function has the following signature:

```python
model, loss_list, mov = train(
    batches=2,
    batch_size=256,
    epochs=500,
    problems_ids=[1, 2],
    cases=[1, 2],
    do_plot=True,
    saving_dir="my_saved_models"
)
```

### Running the CLI

After installing the package (which sets up a CLI entry point via Poetry), you can run:

```bash
deeplp --batches 1 --batch_size 128 --iterations 1000 --case 1 --example 1 --do_plot --folder saved_models
```

This command runs your CLI to start training with the specified options.
