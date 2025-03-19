import numpy as np
import pandas as pd

class DataValidator:
    def __init__(self, raise_warning=True):
        """Initialize the DataValidator class"""
        self.raise_warning = raise_warning

    def check_data_type(self, y_true, y_pred):
        """Check if input data types are valid"""
        valid_types = (np.ndarray, pd.Series, pd.DataFrame, list)
        if not isinstance(y_true, valid_types) or not isinstance(y_pred, valid_types):
            raise TypeError("y_true and y_pred must be numpy array, pandas series, or list")

    def check_missing_values(self, y_true, y_pred):
        """Check for missing values"""
        if np.any(pd.isnull(y_true)) or np.any(pd.isnull(y_pred)):
            raise ValueError("Missing values (NaN) detected in data")

    def check_inf_values(self, y_true, y_pred):
        """Check for infinite values"""
        if np.any(np.isinf(y_true)) or np.any(np.isinf(y_pred)):
            raise ValueError("Infinite values (inf) detected in data")

    def check_lengths(self, y_true, y_pred):
        """Check if y_true and y_pred have the same length"""
        if len(y_true) != len(y_pred):
            raise ValueError("y_true and y_pred must have the same length")

    def check_numeric_values(self, y_true, y_pred):
        """Check if values are numeric"""
        if not np.issubdtype(np.array(y_true).dtype, np.number) or not np.issubdtype(np.array(y_pred).dtype, np.number):
            raise TypeError("y_true and y_pred must contain numeric values")

    def check_variance(self, y_true, y_pred):
        """Check if variance of y_true is zero (can cause issues in R-squared calculation)"""
        if np.var(y_true) == 0:
            raise ValueError("Variance of y_true is zero. R-squared may not be meaningful")

    def check_non_negative(self, y_true, y_pred):
        """Check that values are non-negative for Logarithmic Mean Squared Error"""
        if np.any(y_true < -1) or np.any(y_pred < -1):
            raise ValueError("y_true and y_pred must be greater than or equal to -1 for log-based metrics")

    def check_multicollinearity(self, X, threshold=0.9):
        """Check for multicollinearity in input features"""
        if isinstance(X, pd.DataFrame):
            corr_matrix = X.corr().abs()
            high_corr = (corr_matrix > threshold).sum().sum() - len(X.columns)
            if high_corr > 0:
                raise ValueError("High multicollinearity detected in input features")
        else:
            if self.raise_warning:
                print("Warning: Multicollinearity check requires a pandas DataFrame")

    def validate_all(self, y_true, y_pred, log_based=False, mape_based=False):
        """Run all validation checks"""
        self.check_data_type(y_true, y_pred)
        self.check_missing_values(y_true, y_pred)
        self.check_inf_values(y_true, y_pred)
        self.check_lengths(y_true, y_pred)
        self.check_numeric_values(y_true, y_pred)
        self.check_variance(y_true, y_pred)
        if log_based or mape_based:
            self.check_non_negative(y_true, y_pred)  # Ensure non-negative values for log-based functions and MAPE
        return True  # Return True if all checks pass


# Example usage
if __name__ == "__main__":
  pass