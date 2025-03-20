
import pandas as pd
import numpy as np
from scia.preprocess import prepare_scd
from scia.recombine import recombine_phases
from scia.utils import revise_names
from scia.pand import pand

def ird(data, dvar="values", pvar="phase", decreasing=False, phases=("A", "B")):
    """
    Compute the Improvement Rate Difference (IRD) for single-case data.
    
    Parameters:
    - data (pd.DataFrame): The single-case dataset.
    - dvar (str): Name of the dependent variable column.
    - pvar (str): Name of the phase variable column.
    - decreasing (bool, default=False): If True, considers lower values in Phase B as improvement.
    - phases (tuple, default=("A", "B")): Phases to compare.
    
    Returns:
    - dict: A dictionary containing IRD results with class 'sc_ird'.
    """
    
    # Ensure "case" column exists
    if "case" not in data.columns:
        data["case"] = "Default_Case"
        
    # Prepare the data
    data = prepare_scd(data)
    recombined_data = recombine_phases(data, phases=phases)
    keep = recombined_data["data"] if isinstance(recombined_data, dict) else recombined_data
    
    # Get case names
    case_names = revise_names(keep["case"].unique(), len(keep["case"].unique()))
    
    # Calculate PAND with 'minimum' method (as used in R function)
    # Using return_values=True to get only the numeric values needed for IRD calculation
    pa = pand(data, dvar=dvar, pvar=pvar, decreasing=decreasing, 
              phases=phases, method="minimum", return_values=True)
    
    # Calculate IRD using the formula from the R function
    # IRD = 1 - ((n² / (2 * n_a * n_b)) * (1 - (pand / 100)))
    ird_value = 1 - (((pa["n"]**2) / (2 * pa["n_a"] * pa["n_b"])) * (1 - (pa["pand"] / 100)))
    
    # Create output object
    out = {
        "ird": ird_value,
        "decreasing": decreasing,
        "phases": recombined_data["phases"] if isinstance(recombined_data, dict) else phases
    }
    
    # Add class to output
    out["class"] = "sc_ird"
    
    # Print formatted output
    print("\nImprovement Rate Difference\n")
    print(f"IRD = {ird_value:.4f}\n")
    
    if decreasing:
        print("Note: Analysis assumes that lower values in B-phase represent improvement.")
    else:
        print("Note: Analysis assumes that higher values in B-phase represent improvement.")
    
    return out