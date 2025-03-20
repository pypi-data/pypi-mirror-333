import pandas as pd
import numpy as np
import statsmodels.api as sm
from .exceptions import DataValidationError

def fit_mlogit(df, dependent, independent, baseline, margeff_at='overall', margeff_count=True):
    """
    Fit a multinomial logistic regression model and compute the marginal effects for all categories.
    
    Parameters:
      - df: pandas DataFrame containing the data.
      - dependent: str, name of the dependent variable (should be categorical).
      - independent: list of str, names of the independent (numeric) variables.
      - baseline: str, the baseline category (must be one of the dependent variable's categories).
      - margeff_at: str, point at which marginal effects are evaluated. 
            Typical choices are 'overall' (default) or 'mean'.
      - margeff_count: bool, if True, the marginal effect is the change in probability for a one-unit increase.
            If False, predictors are treated as continuous (default in statsmodels).
    
    Returns:
      - model_fit: The fitted MNLogit model.
      - effects_df: DataFrame of marginal effects for each outcome category (excluding baseline).
      - se_effects_df: DataFrame of standard errors for the marginal effects (excluding baseline).
      - pval_df: DataFrame of regression p-values (excluding baseline).
    """
    
    # Ensure the dependent variable is categorical.
    if not pd.api.types.is_categorical_dtype(df[dependent]):
        df[dependent] = df[dependent].astype('category')
    
    if baseline not in df[dependent].cat.categories:
        raise DataValidationError(f"Baseline category '{baseline}' not found in dependent variable.")
    
    # Reorder so that the baseline is the first category.
    categories = list(df[dependent].cat.categories)
    if categories[0] != baseline:
        categories.remove(baseline)
        categories.insert(0, baseline)
        df[dependent] = df[dependent].cat.reorder_categories(categories, ordered=True)
    
    # Validate that all independent variables are numeric.
    for var in independent:
        if not pd.api.types.is_numeric_dtype(df[var]):
            raise DataValidationError(f"Independent variable '{var}' is not numeric.")
    
    # Prepare design matrix X and response y.
    X = df[independent]
    X = sm.add_constant(X)  # Adds constant column.
    y = df[dependent].cat.codes  # Baseline (first category) becomes 0.
    
    # Fit multinomial logistic regression.
    model = sm.MNLogit(y, X)
    model_fit = model.fit(disp=False)
    
    # Extract regression p-values (dropping the constant row) and assign non-baseline names.
    coef_pvalues = model_fit.pvalues.iloc[1:, :]
    non_baseline_labels = categories[1:]  # Original category names excluding baseline.
    coef_pvalues.columns = non_baseline_labels
    
    # Compute average marginal effects using user-specified settings.
    margeff_obj = model_fit.get_margeff(at=margeff_at, method='dydx', count=margeff_count)
    effects = margeff_obj.margeff   # Expected shape: (n_vars, n_outcomes)
    se_effects = margeff_obj.margeff_se
    
    # Sometimes the returned effects include the baseline column.
    # If so, drop the first column so that we only have non-baseline outcomes.
    if effects.shape[1] == len(categories):
        effects = effects[:, 1:]
        se_effects = se_effects[:, 1:]
    
    n_vars, n_outcomes = effects.shape
    # Ensure the list of labels matches the number of outcome columns.
    labels = non_baseline_labels[:n_outcomes]
    if len(labels) < n_outcomes:
        labels += [f"Outcome_{i}" for i in range(len(labels), n_outcomes)]
    
    # Map marginal effects to the correct outcome labels.
    effects_dict = {}
    se_effects_dict = {}
    for i, label in enumerate(labels):
        effects_dict[label] = effects[:, i]
        se_effects_dict[label] = se_effects[:, i]
    
    # Create DataFrames with the correct outcome names.
    effects_df = pd.DataFrame(effects_dict, index=[col for col in X.columns if col != 'const'])
    se_effects_df = pd.DataFrame(se_effects_dict, index=[col for col in X.columns if col != 'const'])
    
    return model_fit, effects_df, se_effects_df, coef_pvalues
