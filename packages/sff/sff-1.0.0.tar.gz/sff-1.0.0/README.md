# Feature Selection with Hybrid TFFS

## Description
The `get_list_feature_tffs_hybrid` function is used for feature selection based on high occurrence frequency during the Random Forest construction process, while also supporting integration with traditional feature selection methods.

## Syntax
```python
get_list_feature_tffs_hybrid(df, number_of_runs, n_estimators, percent, type=None, percent_hybrid=None)
```

## Parameters

| Parameter         | Data Type | Description |
|----------------|-------------|----------------------------------------------------------------|
| `df`           | `DataFrame`  | DataFrame containing input data (dependent variable in the first column). |
| `number_of_runs` | `int`       | Number of Random Forest runs to determine important feature frequencies. |
| `n_estimators`  | `int`       | Number of trees in the Random Forest. |
| `percent`       | `float`     | Percentage of features selected based on the highest occurrence frequency. |
| `type`          | `str`, optional | (Optional) Traditional feature selection method for integration. |
| `percent_hybrid`| `float`, optional | (Optional) Percentage of features retained after hybrid selection. |

## Valid Values for `type`
If `type` is used, one of the following feature selection methods can be chosen:

| `type` Value | Feature Selection Method |
|--------------|----------------------------|
| `"MI"`       | Mutual Information |
| `"PC"`       | Pearson Correlation |
| `"FS"`       | Fisher Score |
| `"BW"`       | Backward Selection |
| `"FW"`       | Forward Selection |
| `"RC"`       | Recursive Feature Elimination (RFE) |
| `"LS"`       | Lasso Regression |

## Usage

### Using Random Forest Only for Feature Selection
```python
import pandas as pd
from sff.app import get_list_feature_tffs_hybrid

# Sample DataFrame
data = {
    "Class": [0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
    "Feature1": [5, 8, 6, 7, 5, 8, 6, 7, 5, 8],
    "Feature2": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    "Feature3": [10, 20, 10, 20, 10, 20, 10, 20, 10, 20]
}
df = pd.DataFrame(data)

# Run function
selected_features = get_list_feature_tffs_hybrid(df, number_of_runs=10, n_estimators=100, percent=20)
print("Selected Features:", selected_features)
```

### Integrating with Mutual Information (MI)
```python
selected_features = get_list_feature_tffs_hybrid(df, number_of_runs=10, n_estimators=100, percent=75, type="MI", percent_hybrid=50)
print("Selected Features:", selected_features)
```

### Integrating with Recursive Feature Elimination (RFE)
```python
selected_features = get_list_feature_tffs_hybrid(df, number_of_runs=15, n_estimators=200, percent=75, type="RC", percent_hybrid=50)
print("Selected Features:", selected_features)
```

### Integrating with Mutual Information (MI) - Example Code
```python
import pandas as pd
from sff.app import get_list_feature_tffs_hybrid

# Sample DataFrame
data = {
    "Class": [0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
    "Feature1": [5, 8, 6, 7, 5, 8, 6, 7, 5, 8],
    "Feature2": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    "Feature3": [10, 20, 10, 20, 10, 20, 10, 20, 10, 20]
}
df = pd.DataFrame(data)

# Run function
selected_features = get_list_feature_tffs_hybrid(df, 5, 20, 75, "MI", 50)
print("Selected Features:", selected_features)
```

## Notes
- If `type` is not provided, the function will use only Random Forest for feature selection.
- If `type` is provided, the function will integrate Random Forest with the specified traditional method for optimal feature selection.
- `percent_hybrid` is applicable only when `type` is used.
- **Note:** `percent` (4th parameter) **must be greater than** `percent_hybrid`.
- **Note:** `df` **must have the class column as the first column**.
