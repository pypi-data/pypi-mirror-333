import pytest
import numpy as np
from Moral88.regression import (
                                mean_absolute_error,
                                mean_squared_error,
                                root_mean_squared_error,
                                mean_bias_deviation,
                                r_squared,
                                adjusted_r_squared,
                                mean_absolute_percentage_error,
                                symmetric_mean_absolute_percentage_error,
                                huber_loss,
                                relative_squared_error,
                                mean_squared_log_error,
                                root_mean_squared_log_error,
                                log_cosh_loss,
                                explained_variance,
                                median_absolute_error
)
import warnings
from Moral88.utils import DataValidator

validator = DataValidator()

def test_is_1d_array():
    validator = DataValidator()
    array = [[1], [2], [3]]
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", UserWarning)
        result = validator.is_1d_array(array, warn=True)
    assert result.ndim == 1
    assert np.array_equal(result, np.array([1, 2, 3]))

def test_check_samples():
    validator = DataValidator()
    array = [[1, 2], [3, 4], [5, 6]]
    result = validator.check_samples(array)
    assert result == 3

def test_check_consistent_length():
    validator = DataValidator()
    array1 = [1, 2, 3]
    array2 = [4, 5, 6]
    validator.check_consistent_length(array1, array2)  # Should not raise an error

    array3 = [7, 8]
    with pytest.raises(ValueError):
        validator.check_consistent_length(array1, array3)

def test_mean_absolute_error():
    y_true = [3, -0.5, 2, 7]
    y_pred = [2.5, 0.0, 2, 8]
    result = mean_absolute_error(y_true, y_pred)
    assert result == pytest.approx(0.5, rel=1e-2)

def test_mean_squared_error():
    y_true = [3, -0.5, 2, 7]
    y_pred = [2.5, 0.0, 2, 8]
    result = mean_squared_error(y_true, y_pred)
    assert result == pytest.approx(0.375, rel=1e-2)

def test_root_mean_squared_error():
    y_true = [3, -0.5, 2, 7]
    y_pred = [2.5, 0.0, 2, 8]
    result = root_mean_squared_error(y_true, y_pred)
    assert result == pytest.approx(0.612, rel=1e-2)

def test_mean_bias_deviation():
    y_true = [3, 5, 2, 7]
    y_pred = [2.5, 5.5, 2, 8]
    result = mean_bias_deviation(y_true, y_pred)
    assert result == pytest.approx(-0.25, rel=1e-2)

def test_r_squared():
    y_true = [3, -0.5, 2, 7]
    y_pred = [2.5, 0.0, 2, 8]
    result = r_squared(y_true, y_pred)
    assert result == pytest.approx(0.948, rel=1e-2)

def test_adjusted_r_squared():
    y_true = [3, -0.5, 2, 7]
    y_pred = [2.5, 0.0, 2, 8]
    result = adjusted_r_squared(y_true, y_pred, n_features=2)
    assert result == pytest.approx(0.896, rel=1e-2)

def test_mean_absolute_percentage_error():
    y_true = [3, -0.5, 2, 7]
    y_pred = [2.5, 0.0, 2, 8]
    result = mean_absolute_percentage_error(y_true, y_pred)
    assert result == pytest.approx(27.77, rel=1e-2)

def test_symmetric_mean_absolute_percentage_error():
    y_true = [3, -0.5, 2, 7]
    y_pred = [2.5, 0.0, 2, 8]
    result = symmetric_mean_absolute_percentage_error(y_true, y_pred)
    assert result == pytest.approx(28.99, rel=1e-2)

def test_huber_loss():
    y_true = [3, -0.5, 2, 7]
    y_pred = [2.5, 0.0, 2, 8]
    result = huber_loss(y_true, y_pred)
    assert result == pytest.approx(0.3125, rel=1e-2)

def test_relative_squared_error():
    y_true = [3, -0.5, 2, 7]
    y_pred = [2.5, 0.0, 2, 8]
    result = relative_squared_error(y_true, y_pred)
    assert result == pytest.approx(0.052, rel=1e-2)

def test_mean_squared_log_error():
    y_true = [3, 5, 2, 7]
    y_pred = [2.5, 4.5, 2, 6.5]
    result = mean_squared_log_error(y_true, y_pred)
    assert result == pytest.approx(0.004, rel=1e-2)

def test_root_mean_squared_log_error():
    y_true = [3, 5, 2, 7]
    y_pred = [2.5, 4.5, 2, 6.5]
    result = root_mean_squared_log_error(y_true, y_pred)
    assert result == pytest.approx(0.063, rel=1e-2)

def test_log_cosh_loss():
    y_true = [3, -0.5, 2, 7]
    y_pred = [2.5, 0.0, 2, 8]
    result = log_cosh_loss(y_true, y_pred)
    assert result == pytest.approx(0.216, rel=1e-2)

def test_explained_variance():
    y_true = [3, -0.5, 2, 7]
    y_pred = [2.5, 0.0, 2, 8]
    result = explained_variance(y_true, y_pred)
    assert result == pytest.approx(0.95, rel=1e-2)

def test_median_absolute_error():
    y_true = [3, -0.5, 2, 7]
    y_pred = [2.5, 0.0, 2, 8]
    result = median_absolute_error(y_true, y_pred)
    assert result == pytest.approx(0.5, rel=1e-2)

if __name__ == "__main__":
    pytest.main()
