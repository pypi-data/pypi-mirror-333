# IQR Outlier Detection Library

This Python package helps in detecting and removing outliers from a dataset using the **Interquartile Range (IQR)** method.

## Features
- Detects outliers using IQR.
- Removes outliers from a dataset.
- Works with Pandas DataFrames and Series.

## Installation

```bash
pip install iqr-outlier
```

### Import the package:
```python
from iqr_outlier.detection import detect_outliers # Returns list with outliers
from iqr_outlier.removal import remove_outliers # Return a pandas series with outliers removed
import pandas as pd
```

### Example
```python
# Sample dataset
data = pd.Series([10, 12, 14, 15, 18, 20, 22, 24, 30, 100])

# Detect outliers
outliers = detect_outliers(data)
print("Outliers:", outliers.tolist())

# Remove outliers
cleaned_data = remove_outliers(data)
print("Cleaned Data:", cleaned_data.tolist())
```

## Project Structure
```
iqr_outliers/
│-- iqr_outlier/
│   │-- __init__.py
│   │-- detection.py
│   │-- removal.py
│-- setup.py
│-- test.py
│-- README.md
```