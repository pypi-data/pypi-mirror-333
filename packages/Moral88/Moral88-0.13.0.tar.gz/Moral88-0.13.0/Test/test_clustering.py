import pytest
import numpy as np
from Moral88.clustering import *
import warnings
from Moral88.utils import DataValidator


def test_adjusted_rand_index():
    labels_true = [0, 0, 1, 1, 2, 2]
    labels_pred = [0, 1, 1, 1, 2, 2]
    result = adjusted_rand_index(labels_true, labels_pred)
    assert result == pytest.approx(0.444, rel=1e-2)

def test_normalized_mutual_info():
    labels_true = [0, 0, 1, 1, 2, 2]
    labels_pred = [0, 1, 1, 1, 2, 2]
    result = normalized_mutual_info(labels_true, labels_pred)
    assert result == pytest.approx(0.557, rel=1e-2)

def test_silhouette_score():
    X = np.random.rand(6, 2)
    labels_pred = np.array([0, 1, 1, 1, 2, 2])
    result = silhouette_score(X, labels_pred)
    assert isinstance(result, float)

def test_calinski_harabasz_index():
    X = np.random.rand(6, 2)
    labels_pred = np.array([0, 1, 1, 1, 2, 2])
    result = calinski_harabasz_index(X, labels_pred)
    assert isinstance(result, float)

def test_dunn_index():
    X = np.random.rand(6, 2)
    labels_pred = np.array([0, 1, 1, 1, 2, 2])
    result = dunn_index(X, labels_pred)
    assert isinstance(result, float)

def test_inertia():
    X = np.random.rand(6, 2)
    labels_pred = np.array([0, 1, 1, 1, 2, 2])
    result = inertia(X, labels_pred)
    assert isinstance(result, float)

def test_homogeneity_score():
    labels_true = [0, 0, 1, 1, 2, 2]
    labels_pred = [0, 1, 1, 1, 2, 2]
    result = homogeneity_score(labels_true, labels_pred)
    assert isinstance(result, float)

def test_completeness_score():
    labels_true = [0, 0, 1, 1, 2, 2]
    labels_pred = [0, 1, 1, 1, 2, 2]
    result = completeness_score(labels_true, labels_pred)
    assert isinstance(result, float)

def test_davies_bouldin_index():
    X = np.random.rand(6, 2)
    labels_pred = np.array([0, 1, 1, 1, 2, 2])
    result = davies_bouldin_index(X, labels_pred)
    assert isinstance(result, float)

if __name__ == "__main__":
    pytest.main()
