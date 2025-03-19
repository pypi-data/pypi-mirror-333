import pytest
import numpy as np
from Moral88.classification import *
import warnings
from Moral88.utils import DataValidator
validator = DataValidator()


def test_check_data_type():
    y_true = [1, 2, 3]
    y_pred = [1, 2, 3]
    assert validator.check_data_type(y_true, y_pred) is None
    with pytest.raises(TypeError):
        validator.check_data_type(123, y_pred)

def test_check_inf_values():
    y_true = np.array([1, 2, np.inf])
    y_pred = np.array([1, 2, 3])
    with pytest.raises(ValueError):
        validator.check_inf_values(y_true, y_pred)

def test_check_missing_values():
    y_true = np.array([1, 2, np.nan])
    y_pred = np.array([1, 2, 3])
    with pytest.raises(ValueError):
        validator.check_missing_values(y_true, y_pred)

def test_check_lengths():
    y_true = [1, 2, 3]
    y_pred = [1, 2]
    with pytest.raises(ValueError):
        validator.check_lengths(y_true, y_pred)

def test_validate_all():
    y_true = [1, 2, 3]
    y_pred = [1, 2, 3]
    assert validator.validate_all(y_true, y_pred) is True
    with pytest.raises(TypeError):
        validator.validate_all(123, y_pred)
    with pytest.raises(ValueError):
        validator.validate_all([1, 2, np.nan], [1, 2, 3])
    with pytest.raises(ValueError):
        validator.validate_all([1, 2, 3], [1, 2])

def test_accuracy():
    y_true = [0, 1, 1, 0, 1]
    y_pred = [0, 1, 0, 0, 1]
    result = accuracy(y_true, y_pred)
    assert result == pytest.approx(0.8, rel=1e-2)

def test_auc_roc():
    y_true = [0, 1, 1, 0, 1]
    y_probs = [0.1, 0.8, 0.4, 0.3, 0.9]
    result = auc_roc(y_true, y_probs, average='macro')
    assert result == pytest.approx(0.75, rel=1e-2)

def test_precision():
    y_true = [0, 1, 1, 0, 1]
    y_pred = [0, 1, 0, 0, 1]
    result = precision(y_true, y_pred, average='macro')
    assert result == pytest.approx(0.75, rel=1e-2)

def test_recall():
    y_true = [0, 1, 1, 0, 1]
    y_pred = [0, 1, 0, 0, 1]
    result = recall(y_true, y_pred, average='macro')
    assert result == pytest.approx(0.75, rel=1e-2)

def test_balanced_accuracy():
    y_true = [0, 1, 1, 0, 1]
    y_pred = [0, 1, 0, 0, 1]
    result = balanced_accuracy(y_true, y_pred)
    assert result == pytest.approx(0.75, rel=1e-2)

def test_matthews_correlation_coefficient():
    y_true = [0, 1, 1, 0, 1]
    y_pred = [0, 1, 0, 0, 1]
    result = matthews_correlation_coefficient(y_true, y_pred)
    assert result == pytest.approx(0.632, rel=1e-2)

def test_cohens_kappa():
    y_true = [0, 1, 1, 0, 1]
    y_pred = [0, 1, 0, 0, 1]
    result = cohens_kappa(y_true, y_pred)
    assert result == pytest.approx(0.5, rel=1e-2)

if __name__ == "__main__":
    pytest.main()