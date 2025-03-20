import pandas as pd
import numpy as np
from scipy import stats
from sklearn.linear_model import LinearRegression
import statsmodels.api as sm
from statsmodels.stats.diagnostic import acorr_ljungbox
from statsmodels.formula.api import gls
from statsmodels.regression.linear_model import GLS
from statsmodels.genmod.generalized_linear_model import GLM
from statsmodels.genmod import families
from statsmodels.tools.tools import add_constant
# from scia.data import prepare_scd
from scia.preprocess import prepare_scd
from scia.utils import revise_names

def plm(data, dvar="values", pvar="phase", mvar="mt",
        AR=0, model="W", family="gaussian",
        trend=True, level=True, slope=True,
        contrast="first", contrast_level=None, contrast_slope=None,
        formula=None, update=None, na_action="drop",
        r_squared=True, var_trials=None, dvar_percentage=False):
    """
    Piecewise Linear Regression Model for single-case data.

    Parameters:
    - data (pd.DataFrame): The single-case dataset.
    - dvar (str): Name of the dependent variable column.
    - pvar (str): Name of the phase variable column.
    - mvar (str): Name of the measurement-time variable column.
    - AR (int): Autoregressive order.
    - model (str): Model type: 'W', 'H-M', 'B&L-B', or 'JW'.
    - family (str): Distribution family: 'gaussian', 'binomial', etc.
    - trend (bool): Include trend term.
    - level (bool): Include level term.
    - slope (bool): Include slope term.
    - contrast (str): Contrasting method: 'first' or 'preceding'.
    - contrast_level, contrast_slope (str): Contrasting method specifically for level/slope.
    - formula (str): Custom formula if needed.
    - update (str): Formula update if needed.
    - na_action (str): How to handle NA values.
    - r_squared (bool): Calculate R² values.
    - var_trials (str or int): Variable name with number of trials (for binomial).
    - dvar_percentage (bool): Whether dependent variable is already percentage.

    Returns:
    - None: Prints the formatted summary of the piecewise regression analysis.
    """
    # Check arguments
    if family != "gaussian" and AR != 0:
        raise ValueError("Family is not 'gaussian' but AR is set.")

    if family == "binomial" and var_trials is None:
        raise ValueError("Family is 'binomial' but 'var_trials' is not defined.")

    if AR < 0:
        raise ValueError("AR must be non-negative.")

    # Handle contrast settings
    if contrast_level is None:
        contrast_level = contrast

    if contrast_slope is None:
        contrast_slope = contrast

    # Special case for 'JW' model
    if model == "JW":
        contrast_level = "preceding"
        contrast_slope = "preceding"
        model = "B&L-B"

    # Prepare data
    if isinstance(data, pd.DataFrame):
        df = data.copy()
    else:
        df = prepare_scd(data, na_rm=True)

    # Add dummy variables based on model and contrast settings
    df, var_phase, var_inter = add_dummy_variables(df, model, contrast_level, contrast_slope, pvar, mvar)

    # Create formula if not provided
    if formula is None:
        formula = create_fixed_formula(dvar, mvar, slope, level, trend, var_phase, var_inter)

    # Update formula if needed
    if update is not None:
        # Implementation of formula update would go here
        pass

    # Extract predictors from formula
    formula_parts = formula.split('~')
    response = formula_parts[0].strip()
    predictors_str = formula_parts[1].strip()
    predictors = [p.strip() for p in predictors_str.split('+')]
    if '1' in predictors:
        predictors.remove('1')

    # Create restricted formulas (one for each predictor)
    formulas_restricted = {}
    for p in predictors:
        restricted_predictors = [pred for pred in predictors if pred != p]
        restricted_formula = f"{response} ~ 1 + {' + '.join(restricted_predictors)}"
        formulas_restricted[p] = restricted_formula

    # Fit models based on AR and family
    if AR == 0:
        if family != "binomial":
            # Regular GLM
            model_formula = f"{formula}"
            full_model = sm.formula.glm(formula=model_formula, data=df, family=getattr(sm.families, family.capitalize())()).fit()
        else:
            # Binomial model with trials
            if isinstance(var_trials, str):
                trials = df[var_trials]
            else:
                trials = np.repeat(var_trials, len(df[dvar]))

            if not dvar_percentage:
                df[dvar] = df[dvar] / trials

            model_formula = f"{formula}"
            full_model = sm.formula.glm(
                formula=model_formula,
                data=df,
                family=sm.families.Binomial(),
                freq_weights=trials
            ).fit()
    else:
        # GLS with AR correlation structure
        model_formula = f"{formula}"
        full_model = sm.formula.gls(
            formula=model_formula,
            data=df,
            correlation=sm.regression.correlation.ARMA(ar=AR)
        ).fit()

    # Calculate statistics
    if family == "gaussian":
        n = full_model.nobs

        # Use resid_response instead of resid for GLM models
        residuals = full_model.resid_response  # Changed from full_model.resid

        df_effect = len(predictors)
        df_residuals = n - df_effect - 1  # -1 for intercept
        df_intercept = 1 if "Intercept" in full_model.params else 0

        QSE = np.sum(residuals**2)
        QST = np.sum((df[dvar] - df[dvar].mean())**2)
        MQSA = (QST - QSE) / df_effect
        MQSE = QSE / df_residuals
        F = MQSA / MQSE
        p = 1 - stats.f.cdf(F, df_effect, df_residuals)

        total_variance = df[dvar].var()
        r2 = 1 - (full_model.resid_response.var() / total_variance)
        r2_adj = 1 - ((1 - r2) * ((n - df_intercept) / df_residuals))

        # Calculate partial R² for each predictor
        r_squares = {}
        if r_squared:
            for pred, restricted_formula in formulas_restricted.items():
                restricted_model = sm.formula.glm(formula=restricted_formula, data=df, family=getattr(sm.families, family.capitalize())()).fit()
                restricted_r2 = 1 - (restricted_model.resid_response.var() / total_variance)
                r_squares[pred] = r2 - restricted_r2

        F_test = {
            'F': F,
            'df1': df_effect,
            'df2': df_residuals,
            'p': p,
            'R2': r2,
            'R2_adj': r2_adj
        }
    else:
        F_test = None
        r_squares = None

    # Calculate autocorrelations of residuals
    acf = sm.tsa.acf(full_model.resid_response, nlags=3)

    # Ljung-Box test
    lb_test = acorr_ljungbox(full_model.resid_response, lags=3)

    # Print the formatted summary
    print(format_plm_output(full_model, F_test, r_squares, model, contrast_level,
                             contrast_slope, family, acf, lb_test, mvar))

def add_dummy_variables(data, model, contrast_level, contrast_slope, pvar, mvar):
    """
    Add dummy variables for phases based on the selected model and contrast methods.

    Returns:
    - Modified dataframe, phase variable name, interaction variable name
    """
    df = data.copy()

    # Get unique phases
    phases = sorted(df[pvar].unique())

    # Create dummy variables based on model type
    if model == "W":  # White model
        # Create dummy variables for each phase (except reference)
        reference_phase = phases[0] if contrast_level == "first" else None

        # Create phase dummies
        df["phaseB"] = (df[pvar] != phases[0]).astype(int)

        # Create interaction terms
        df["interB"] = df["phaseB"] * df[mvar]

        var_phase = "phaseB"
        var_inter = "interB"

    elif model == "H-M":  # Huitema-McKean model
        # Set centered measurement time
        mt_centered = df[mvar] - df[mvar].mean()
        df["mt_c"] = mt_centered

        # Create phase dummies
        df["phaseB"] = (df[pvar] != phases[0]).astype(int)

        # Create interaction terms
        df["interB"] = df["phaseB"] * mt_centered

        var_phase = "phaseB"
        var_inter = "interB"

    elif model in ["B&L-B", "JW"]:  # Beeson & Robey - Brossart model or Johnson-Watson
        # Create dummy for each phase change
        for i in range(1, len(phases)):
            df[f"phase{phases[i]}"] = (df[pvar] == phases[i]).astype(int)

        # Create interaction terms for each phase change
        for i in range(1, len(phases)):
            df[f"inter{phases[i]}"] = df[f"phase{phases[i]}"] * df[mvar]

        var_phase = [f"phase{phase}" for phase in phases[1:]]
        var_inter = [f"inter{phase}" for phase in phases[1:]]

    return df, var_phase, var_inter

def create_fixed_formula(dvar, mvar, slope, level, trend, var_phase, var_inter):
    """Create a formula string for the model."""
    formula_parts = [dvar, "~", "1"]

    # Add appropriate terms with plus signs between them
    terms = []

    if trend:
        terms.append(mvar)

    if level:
        if isinstance(var_phase, list):
            terms.extend(var_phase)
        else:
            terms.append(var_phase)

    if slope:
        if isinstance(var_inter, list):
            terms.extend(var_inter)
        else:
            terms.append(var_inter)

    # Join all terms with plus signs
    if terms:
        formula_parts.append("+ " + " + ".join(terms))

    return " ".join(formula_parts)

def format_plm_output(model, F_test, r_squares, model_type, contrast_level, contrast_slope, family, acf, lb_test, mvar):
    """Format the output of the PLM analysis to match the desired format."""
    output_lines = []

    # Header
    output_lines.append("Piecewise Regression Analysis")
    output_lines.append("")

    # Contrast model information
    output_lines.append(f"Contrast model: {model_type} / level = {contrast_level}, slope = {contrast_slope}")
    output_lines.append("")

    # Distribution family
    output_lines.append(f"Fitted a {family} distribution.")

    # F-test, p-value, R², adjusted R², AIC
    if F_test:
        aic = model.aic
        output_lines.append(f"F({F_test['df1']}, {F_test['df2']}) = {F_test['F']:.2f}; p = {F_test['p']:.3f}; "
                           f"R² = {F_test['R2']:.3f}; Adjusted R² = {F_test['R2_adj']:.3f}; AIC = {aic:.4f}")
    else:
        output_lines.append(f"AIC = {model.aic:.4f}")

    output_lines.append("")

    # Coefficient table
    output_lines.append("{:<25} {:<10} {:<10} {:<10} {:<8} {:<8} {:<8} {:<8}".format(
        "", "B", "LL-CI95%", "UL-CI95%", "SE", "t", "p", "delta R²"))

    # Extract confidence intervals
    conf_int = model.conf_int()

    # Add each coefficient
    for param in model.params.index:
        coef = model.params[param]
        se = model.bse[param]
        tval = model.tvalues[param]
        pval = model.pvalues[param]
        ci_lower = conf_int.loc[param, 0]
        ci_upper = conf_int.loc[param, 1]

        # Get delta R² if available
        delta_r2 = r_squares.get(param, "") if r_squares else ""
        if delta_r2:
            delta_r2 = f"{delta_r2:.3f}"

        # Format parameter name
        param_name = param
        if param == "Intercept":
            param_name = "Intercept"
        elif param == mvar:
            param_name = "Trend (mt)"
        elif "phase" in param:
            param_name = f"Level phase B"
        elif "inter" in param:
            param_name = f"Slope phase B"

        output_lines.append("{:<25} {:<10.2f} {:<10.3f} {:<10.3f} {:<8.3f} {:<8.3f} {:<8.3f} {:<8}".format(
            param_name, coef, ci_lower, ci_upper, se, tval, pval, delta_r2))

    output_lines.append("")

    # Autocorrelations
    output_lines.append("Autocorrelations of the residuals")
    output_lines.append(" lag    cr")
    for i, ac in enumerate(acf[1:], 1):  # Skip lag 0 (always 1.0)
        output_lines.append(f"   {i}  {ac:.2f}")

    # Ljung-Box test
    lb_stat = lb_test.iloc[2, 0]  # 3rd lag
    lb_pval = lb_test.iloc[2, 1]
    output_lines.append(f"Ljung-Box test: X²(3) = {lb_stat:.2f}; p = {lb_pval:.3f}")

    # Add formula at the end
    output_lines.append("")
    output_lines.append(f"Formula: {model.model.formula}")

    # Join all lines and print
    print("\n".join(output_lines))
