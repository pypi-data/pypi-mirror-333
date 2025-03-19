import numpy as np
from Moral88.utils import DataValidator

validator = DataValidator()


def mean_absolute_error(y_true, y_pred, sample_weights=None, normalize=False, method='mean'):
    """Compute Mean Absolute Error (MAE)"""
    validator.validate_all(y_true, y_pred)
    errors = np.abs(y_true - y_pred)

    if sample_weights is not None:
        sample_weights = np.array(sample_weights)
        if len(sample_weights) != len(y_true):
            raise ValueError("sample_weights must have the same length as y_true and y_pred")
        errors *= sample_weights

    if normalize:
        errors /= np.mean(y_true)

    if method == 'mean':
        return np.mean(errors)
    elif method == 'sum':
        return np.sum(errors)
    elif method == 'none':
        return errors
    else:
        raise ValueError("Invalid method. Choose from 'mean', 'sum', or 'none'")

def mean_squared_error(y_true, y_pred, sample_weights=None, squared=True, method='mean'):
    """Compute Mean Squared Error (MSE) or Root Mean Squared Error (RMSE)"""
    validator.validate_all(y_true, y_pred)
    errors = (y_true - y_pred) ** 2

    if sample_weights is not None:
        sample_weights = np.array(sample_weights)
        if len(sample_weights) != len(y_true):
            raise ValueError("sample_weights must have the same length as y_true and y_pred")
        errors *= sample_weights

    if method == 'mean':
        result = np.mean(errors)
    elif method == 'sum':
        result = np.sum(errors)
    elif method == 'none':
        return errors
    else:
        raise ValueError("Invalid method. Choose from 'mean', 'sum', or 'none'")

    return result if squared else np.sqrt(result)

def root_mean_squared_error(y_true, y_pred, sample_weights=None, method='mean'):
    """Compute Root Mean Squared Error (RMSE)"""
    validator.validate_all(y_true, y_pred)
    errors = (y_true - y_pred) ** 2

    if sample_weights is not None:
        sample_weights = np.array(sample_weights)
        if len(sample_weights) != len(y_true):
            raise ValueError("sample_weights must have the same length as y_true and y_pred")
        errors *= sample_weights

    if method == 'mean':
        result = np.mean(errors)
    elif method == 'sum':
        result = np.sum(errors)
    elif method == 'none':
        return np.sqrt(errors)
    else:
        raise ValueError("Invalid method. Choose from 'mean', 'sum', or 'none'")

    return np.sqrt(result)

def mean_bias_deviation(y_true, y_pred, sample_weights=None, method='mean'):
    """Compute Mean Bias Deviation (MBD)"""
    validator.validate_all(y_true, y_pred)
    errors = y_true - y_pred

    if sample_weights is not None:
        sample_weights = np.array(sample_weights)
        if len(sample_weights) != len(y_true):
            raise ValueError("sample_weights must have the same length as y_true and y_pred")
        errors *= sample_weights

    if method == 'mean':
        return np.mean(errors)
    elif method == 'sum':
        return np.sum(errors)
    elif method == 'none':
        return errors
    else:
        raise ValueError("Invalid method. Choose from 'mean', 'sum', or 'none'")

def r_squared(y_true, y_pred, adjusted=False, n_features=None):
    """Compute R-squared (R²) and Adjusted R-squared if needed"""
    validator.validate_all(y_true, y_pred)
    ss_total = np.sum((y_true - np.mean(y_true)) ** 2)
    ss_residual = np.sum((y_true - y_pred) ** 2)
    r2 = 1 - (ss_residual / ss_total)

    if adjusted:
        if n_features is None:
            raise ValueError("n_features must be provided for adjusted R² calculation")
        n = len(y_true)
        return 1 - ((1 - r2) * (n - 1) / (n - n_features - 1))

    return r2

def adjusted_r_squared(y_true, y_pred, n_features):
    """Compute Adjusted R-squared (R² Adjusted)"""
    validator.validate_all(y_true, y_pred)

    n = len(y_true)
    if n_features >= n:
        raise ValueError("Number of features must be less than number of samples")

    ss_total = np.sum((y_true - np.mean(y_true)) ** 2)
    ss_residual = np.sum((y_true - y_pred) ** 2)
    r2 = 1 - (ss_residual / ss_total)

    return 1 - ((1 - r2) * (n - 1) / (n - n_features - 1))

def mean_absolute_percentage_error(y_true, y_pred, sample_weights=None, method='mean'):
    """Compute Mean Absolute Percentage Error (MAPE)"""
    validator.validate_all(y_true, y_pred, mape_based=True)
    errors = np.abs((y_true - y_pred) / y_true) * 100

    if sample_weights is not None:
        sample_weights = np.array(sample_weights)
        if len(sample_weights) != len(y_true):
            raise ValueError("sample_weights must have the same length as y_true and y_pred")
        errors *= sample_weights

    if method == 'mean':
        return np.mean(errors)
    elif method == 'sum':
        return np.sum(errors)
    elif method == 'none':
        return errors
    else:
        raise ValueError("Invalid method. Choose from 'mean', 'sum', or 'none'")

def symmetric_mean_absolute_percentage_error(y_true, y_pred, sample_weights=None, method='mean'):
    """Compute Symmetric Mean Absolute Percentage Error (sMAPE)"""
    validator.validate_all(y_true, y_pred, mape_based=True)
    errors = 200 * np.abs(y_true - y_pred) / (np.abs(y_true) + np.abs(y_pred))

    if sample_weights is not None:
        sample_weights = np.array(sample_weights)
        if len(sample_weights) != len(y_true):
            raise ValueError("sample_weights must have the same length as y_true and y_pred")
        errors *= sample_weights

    if method == 'mean':
        return np.mean(errors)
    elif method == 'sum':
        return np.sum(errors)
    elif method == 'none':
        return errors
    else:
        raise ValueError("Invalid method. Choose from 'mean', 'sum', or 'none'")

def huber_loss(y_true, y_pred, delta=1.0, sample_weights=None, method='mean'):
    """Compute Huber Loss"""
    validator.validate_all(y_true, y_pred)
    error = y_true - y_pred

    loss = np.where(np.abs(error) <= delta, 0.5 * error ** 2, delta * (np.abs(error) - 0.5 * delta))

    if sample_weights is not None:
        sample_weights = np.array(sample_weights)
        if len(sample_weights) != len(y_true):
            raise ValueError("sample_weights must have the same length as y_true and y_pred")
        loss *= sample_weights

    if method == 'mean':
        return np.mean(loss)
    elif method == 'sum':
        return np.sum(loss)
    elif method == 'none':
        return loss
    else:
        raise ValueError("Invalid method. Choose from 'mean', 'sum', or 'none'")

def relative_squared_error(y_true, y_pred):
    """Compute Relative Squared Error (RSE)"""
    validator.validate_all(y_true, y_pred)
    return np.sum((y_true - y_pred) ** 2) / np.sum((y_true - np.mean(y_true)) ** 2)

def mean_squared_log_error(y_true, y_pred, sample_weights=None, method='mean', squared=True):
    """Compute Logarithmic Mean Squared Error (MSLE) or Root Mean Squared Log Error (RMSLE)"""
    validator.validate_all(y_true, y_pred, log_based=True)
    errors = (np.log1p(y_true) - np.log1p(y_pred)) ** 2

    if sample_weights is not None:
        sample_weights = np.array(sample_weights)
        if len(sample_weights) != len(y_true):
            raise ValueError("sample_weights must have the same length as y_true and y_pred")
        errors *= sample_weights

    if method == 'mean':
        result = np.mean(errors)
    elif method == 'sum':
        result = np.sum(errors)
    elif method == 'none':
        return errors
    else:
        raise ValueError("Invalid method. Choose from 'mean', 'sum', or 'none'")

    return result if squared else np.sqrt(result)

def root_mean_squared_log_error(y_true, y_pred, sample_weights=None, method='mean'):
    """Compute Root Mean Squared Logarithmic Error (RMSLE)"""
    validator.validate_all(y_true, y_pred, log_based=True)
    errors = (np.log1p(y_true) - np.log1p(y_pred)) ** 2

    if sample_weights is not None:
        sample_weights = np.array(sample_weights)
        if len(sample_weights) != len(y_true):
            raise ValueError("sample_weights must have the same length as y_true and y_pred")
        errors *= sample_weights

    if method == 'mean':
        return np.sqrt(np.mean(errors))
    elif method == 'sum':
        return np.sqrt(np.sum(errors))
    elif method == 'none':
        return np.sqrt(errors)
    else:
        raise ValueError("Invalid method. Choose from 'mean', 'sum', or 'none'")

def log_cosh_loss(y_true, y_pred, sample_weights=None, method='mean'):
    """Compute Log-Cosh Loss"""
    validator.validate_all(y_true, y_pred)
    errors = np.log(np.cosh(y_pred - y_true))

    if sample_weights is not None:
        sample_weights = np.array(sample_weights)
        if len(sample_weights) != len(y_true):
            raise ValueError("sample_weights must have the same length as y_true and y_pred")
        errors *= sample_weights

    if method == 'mean':
        return np.mean(errors)
    elif method == 'sum':
        return np.sum(errors)
    elif method == 'none':
        return errors
    else:
        raise ValueError("Invalid method. Choose from 'mean', 'sum', or 'none'")

def explained_variance(y_true, y_pred):
    """Compute Explained Variance Score"""
    validator.validate_all(y_true, y_pred)
    variance_y_true = np.var(y_true)
    return 1 - (np.var(y_true - y_pred) / variance_y_true) if variance_y_true != 0 else 0

def median_absolute_error(y_true, y_pred, sample_weights=None):
    """Compute Median Absolute Error"""
    validator = DataValidator()
    validator.validate_all(y_true, y_pred)
    errors = np.abs(y_true - y_pred)

    if sample_weights is not None:
        sample_weights = np.array(sample_weights)
        if len(sample_weights) != len(y_true):
            raise ValueError("sample_weights must have the same length as y_true and y_pred")
        errors *= sample_weights

    return np.median(errors)

