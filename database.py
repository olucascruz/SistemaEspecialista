import numpy as np
import pandas as pd
import json
from sklearn.preprocessing import StandardScaler

def open_csv(path):
    return pd.read_csv(path)

mineral_water_potability_cases = open_csv("./waterQuality.csv")

mineral_water_potability_cases.info()

mineral_water_potability_cases = mineral_water_potability_cases[~mineral_water_potability_cases['ammonia'].str.contains('#NUM!')]

mineral_water_potability_cases = mineral_water_potability_cases[~mineral_water_potability_cases['is_safe'].str.contains('#NUM!')]

mineral_water_potability_cases['ammonia'] = mineral_water_potability_cases['ammonia'].astype(float)

mineral_water_potability_cases['is_safe'] = mineral_water_potability_cases['is_safe'].astype(float)

positive_condition = mineral_water_potability_cases['ammonia'] < 0

mineral_water_potability_cases = mineral_water_potability_cases[~positive_condition]

mineral_water_potability_cases.info()

spearman_corelation = mineral_water_potability_cases.corr("spearman")

last_colunm_correlation = spearman_corelation.iloc[:, -1]

weights = last_colunm_correlation.head(20).to_numpy()

scaler_global = StandardScaler()
columns_to_normalize = mineral_water_potability_cases.columns[:-1]
df_norm_global = mineral_water_potability_cases

df_mean = mineral_water_potability_cases.mean()
df_std = mineral_water_potability_cases.std()

metrics_df_json_path = './metrics_df.json'

df_z_score = (mineral_water_potability_cases - df_mean) / df_std

df_norm_global[columns_to_normalize] = scaler_global.fit_transform(mineral_water_potability_cases[columns_to_normalize])

df_norm_global.to_csv("./waterQualityNormalized.csv", index=False)

weights_json_path = './weights.json'

with open(weights_json_path, 'w') as arquivo_json:
    json.dump(weights.tolist(), arquivo_json)