import pandas as pd
import numpy as np
from scia.preprocess import prepare_scd
from scia.recombine import recombine_phases
from scia.utils import revise_names

def smd(data, dvar="values", pvar="phase", mvar="mt", phases=(1, 2)):
    """
    Compute standardized mean differences for single-case data.

    Parameters:
    - data (pd.DataFrame): The single-case data.
    - dvar (str): Name of the dependent variable column.
    - pvar (str): Name of the phase variable column.
    - mvar (str): Name of the measurement-time variable column.
    - phases (tuple or list): Two phases to compare (default: (1,2)).

    Returns:
    - pd.DataFrame: A DataFrame containing computed effect sizes and phase details.
    """
    
    # Ensure we're working on a copy to avoid SettingWithCopyWarning
    data = data.copy()
    
    # Assign default case if missing
    if "case" not in data.columns:
        data["case"] = "Default_Case"
    
    # Prepare data
    data = prepare_scd(data)
    
    # Recombine phases
    keep = recombine_phases(data, phases=phases)
    
    # Extract cases
    case_names = revise_names(keep["case"].unique(), len(keep["case"].unique()))
    
    # Define effect size metrics
    vars = ["mA", "mB", "sdA", "sdB", "sd cohen", "sd hedges", "Glass' delta", 
            "Hedges' g", "Hedges' g correction", "Hedges' g durlak correction", "Cohen's d"]
    df = pd.DataFrame(columns=["Case"] + vars)
    df["Case"] = case_names
    
    # Compute effect sizes for each case
    for i, case in enumerate(case_names):
        case_data = keep.loc[keep["case"] == case].copy()
        
        A = case_data.loc[case_data[pvar] == "A", dvar].dropna()
        B = case_data.loc[case_data[pvar] == "B", dvar].dropna()
        
        nA, nB = len(A), len(B)
        n = nA + nB
        mA, mB = A.mean(), B.mean()
        sdA, sdB = A.std(), B.std()
        
        # Compute effect sizes
        df.loc[i, "mA"] = mA
        df.loc[i, "mB"] = mB
        df.loc[i, "sdA"] = sdA
        df.loc[i, "sdB"] = sdB
        df.loc[i, "Glass' delta"] = (mB - mA) / sdA
        df.loc[i, "sd hedges"] = np.sqrt(((nA - 1) * sdA**2 + (nB - 1) * sdB**2) / (nA + nB - 2))
        df.loc[i, "Hedges' g"] = (mB - mA) / df.loc[i, "sd hedges"]
        corr_hedges = 1 - (3 / (4 * n - 9))
        df.loc[i, "Hedges' g correction"] = df.loc[i, "Hedges' g"] * corr_hedges
        corr_durlak = (n - 3) / (n - 2.25) * np.sqrt((n - 2) / n)
        df.loc[i, "Hedges' g durlak correction"] = df.loc[i, "Hedges' g"] * corr_durlak
        df.loc[i, "sd cohen"] = np.sqrt((sdA**2 + sdB**2) / 2)
        df.loc[i, "Cohen's d"] = (mB - mA) / df.loc[i, "sd cohen"]
    
    # # Add phase details as DataFrame columns
    # df["Phases_A"] = keep["phase"].unique()[0]
    # df["Phases_B"] = keep["phase"].unique()[1]
    
    return df
