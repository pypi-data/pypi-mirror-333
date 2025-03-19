# Moral88
A Python library for regression evaluation metrics.

## Installation
To use the library, simply clone the repository and add it to your project.

## Overview 🚀
`Moral88` is a Python library providing **robust, optimized, and flexible** implementations of **regression and segmentation metrics** for machine learning, deep learning, and data science applications. It supports:

- **Multiple Libraries** (`Moral88`, `sklearn`, `torch`, `tensorflow`)
- **GPU Acceleration** (`torch.cuda`, `tensorflow-GPU`)
- **Flexible Input Formats** (`numpy`, `pandas`, `torch.Tensor`, `tensorflow.Tensor`)
- **Error Handling & Validation** (Ensures data integrity)

## Installation 📦
Install via `pip`:
```bash
pip install Moral88
```

## Usage 💡
Import `Moral88` metrics easily:
```python
from Moral88.regression import mean_absolute_error, r2_score
from Moral88.segmentation import dice_coefficient, jaccard_index
```

### 1️⃣ **Regression Metrics**
#### Mean Absolute Error (MAE)
```python
import numpy as np
from Moral88.regression import mean_absolute_error

y_true = [3, -0.5, 2, 7]
y_pred = [2.5, 0.0, 2, 8]
mae = mean_absolute_error(y_true, y_pred, library='sklearn')
print("MAE:", mae)
```

#### Mean Squared Error (MSE)
```python
from Moral88.regression import mean_squared_error
mse = mean_squared_error(y_true, y_pred, library='torch')
print("MSE:", mse)
```

#### Root Mean Squared Error (RMSE)
```python
from Moral88.regression import root_mean_squared_error
rmse = root_mean_squared_error(y_true, y_pred, library='tensorflow')
print("RMSE:", rmse)
```

#### R-Squared (R²) Score
```python
from Moral88.regression import r2_score
r2 = r2_score(y_true, y_pred, library='statsmodels')
print("R2 Score:", r2)
```

#### Adjusted R-Squared Score
```python
from Moral88.regression import adjusted_r2_score
adj_r2 = adjusted_r2_score(y_true, y_pred, n_features=2, library='Moral88')
print("Adjusted R2:", adj_r2)
```

#### Mean Absolute Percentage Error (MAPE)
```python
from Moral88.regression import mean_absolute_percentage_error
mape = mean_absolute_percentage_error(y_true, y_pred, library='sklearn')
print("MAPE:", mape)
```

#### Huber Loss
```python
from Moral88.regression import huber_loss
huber = huber_loss(y_true, y_pred, delta=1.0, library='torch')
print("Huber Loss:", huber)
```

### 2️⃣ **Segmentation Metrics**
#### Dice Coefficient
```python
import numpy as np
from Moral88.segmentation import dice_coefficient

y_true_mask = np.array([[1, 1, 0], [0, 1, 1], [1, 0, 0]])
y_pred_mask = np.array([[1, 0, 0], [1, 1, 1], [1, 0, 1]])

dice = dice_coefficient(y_true_mask, y_pred_mask, library='torch')
print("Dice Coefficient:", dice)
```

#### Jaccard Index (IoU)
```python
from Moral88.segmentation import jaccard_index
jaccard = jaccard_index(y_true_mask, y_pred_mask, library='tensorflow')
print("Jaccard Index:", jaccard)
```

#### Hausdorff Distance
```python
from Moral88.segmentation import hausdorff_distance
hausdorff = hausdorff_distance(y_true_mask, y_pred_mask, library='Moral88')
print("Hausdorff Distance:", hausdorff)
```

#### F1 Score for Segmentation
```python
from Moral88.segmentation import f1_score
f1 = f1_score(y_true_mask, y_pred_mask, library='sklearn')
print("F1 Score:", f1)
```

### 3️⃣ **Advanced Features**
- **GPU Acceleration** 🚀
```python
import torch

y_true_tensor = torch.tensor(y_true, device='cuda')
y_pred_tensor = torch.tensor(y_pred, device='cuda')
mae_gpu = mean_absolute_error(y_true_tensor, y_pred_tensor, library='torch')
print("MAE (GPU):", mae_gpu)
```

- **Handling Different Input Formats** ✅
```python
import pandas as pd

df = pd.DataFrame({"y_true": y_true, "y_pred": y_pred})
mae_df = mean_absolute_error(df["y_true"], df["y_pred"], library='Moral88')
print("MAE (Pandas DataFrame):", mae_df)
```

## **Contributing 🤝**
Feel free to contribute to `Moral88` by submitting pull requests or opening issues! 🙌

## **License 📜**
`Moral88` is licensed under the **MIT License**.

---
🚀 **Happy Coding with Moral88!** 🚀

