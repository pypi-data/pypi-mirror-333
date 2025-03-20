import pandas as pd
import numpy as np
from scipy.stats import binomtest, norm
from sklearn.linear_model import LinearRegression
from scia.preprocess import prepare_scd
from scia.recombine import recombine_phases
from scia.utils import revise_names

def pet(data, dvar="values", pvar="phase", mvar="mt", ci=0.95, decreasing=False, phases=("A", "B")):
    """
    Compute the Percentage Exceeding the Trend (PET) for single-case data.

    Parameters:
    - data (pd.DataFrame): The single-case dataset.
    - dvar (str): Name of the dependent variable column.
    - pvar (str): Name of the phase variable column.
    - mvar (str): Name of the measurement-time variable column.
    - ci (float, default=0.95): Confidence interval level.
    - decreasing (bool, default=False): If True, considers lower values in Phase B.
    - phases (tuple, default=("A", "B")): Phases to compare.

    Returns:
    - pd.DataFrame: A summary of PET calculations.
    """

    # Ensure "case" column exists
    if "case" not in data.columns:
        data["case"] = "NAs"  # Default case if missing

    # Prepare the data
    data = prepare_scd(data)
    keep = recombine_phases(data, phases=phases)
    case_names = revise_names(keep["case"].unique(), len(keep["case"].unique()))

    # Compute standard error factor for confidence intervals
    se_factor = norm.ppf(ci)  # Using qnorm(ci)

    # Create a dataframe for storing results
    results = pd.DataFrame(columns=["Case", "PET", "PET CI", "Binom.p"])
    results["Case"] = case_names

    # Iterate through each case
    for i, case in enumerate(case_names):
        case_data = keep.loc[keep["case"] == case]

        A = case_data.loc[case_data[pvar] == "A", [mvar, dvar]].dropna()
        B = case_data.loc[case_data[pvar] == "B", [mvar, dvar]].dropna()

        if len(A) < 2 or len(B) == 0:
            results.loc[i, ["PET", "PET CI", "Binom.p"]] = [np.nan, np.nan, np.nan]
            continue

        # Fit Linear Regression Model for Phase A
        X_A = A[[mvar]].values
        y_A = A[dvar].values
        model = LinearRegression().fit(X_A, y_A)
        
        # Predict values for Phase B
        X_B = B[[mvar]].values
        pred_B = model.predict(X_B)
        
        # Calculate residual standard error (RSE)
        residuals = y_A - model.predict(X_A)
        
        # Degrees of freedom: n - k - 1 (n = sample size, k = number of predictors)
        df = len(A) - 1 - 1
        if df < 1:
            results.loc[i, ["PET", "PET CI", "Binom.p"]] = [np.nan, np.nan, np.nan]
            continue
            
        rse = np.sqrt(np.sum(residuals**2) / df)
        
        # Calculate prediction standard errors for each B point
        # Formula: se.fit = rse * sqrt(1/n + (x - x_mean)²/SSx)
        X_A_mean = np.mean(X_A)
        SSx = np.sum((X_A - X_A_mean)**2)
        
        se_pred_B = np.array([
            rse * np.sqrt(1/len(A) + ((x - X_A_mean)**2)/SSx) 
            for x in X_B.flatten()
        ])
        
        # Calculate PET and PET CI exactly as in the R code
        if decreasing:
            # For each B point, check if it's below the prediction minus SE * factor
            pet_ci_val = np.mean(B[dvar].values < (pred_B - se_pred_B * se_factor)) * 100
            pet_val = np.mean(B[dvar].values < pred_B) * 100
            success_count = sum(B[dvar].values < pred_B)
        else:
            # For each B point, check if it's above the prediction plus SE * factor
            pet_ci_val = np.mean(B[dvar].values > (pred_B + se_pred_B * se_factor)) * 100
            pet_val = np.mean(B[dvar].values > pred_B) * 100
            success_count = sum(B[dvar].values > pred_B)

        # Compute binomial test
        total_B = len(B)
        binom_result = binomtest(success_count, total_B, 0.5, alternative="greater")
        p_value = binom_result.pvalue

        # Store results
        results.loc[i, "PET"] = round(pet_val, 1)
        results.loc[i, "PET CI"] = round(pet_ci_val, 1)
        results.loc[i, "Binom.p"] = f"{p_value:.6f}"

    return results