# mlogitviz

**mlogitviz** is a Python library for fitting multinomial logistic regression models and visualizing marginal effects as heatmaps. It is designed for ease of use, including clear options for evaluating marginal effects at different points (e.g., overall vs. mean) and treating predictors as count or continuous variables.

## Features

- **Model Fitting:**  
  Fit a multinomial logistic regression using `statsmodels` and compute marginal effects.
  
- **Visualization:**  
  Create heatmaps of probability changes relative to a baseline outcome, with options to annotate significance.

## Installation

You can install the library via pip once it’s published on PyPI:

```bash
pip install mlogitviz
