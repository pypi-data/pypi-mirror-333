import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from .model import fit_mlogit

def visualize_mlogit(df, dependent, independent, baseline, significance=0.05, output_file=None, 
                     margeff_at='overall', margeff_count=True):
    """
    Fit a multinomial logistic regression and visualize probability changes relative to a baseline using a heatmap.
    
    Parameters:
      - df: pandas DataFrame.
      - dependent: str, name of the dependent (categorical) variable.
      - independent: list of str, names of independent (numeric) variables.
      - baseline: str, baseline category in the dependent variable.
      - significance: float, significance level (default 0.05).
      - output_file: str or None, if provided the heatmap will be saved to this file.
      - margeff_at: str, point at which marginal effects are evaluated (passed to fit_mlogit).
      - margeff_count: bool, passed to fit_mlogit.
    
    Returns:
      - fig: matplotlib Figure object.
    """
    # Fit the model and get the marginal effects and related tables.
    model_fit, diff_df, diff_se_df, diff_pval_df = fit_mlogit(
        df, dependent, independent, baseline, margeff_at=margeff_at, margeff_count=margeff_count
    )
    
    # Optionally drop the constant row if present.
    if 'const' in diff_df.index:
        diff_df = diff_df.drop(index='const')
        diff_pval_df = diff_pval_df.drop(index='const')
    
    # ---------------------------------------------
    # Compute and insert the baseline marginal effects.
    # For each predictor, the baseline marginal effect is the negative sum of non-baseline effects.
    baseline_label = f"{baseline}(baseline)"
    baseline_effect = - diff_df.sum(axis=1)
    
    # Concatenate the baseline column as the leftmost column.
    baseline_df = pd.DataFrame({baseline_label: baseline_effect}, index=diff_df.index)
    diff_df = pd.concat([baseline_df, diff_df], axis=1)
    
    # For p-values, create a corresponding baseline column with values set to 1.0.
    baseline_pvals = pd.Series(1.0, index=diff_pval_df.index, name=baseline_label)
    baseline_pval_df = pd.DataFrame({baseline_label: baseline_pvals})
    diff_pval_df = pd.concat([baseline_pval_df, diff_pval_df], axis=1)
    # ---------------------------------------------
    
    # Filter to keep only those independent variables that are significant for at least one outcome.
    significant_mask = diff_pval_df < significance
    keep = significant_mask.any(axis=1)
    diff_df_filtered = diff_df[keep]
    pval_df_filtered = diff_pval_df[keep]
    
    # Create annotations: format values to 2 decimals.
    # For non-baseline columns, append an asterisk if the p-value is below significance.
    annot = diff_df_filtered.copy().astype(str)
    for row in diff_df_filtered.index:
        for col in diff_df_filtered.columns:
            val = diff_df_filtered.loc[row, col]
            if col == baseline_label:
                annot.loc[row, col] = f"{val:.2f}"
            else:
                pval = pval_df_filtered.loc[row, col]
                annotation = f"{val:.2f}"
                if pval < significance:
                    annotation += "*"
                annot.loc[row, col] = annotation
    
    # Plot the heatmap.
    plt.figure(figsize=(10, max(6, 0.5 * len(diff_df_filtered))))
    ax = sns.heatmap(
        diff_df_filtered,
        annot=annot,
        fmt='',
        cmap="RdBu_r",
        center=0,
        cbar_kws={'label': 'Probability Change'}
    )
    plt.title("Probability Changes Relative to Baseline")
    plt.ylabel("Independent Variables")
    plt.xlabel("Outcome Categories")
    plt.tight_layout()
    
    # Save the figure if requested, otherwise show it.
    if output_file:
        plt.savefig(output_file, dpi = 300)
    fig = ax.get_figure()
    plt.show()
    return fig
