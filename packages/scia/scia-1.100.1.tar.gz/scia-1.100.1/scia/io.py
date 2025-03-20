import pandas as pd

def read_scd(file, cvar="case", pvar="phase", dvar="values", mvar="mt", 
             sort_cases=False, phase_names=None, file_type=None, 
             na_values=["", "NA"], **kwargs):
    """
    Import Single-Case DataFrame (SCD) from CSV, Excel, or other formats.

    Parameters:
    - file (str): Path to the data file (CSV or Excel).
    - cvar (str, default="case"): Column name for case identification.
    - pvar (str, default="phase"): Column name for phase labels.
    - dvar (str, default="values"): Column name for dependent variable.
    - mvar (str, default="mt"): Column name for measurement-time.
    - sort_cases (bool, default=False): Whether to sort cases.
    - phase_names (list, optional): Rename phase labels (e.g., [“A”, “B”]).
    - file_type (str, optional): Manually specify file type (csv, xls, xlsx).
    - na_values (list, default=["", "NA"]): Values to treat as missing.
    - **kwargs: Additional parameters for pandas read functions.

    Returns:
    - pd.DataFrame: Imported Single-Case DataFrame.
    """
    
    # Determine file type if not provided
    if file_type is None:
        file_type = file.split('.')[-1].lower()

    # Read data based on file type
    if file_type == "csv":
        df = pd.read_csv(file, na_values=na_values, **kwargs)
    elif file_type in ["xlsx", "xls"]:
        df = pd.read_excel(file, na_values=na_values, **kwargs)
    else:
        raise ValueError(f"Unsupported file type: {file_type}")

    # Rename columns if different names are used
    column_mapping = {cvar: "case", pvar: "phase", dvar: "values", mvar: "mt"}
    df.rename(columns=column_mapping, inplace=True)

    # Apply phase name conversion if specified
    if phase_names:
        df["phase"] = df["phase"].replace({i: name for i, name in enumerate(phase_names)})

    # Sort cases if needed
    if sort_cases:
        df.sort_values(by="case", inplace=True)

    print(f"Imported {df['case'].nunique()} cases")

    return df

def write_scd(data, filename, sep=",", dec=".", file_type=None, **kwargs):
    """
    Export a Single-Case DataFrame (SCD) to a CSV or Excel file.

    Parameters:
    - data (pd.DataFrame): The SCD data to export.
    - filename (str): The output file path.
    - sep (str, default=","): Column separator for CSV files.
    - dec (str, default="."): Decimal point format.
    - file_type (str, optional): Manually specify file type (csv, xls, xlsx).
    - **kwargs: Additional arguments for pandas write functions.

    Returns:
    - None: Writes file to disk.
    """

    # Determine file type if not provided
    if file_type is None:
        file_type = filename.split('.')[-1].lower()

    # Convert decimal format if needed
    if dec == ",":
        data = data.applymap(lambda x: str(x).replace(".", ",") if isinstance(x, float) else x)

    # Write to file based on file type
    if file_type == "csv":
        data.to_csv(filename, index=False, sep=sep, **kwargs)
    elif file_type in ["xlsx", "xls"]:
        data.to_excel(filename, index=False, engine="xlsxwriter", **kwargs)
    else:
        raise ValueError(f"Unsupported file type: {file_type}")

    print(f"Data successfully saved to {filename}")
