import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from typing import List

def clean_text_column(series: pd.Series) -> pd.Series:
    """Trim whitespace, strip non-alphanumeric noise, and convert text to lowercase."""
    if not isinstance(series, pd.Series):
        raise TypeError("Input must be a pandas Series.")
    return series.astype(str).str.strip().str.lower()

def impute_missing_numeric(df: pd.DataFrame, column: str, strategy: str = "mean") -> pd.DataFrame:
    """Impute missing numerical entries using either mean or median strategy."""
    if column not in df.columns:
        raise KeyError(f"Column '{column}' does not exist in the DataFrame.")
    
    df_copy = df.copy()
    if strategy == "mean":
        fill_val = df_copy[column].mean()
    elif strategy == "median":
        fill_val = df_copy[column].median()
    else:
        raise ValueError("Strategy must be either 'mean' or 'median'.")

    df_copy[column] = df_copy[column].fillna(fill_val)
    return df_copy

def scale_numeric_features(df: pd.DataFrame, feature_cols: List[str]) -> np.ndarray:
    """Standardize numerical columns to zero mean and unit variance."""
    for col in feature_cols:
        if col not in df.columns:
            raise KeyError(f"Feature column '{col}' missing from DataFrame.")
        if df[col].isnull().any():
            raise ValueError(f"Column '{col}' contains NaN values. Impute before scaling.")
    
    scaler = StandardScaler()
    return scaler.fit_transform(df[feature_cols])