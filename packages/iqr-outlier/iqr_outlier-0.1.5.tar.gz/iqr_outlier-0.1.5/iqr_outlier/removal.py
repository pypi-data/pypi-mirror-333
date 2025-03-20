import pandas as pd
import numpy as np

def remove_outliers(data):
    """Remove outliers from dataset using IQR method.
        Returns a pandas series """

    if isinstance(data, list):
        data = pd.Series(data)

    Q1 = np.percentile(data,25)
    Q3 = np.percentile(data,75)

    IQR = Q3 - Q1

    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    cleaned_data = data[(data >= lower_bound) & (data <= upper_bound)]
    return cleaned_data