import pytest
import pandas as pd
import numpy as np
from src.pipeline import clean_text_column, impute_missing_numeric, scale_numeric_features

@pytest.fixture
def raw_dataset():
    """Provides a synthetic tabular dataset simulating uncleaned customer records."""
    return pd.DataFrame({
        "customer_name": ["  ALICE ", "Bob", " Charlie   ", "david"],
        "account_balance": [1000.0, np.nan, 3000.0, 4000.0],
        "credit_score": [650.0, 700.0, 750.0, np.nan]
    })

@pytest.mark.parametrize("input_series, expected_values", [
    (pd.Series(["  Data  ", "SCIENCE", " ai "]), ["data", "science", "ai"]),
    (pd.Series(["TEST", "TeSt ", "   test"]), ["test", "test", "test"])
])
def test_clean_text_column_variations(input_series, expected_values):
    """Ensure text sanitization handles varying whitespace and capitalization correctly."""
    result = clean_text_column(input_series)
    assert result.tolist() == expected_values

def test_clean_text_type_check():
    """Verify that passing invalid types raises a TypeError."""
    with pytest.raises(TypeError, match="Input must be a pandas Series"):
        clean_text_column(["invalid", "list", "input"])

@pytest.mark.parametrize("strategy, expected_imputed_value", [
    ("mean", 2666.6667),   # (1000 + 3000 + 4000) / 3
    ("median", 3000.0)      # Median of [1000, 3000, 4000]
])
def test_impute_missing_numeric_strategies(raw_dataset, strategy, expected_imputed_value):
    """Verify that numeric imputation adheres to the selected statistical strategy."""
    imputed_df = impute_missing_numeric(raw_dataset, "account_balance", strategy=strategy)
    
    assert imputed_df["account_balance"].isnull().sum() == 0
    assert np.isclose(imputed_df["account_balance"].iloc[1], expected_imputed_value, atol=1e-4)

def test_impute_invalid_strategy(raw_dataset):
    """Ensure unsupported imputation strategies raise a ValueError."""
    with pytest.raises(ValueError, match="Strategy must be either 'mean' or 'median'"):
        impute_missing_numeric(raw_dataset, "account_balance", strategy="mode")

def test_scale_features_unhandled_nulls(raw_dataset):
    """Ensure scaling fails early with a clear ValueError if missing values are present."""
    with pytest.raises(ValueError, match="contains NaN values"):
        scale_numeric_features(raw_dataset, ["account_balance"])

def test_scale_features_success(raw_dataset):
    """Verify standard scaling converts clean numeric features to mean=0 and std=1."""
    # Pre-clean dataset using pipeline functions
    df_imputed = impute_missing_numeric(raw_dataset, "account_balance", strategy="mean")
    df_imputed = impute_missing_numeric(df_imputed, "credit_score", strategy="mean")
    
    scaled_array = scale_numeric_features(df_imputed, ["account_balance", "credit_score"])
    
    assert scaled_array.shape == (4, 2)
    assert np.allclose(scaled_array.mean(axis=0), [0.0, 0.0], atol=1e-7)
    assert np.allclose(scaled_array.std(axis=0), [1.0, 1.0], atol=1e-7)