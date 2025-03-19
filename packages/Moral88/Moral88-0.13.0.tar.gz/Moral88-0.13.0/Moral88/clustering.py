import numpy as np
from Moral88.utils import DataValidator

validator = DataValidator()


def adjusted_rand_index(labels_true, labels_pred):
    """Compute Adjusted Rand Index (ARI)"""
    validator.validate_all(labels_true, labels_pred)
    n = len(labels_true)
    contingency_matrix = np.zeros((len(set(labels_true)), len(set(labels_pred))))
    
    for i in range(n):
        contingency_matrix[labels_true[i], labels_pred[i]] += 1
    
    sum_comb_c = np.sum([np.sum(row) * (np.sum(row) - 1) for row in contingency_matrix]) / 2
    sum_comb_k = np.sum([np.sum(col) * (np.sum(col) - 1) for col in contingency_matrix.T]) / 2
    sum_comb = np.sum(contingency_matrix * (contingency_matrix - 1)) / 2
    
    expected_index = (sum_comb_c * sum_comb_k) / (n * (n - 1) / 2)
    max_index = (sum_comb_c + sum_comb_k) / 2
    
    return (sum_comb - expected_index) / (max_index - expected_index) if max_index != expected_index else 1

def normalized_mutual_info(labels_true, labels_pred, epsilon=1e-10):
    """Compute Normalized Mutual Information (NMI) avoid devided by zero"""
    validator.validate_all(labels_true, labels_pred)
    unique_true, counts_true = np.unique(labels_true, return_counts=True)
    unique_pred, counts_pred = np.unique(labels_pred, return_counts=True)
    
    contingency_matrix = np.zeros((len(unique_true), len(unique_pred)))
    for i in range(len(labels_true)):
        contingency_matrix[labels_true[i], labels_pred[i]] += 1
    
    h_true = -np.sum((counts_true / len(labels_true)) * np.log2(np.where(counts_true > 0, counts_true / len(labels_true), epsilon)))
    h_pred = -np.sum((counts_pred / len(labels_pred)) * np.log2(np.where(counts_pred > 0, counts_pred / len(labels_pred), epsilon)))
    
    joint_prob = contingency_matrix / len(labels_true)
    mutual_info = np.sum(joint_prob * np.log2(np.where(joint_prob > 0, joint_prob / ((counts_true[:, None] / len(labels_true)) * (counts_pred[None, :] / len(labels_pred))), epsilon)))
    
    return mutual_info / np.sqrt(h_true * h_pred) if h_true * h_pred > 0 else 0

def silhouette_score(X, labels):
    """Compute Silhouette Score"""
    validator.validate_all(labels, labels)
    unique_labels = np.unique(labels)
    a = np.zeros(len(X))
    b = np.zeros(len(X))
    
    for i, label in enumerate(labels):
        same_cluster = X[labels == label]
        other_clusters = [X[labels == other_label] for other_label in unique_labels if other_label != label]
        
        a[i] = np.mean(np.linalg.norm(same_cluster - X[i], axis=1)) if len(same_cluster) > 1 else 0
        b[i] = np.min([np.mean(np.linalg.norm(other_cluster - X[i], axis=1)) for other_cluster in other_clusters]) if other_clusters else 0
    
    silhouette_values = (b - a) / np.maximum(a, b)
    return np.mean(silhouette_values)

def calinski_harabasz_index(X, labels):
    """Compute Calinski-Harabasz Index"""
    validator.validate_all(labels, labels)
    n_clusters = len(np.unique(labels))
    n_samples = len(X)
    cluster_means = np.array([np.mean(X[labels == label], axis=0) for label in np.unique(labels)])
    overall_mean = np.mean(X, axis=0)
    
    between_group_dispersion = np.sum([len(X[labels == label]) * np.linalg.norm(cluster_mean - overall_mean)**2 for label, cluster_mean in zip(np.unique(labels), cluster_means)])
    within_group_dispersion = np.sum([np.sum((X[labels == label] - cluster_mean) ** 2) for label, cluster_mean in zip(np.unique(labels), cluster_means)])
    
    return (between_group_dispersion / within_group_dispersion) * ((n_samples - n_clusters) / (n_clusters - 1))

def dunn_index(X, labels):
    """Compute Dunn Index"""
    validator.validate_all(labels, labels)
    unique_labels = np.unique(labels)
    cluster_means = [np.mean(X[labels == label], axis=0) for label in unique_labels]
    intra_distances = [np.max(np.linalg.norm(X[labels == label] - cluster_mean, axis=1)) for label, cluster_mean in zip(unique_labels, cluster_means)]
    inter_distances = [np.linalg.norm(cluster_means[i] - cluster_means[j]) for i in range(len(unique_labels)) for j in range(i + 1, len(unique_labels))]
    return np.min(inter_distances) / np.max(intra_distances)

def inertia(X, labels):
    """Compute Inertia (Sum of Squared Distances to Centroids)"""
    validator.validate_all(labels, labels)
    unique_labels = np.unique(labels)
    cluster_means = [np.mean(X[labels == label], axis=0) for label in unique_labels]
    return np.sum([np.sum((X[labels == label] - cluster_means[i]) ** 2) for i, label in enumerate(unique_labels)])

def homogeneity_score(labels_true, labels_pred, epsilon=1e-10):
    """Compute Homogeneity Score avoid devided by zero"""
    validator.validate_all(labels_true, labels_pred)
    unique_true, counts_true = np.unique(labels_true, return_counts=True)
    unique_pred, counts_pred = np.unique(labels_pred, return_counts=True)
    contingency_matrix = np.zeros((len(unique_true), len(unique_pred)))
    
    for i in range(len(labels_true)):
        contingency_matrix[labels_true[i], labels_pred[i]] += 1
    
    entropy_true = -np.sum((counts_true / len(labels_true)) * np.log2(np.where(counts_true > 0, counts_true / len(labels_true), epsilon)))
    mutual_info = np.sum(contingency_matrix * np.log2(np.where(contingency_matrix > 0, contingency_matrix / ((counts_true[:, None] / len(labels_true)) * (counts_pred[None, :] / len(labels_pred))), epsilon)))
    
    return mutual_info / entropy_true if entropy_true > 0 else 0


def completeness_score(labels_true, labels_pred, epsilon=1e-10):
    """Compute Completeness Score avoid divided by zero"""
    validator.validate_all(labels_true, labels_pred)
    unique_true, counts_true = np.unique(labels_true, return_counts=True)
    unique_pred, counts_pred = np.unique(labels_pred, return_counts=True)
    contingency_matrix = np.zeros((len(unique_true), len(unique_pred)))
    
    for i in range(len(labels_true)):
        contingency_matrix[labels_true[i], labels_pred[i]] += 1
    
    entropy_pred = -np.sum((counts_pred / len(labels_pred)) * np.log2(np.where(counts_pred > 0, counts_pred / len(labels_pred), epsilon)))
    mutual_info = np.sum(contingency_matrix * np.log2(np.where(contingency_matrix > 0, contingency_matrix / ((counts_true[:, None] / len(labels_true)) * (counts_pred[None, :] / len(labels_pred))), epsilon)))
    
    return mutual_info / entropy_pred if entropy_pred > 0 else 0

def davies_bouldin_index(X, labels):
    """Compute Davies-Bouldin Index"""
    validator.validate_all(labels, labels)
    n_clusters = len(np.unique(labels))
    cluster_means = np.array([np.mean(X[labels == label], axis=0) for label in np.unique(labels)])
    
    dispersions = np.array([np.mean(np.linalg.norm(X[labels == label] - cluster_means[i], axis=1)) for i, label in enumerate(np.unique(labels))])
    db_index = np.mean([max([(dispersions[i] + dispersions[j]) / np.linalg.norm(cluster_means[i] - cluster_means[j]) for j in range(n_clusters) if i != j]) for i in range(n_clusters)])
    
    return db_index