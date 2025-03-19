import numpy as np
import pandas as pd
from Moral88.utils import DataValidator

validator = DataValidator()
def accuracy(y_true, y_pred):
    """Compute Accuracy"""
    validator.validate_all(y_true, y_pred)
    return np.sum(y_true == y_pred) / len(y_true)

def auc_roc(y_true, y_scores, average='macro'):
    """Compute AUC-ROC Score"""
    validator.validate_all(y_true, np.round(y_scores))
    unique_classes = np.unique(y_true)
    aucs = []
    
    for cls in unique_classes:
        y_binary = (y_true == cls).astype(int)
        sorted_indices = np.argsort(y_scores[:, cls])[::-1]
        y_sorted = y_binary[sorted_indices]
        cum_true = np.cumsum(y_sorted)
        cum_false = np.cumsum(1 - y_sorted)
        auc = np.sum(cum_true * (1 - y_sorted)) / (cum_true[-1] * cum_false[-1]) if (cum_true[-1] > 0 and cum_false[-1] > 0) else 0
        aucs.append(auc)
    
    if average == 'macro':
        return np.mean(aucs)
    elif average == 'weighted':
        class_counts = np.bincount(y_true)
        return np.sum([aucs[i] * class_counts[i] for i in range(len(unique_classes))]) / len(y_true)
    return aucs

def precision(y_true, y_pred, average='binary'):
    """Compute Precision Score"""
    validator.validate_all(y_true, y_pred)
    unique_classes = np.unique(y_true)
    precisions = []
    
    for cls in unique_classes:
        tp = np.sum((y_true == cls) & (y_pred == cls))
        fp = np.sum((y_true != cls) & (y_pred == cls))
        precisions.append(tp / (tp + fp) if (tp + fp) > 0 else 0)
    
    if average == 'macro':
        return np.mean(precisions)
    elif average == 'micro':
        tp_total = np.sum(y_true == y_pred)
        fp_total = np.sum(y_true != y_pred)
        return tp_total / (tp_total + fp_total) if (tp_total + fp_total) > 0 else 0
    elif average == 'weighted':
        class_counts = np.bincount(y_true)
        return np.sum([precisions[i] * class_counts[i] for i in range(len(unique_classes))]) / len(y_true)
    return precisions

def recall(y_true, y_pred, average='binary'):
    """Compute Recall Score"""
    validator.validate_all(y_true, y_pred)
    unique_classes = np.unique(y_true)
    recalls = []
    
    for cls in unique_classes:
        tp = np.sum((y_true == cls) & (y_pred == cls))
        fn = np.sum((y_true == cls) & (y_pred != cls))
        recalls.append(tp / (tp + fn) if (tp + fn) > 0 else 0)
    
    if average == 'macro':
        return np.mean(recalls)
    elif average == 'micro':
        tp_total = np.sum(y_true == y_pred)
        fn_total = np.sum(y_true != y_pred)
        return tp_total / (tp_total + fn_total) if (tp_total + fn_total) > 0 else 0
    elif average == 'weighted':
        class_counts = np.bincount(y_true)
        return np.sum([recalls[i] * class_counts[i] for i in range(len(unique_classes))]) / len(y_true)
    return recalls
def balanced_accuracy(y_true, y_pred):
    """Compute Balanced Accuracy"""
    validator.validate_all(y_true, y_pred)
    unique_classes = np.unique(y_true)
    recalls = []
    
    for cls in unique_classes:
        tp = np.sum((y_true == cls) & (y_pred == cls))
        fn = np.sum((y_true == cls) & (y_pred != cls))
        recalls.append(tp / (tp + fn) if (tp + fn) > 0 else 0)
    
    return np.mean(recalls)

def matthews_correlation_coefficient(y_true, y_pred):
    """Compute Matthews Correlation Coefficient (MCC)"""
    validator.validate_all(y_true, y_pred)
    unique_classes = np.unique(y_true)
    confusion_mat = np.zeros((len(unique_classes), len(unique_classes)), dtype=int)
    
    for i, cls_true in enumerate(unique_classes):
        for j, cls_pred in enumerate(unique_classes):
            confusion_mat[i, j] = np.sum((y_true == cls_true) & (y_pred == cls_pred))
    
    tp = np.diag(confusion_mat)
    fp = np.sum(confusion_mat, axis=0) - tp
    fn = np.sum(confusion_mat, axis=1) - tp
    tn = np.sum(confusion_mat) - (tp + fp + fn)
    
    numerator = (tp * tn) - (fp * fn)
    denominator = np.sqrt((tp + fp) * (tp + fn) * (tn + fp) * (tn + fn))
    mcc = np.mean(numerator / denominator) if np.all(denominator > 0) else 0
    return mcc

def cohens_kappa(y_true, y_pred):
    """Compute Cohen’s Kappa Score"""
    validator.validate_all(y_true, y_pred)
    unique_classes = np.unique(y_true)
    confusion_mat = np.zeros((len(unique_classes), len(unique_classes)), dtype=int)
    
    for i, cls_true in enumerate(unique_classes):
        for j, cls_pred in enumerate(unique_classes):
            confusion_mat[i, j] = np.sum((y_true == cls_true) & (y_pred == cls_pred))
    
    total = np.sum(confusion_mat)
    po = np.sum(np.diag(confusion_mat)) / total
    pe = np.sum(np.sum(confusion_mat, axis=0) * np.sum(confusion_mat, axis=1)) / (total ** 2)
    
    return (po - pe) / (1 - pe) if (1 - pe) > 0 else 0
