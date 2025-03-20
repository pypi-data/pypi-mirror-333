# mlogitviz

`mlogitviz` is a Python package designed to visualize changes in predicted probabilities from multinomial logistic regression models. It simplifies interpreting complex models, especially those involving Likert-scale predictors or other categorical data.

## Installation

To install `mlogitviz`, run:

```bash
pip install mlogitviz
```

## Usage

```python
import pandas as pd
from mlogitviz import visualize_mlogit

# Load your dataset
df = pd.read_csv("your_data.csv")

# Define key parameters
dependent_var = "outcome"  # Your categorical dependent variable
independent_vars = ["predictor1", "predictor2", "predictor3"]  # Independent variables
baseline_category = "Baseline_Outcome"

# Visualize with custom parameters
visualize_mlogit(df, dependent_var, independent_vars,
                  baseline=baseline_category,
                  significance=0.05,
                  margeff_at='overall',
                  margeff_count=False,
                  output_file="heatmap.png")
```

## Parameters
- **`df`** *(pd.DataFrame)*: Data containing the dependent and independent variables.
- **`dependent`** *(str)*: The name of the dependent variable (categorical).
- **`independent`** *(list of str)*: List of predictor variables (continuous or categorical).
- **`baseline`** *(str)*: Reference category for interpreting marginal effects.
- **`significance`** *(float, default=0.05)*: Threshold for displaying statistically significant effects.
- **`margeff_at`** *(str, default='overall')*: Controls how marginal effects are computed.
  - `'overall'`: Recommended for Likert scales or diverse data types.
  - `'mean'`: Uses the mean values of predictors for marginal effects.
- **`margeff_count`** *(bool, default=False)*: Treats count variables as continuous (`False`) or calculates changes when increased by one unit (`True`).
- **`output_file`** *(str or None)*: Path to save the visualization as an image file. If `None`, it will be displayed directly.

## Example Output
- The heatmap visualizes changes in probabilities, showing:
  - **Positive values** (red) = increased likelihood.
  - **Negative values** (blue) = decreased likelihood.
  - Baseline effects appear as a separate column with no significance indicators.

## Credits
This package was co-authored by Payam Saeedi and Eric Williams.


## License
This project is licensed under the MIT License.

## Citing this Package
If you use `mlogitviz` in your research, please cite:

**Payam Saeedi** and **Eric Williams**. *mlogitviz: Visualizing Marginal Effects in Multinomial Logistic Regression*. Version 0.1.4. URL: [https://pypi.org/project/mlogitviz/](https://pypi.org/project/mlogitviz/)

### BibTeX
```bibtex
@software{mlogitviz,
  author = {Payam Saeedi and Eric Williams},
  title = {mlogitviz: Visualizing Marginal Effects in Multinomial Logistic Regression},
  year = {2024},
  version = {0.1.4},
  url = {https://pypi.org/project/mlogitviz/}
}
```