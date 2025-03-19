import pandas as pd

def summary_stats(df: pd.DataFrame, verbose: bool = True):
    """
    Generate summary statistics for a Pandas DataFrame.

    Parameters:
    df (pd.DataFrame): The input DataFrame.
    verbose (bool): If True, prints the summary. If False, returns data silently.

    Returns:
    tuple:
        - summary (pd.DataFrame): Columns, data types, missing values, unique values.
        - descriptive_stats (pd.DataFrame): Descriptive statistics (numeric + categorical).
    
    Example:
    >>> import pandas as pd
    >>> from summary_stats import summary_stats
    >>> df = pd.DataFrame({"A": [1, 2, 3, None], "B": ["x", "y", "z", "x"]})
    >>> summary, desc = summary_stats(df)
    >>> print(summary)
    """

    # Check if input is a valid DataFrame
    if not isinstance(df, pd.DataFrame):
        raise TypeError("Input must be a pandas DataFrame.")
    
    if df.empty:
        raise ValueError("DataFrame is empty. Provide a valid dataset.")

    # Summary table with column info
    summary = pd.DataFrame({
        "Column Name": df.columns,
        "Data Type": df.dtypes.values,
        "Missing Values": df.isnull().sum().values,
        "Unique Values": df.nunique().values
    })
    
    shape_info = f"Dataset Shape: {df.shape[0]} rows × {df.shape[1]} columns"
    memory_usage = f"Memory Usage: {df.memory_usage(deep=True).sum() / 1_048_576:.2f} MB"

    # Descriptive statistics (numeric + categorical)
    desc = df.describe(include="all").transpose()

    # Print only if verbose=True
    if verbose:
        print("\n" + "=" * 100)
        print(shape_info)
        print(memory_usage)
        print("=" * 100)

        print("\nSummary Statistics:\n")
        print(summary.to_string(index=False))
        print("=" * 100)

        print("\nDescriptive Statistics:\n")
        print(desc.to_string())
        print("=" * 100)

    return summary, desc
