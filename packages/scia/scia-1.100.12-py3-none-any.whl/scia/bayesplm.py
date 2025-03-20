import pandas as pd
import numpy as np
import pymc as pm
import bambi as bmb
import arviz as az
from scia.preprocess import prepare_scd
from scia.utils import revise_names

def create_fixed_formula(dvar, mvar, slope, level, trend, var_phase, var_inter, intercept=True):
    parameters = ["1"] if intercept else []
    if trend:
        parameters.append(mvar)
    if level:
        parameters.append(var_phase)
    if slope:
        parameters.append(var_inter)
    return f"{dvar} ~ {' + '.join(parameters)}"

def create_random_formula(mvar, slope, level, trend, var_phase, var_inter):
    parameters = []
    if trend:
        parameters.append(mvar)
    if level:
        parameters.append(var_phase)
    if slope:
        parameters.append(var_inter)
    return f"({' + '.join(parameters)} | case)" if parameters else None

def ensure_log_likelihood(idata, model):
    """
    Ensure log_likelihood exists in the inference data.
    """
    if "log_likelihood" not in idata.groups():
        with model.backend.model:
            log_likelihood = pm.compute_log_likelihood(idata)
        try:
            idata.add_groups(log_likelihood=log_likelihood)
        except ValueError as e:
            # If already exists, skip
            print("log_likelihood group already exists; skipping addition.")
    return idata

def bayesplm(data, dvar="values", pvar="phase", mvar="mt", 
             model="W", contrast_level="first", contrast_slope="first",
             trend=True, level=True, slope=True,
             random_trend=False, random_level=False, random_slope=False,
             fixed=None, random=None, update_fixed=None, samples=1000):
    """
    Bayesian Piecewise Linear Model using MCMC.

    Returns:
      A formatted string summary.
    """
    # Prepare data and extract case names
    data = prepare_scd(data)
    case_names = data["case"].unique()

    # Create dummy variables for Phase B and interaction
    data = data.copy()
    data["phaseB"] = (data[pvar] == "B").astype(int)
    data["interB"] = data[mvar] * data["phaseB"]

    # Create fixed-effects formula if not provided
    if fixed is None:
        fixed = create_fixed_formula(dvar, mvar, slope, level, trend, "phaseB", "interB")
    if update_fixed:
        fixed += f" {update_fixed}"

    # Create random-effects formula if not provided
    if random is None and len(case_names) > 1:
        random = "1 | case"
    if any([random_trend, random_level, random_slope]):
        random = create_random_formula(mvar, random_slope, random_level, random_trend, "phaseB", "interB")

    # Combine fixed and random formulas
    model_formula = fixed
    if random:
        model_formula += f" + ({random})"

    # Fit the Bayesian model using Bambi
    bayes_model = bmb.Model(model_formula, data=data)
    idata = bayes_model.fit(draws=samples, chains=2)

    # Ensure log_likelihood exists (if not, add it)
    idata = ensure_log_likelihood(idata, bayes_model)

    # Compute WAIC; if WAIC attribute is missing, set DIC as NA
    try:
        waic_res = az.waic(idata)
        dic = waic_res.waic
    except Exception as e:
        print(f"WAIC computation failed: {e}")
        dic = np.nan

    # Extract posterior summary using ArviZ
    summary_df = az.summary(idata, kind="stats")
    summary_df = summary_df.reset_index().rename(columns={"index": "Variable", "mean": "Estimate"})
    
    # Select only the columns we need. Some versions of ArviZ might not include ess_bulk or mcse_mean.
    cols_to_keep = ["Variable", "Estimate", "hdi_3%", "hdi_97%"]
    for col in ["ess_bulk", "mcse_mean"]:
        if col not in summary_df.columns:
            summary_df[col] = np.nan
            cols_to_keep.append(col)
        else:
            cols_to_keep.append(col)
    summary_df = summary_df[cols_to_keep]
    summary_df = summary_df.rename(columns={"hdi_3%": "Lower 95% CI", 
                                              "hdi_97%": "Upper 95% CI",
                                              "ess_bulk": "Sample Size",
                                              "mcse_mean": "p"})

    # Format the output string
    result_str = "Bayesian Piecewise Linear Regression\n\n"
    result_str += f"Contrast model: {bayes_model} (level: {contrast_level}, slope: {contrast_slope})\n"
    result_str += f"Deviance Information Criterion: {dic:.4f}\n\n"
    result_str += f"B-structure - Fixed effects ({dvar} ~ 1 + {mvar} + phaseB + interB)\n\n"
    result_str += summary_df.to_string(index=False) + "\n\n"
    
    sigma_df = summary_df[summary_df["Variable"] == "sigma"]
    if not sigma_df.empty:
        result_str += "R-Structure - Residuals\n\n"
        result_str += sigma_df.to_string(index=False) + "\n"

    return result_str
