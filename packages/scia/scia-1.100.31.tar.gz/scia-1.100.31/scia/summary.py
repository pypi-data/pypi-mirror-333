import pandas as pd

def summary_scd(data, max_cases=10):
    """
    Generate a summary of a Single-Case DataFrame (SCD) with proper formatting.

    Parameters:
    - data (pd.DataFrame): The SCD dataset.
    - max_cases (int, default=10): Maximum cases to display before truncating.

    Returns:
    - None: Prints a formatted summary.
    """

    # Extract case names
    cases = data["case"].unique()
    num_cases = len(cases)

    # Count number of measurements
    measurements_per_case = data.groupby("case")["values"].count()

    # Extract phase sequences
    phase_designs = data.groupby("case")["phase"].apply(lambda x: "-".join(x.unique()))

    # Print summary header
    print(f"\n# A single-case data frame with {num_cases} cases\n")
    print(f"{'':<15} Measurements  Design")

    # Limit display to max_cases (R truncates after 10 cases)
    displayed_cases = cases[:max_cases]
    for case in displayed_cases:
        print(f"{case:<15} {measurements_per_case[case]:<12} {phase_designs[case]}")

    # Show truncation message if more cases exist
    if num_cases > max_cases:
        print(f"... [skipped {num_cases - max_cases} cases]\n")

    # Print variable names
    print("\nVariable names:")
    for col in data.columns:
        print(f"  {col}{' <dependent variable>' if col == 'values' else ''}\
{' <phase variable>' if col == 'phase' else ''}\
{' <measurement-time variable>' if col == 'mt' else ''}")
