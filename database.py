import numpy as np
import pandas as pd
import json
from sklearn.preprocessing import StandardScaler

# Function to open and read a CSV file into a DataFrame
def open_csv(path):
    return pd.read_csv(path)

# Reading the original dataset from a CSV file
mineral_water_potability_cases = open_csv("./waterQuality.csv")

# Displaying information about the original dataset
mineral_water_potability_cases.info()

# Removing rows where 'ammonia' or 'is_safe' columns contain '#NUM!'
mineral_water_potability_cases = mineral_water_potability_cases[~mineral_water_potability_cases['ammonia'].str.contains('#NUM!')]
mineral_water_potability_cases = mineral_water_potability_cases[~mineral_water_potability_cases['is_safe'].str.contains('#NUM!')]

# Converting 'ammonia' and 'is_safe' columns to float
mineral_water_potability_cases['ammonia'] = mineral_water_potability_cases['ammonia'].astype(float)
mineral_water_potability_cases['is_safe'] = mineral_water_potability_cases['is_safe'].astype(float)

# Removing rows where 'ammonia' is less than 0
positive_condition = mineral_water_potability_cases['ammonia'] < 0
mineral_water_potability_cases = mineral_water_potability_cases[~positive_condition]

# Displaying information about the cleaned dataset
mineral_water_potability_cases.info()

# Calculating Spearman correlation and extracting the correlation values for the last column
spearman_correlation = mineral_water_potability_cases.corr("spearman")
last_column_correlation = spearman_correlation.iloc[:, -1]

# Extracting the top 20 correlation values as weights
weights = last_column_correlation.head(20).to_numpy()

# Initializing a StandardScaler for normalization
scaler_global = StandardScaler()

# Selecting columns for normalization (excluding the last column)
columns_to_normalize = mineral_water_potability_cases.columns[:-1]

# Creating a new DataFrame for normalized data
df_norm_global = mineral_water_potability_cases

# Calculating mean and standard deviation for normalization
df_mean = mineral_water_potability_cases.mean()
df_std = mineral_water_potability_cases.std()

# Creating a dictionary to store mean, standard deviation, and weights
metrics_info = {
    'df_mean': df_mean[:-1].to_dict(),
    'df_std': df_std[:-1].to_dict(),
    'weights': weights.tolist()
}

# Calculating Z-score normalization for the dataset
df_z_score = (mineral_water_potability_cases - df_mean) / df_std

# Normalizing selected columns using StandardScaler
df_norm_global[columns_to_normalize] = scaler_global.fit_transform(mineral_water_potability_cases[columns_to_normalize])

# Writing the normalized dataset to a new CSV file
df_norm_global.to_csv("./waterQualityNormalized.csv", index=False)

# Saving the metrics information (mean, std, weights) to a JSON file
metrics_json_path = './metrics.json'
with open(metrics_json_path, 'w') as json_file:
    json.dump(metrics_info, json_file)
