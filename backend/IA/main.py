import json
import numpy as np
import pandas as pd
from .cbr_system import CBR_System
from .similarity_manager import Similarity_Manager
from .water_mineral_sample_case import Water_Mineral_Sample_Case
from os import path

def IA(data):
    # Reading the globally normalized DataFrame from a CSV file
    path_dir = path.abspath(path.dirname(__file__))
    df_norm_global = pd.read_csv(path.join(path_dir, r'waterQualityNormalized.csv'))

    # Loading metrics from a JSON file, including weights, df_mean, and df_std
    with open(path.join(path_dir, r"metrics.json"), 'r') as json_file:
        metrics_loaded = json.load(json_file)

    weights = np.array(metrics_loaded['weights'])
    df_mean_dict = metrics_loaded['df_mean']
    df_std_dict = metrics_loaded['df_std']

    # Converting dictionaries to pandas Series
    df_mean = pd.Series(df_mean_dict)
    df_std = pd.Series(df_std_dict)

    # Initializing a Case-Based Reasoning (CBR) system
    cbr_system = CBR_System()

    # Adding cases from the normalized DataFrame to the CBR system
    for index, row in df_norm_global.iterrows():
        case = Water_Mineral_Sample_Case(description="Case" + str(index),
                                        attributes=row.values[:-1],
                                        weights=weights,
                                        potability_status=row['is_safe'])
        cbr_system.add_case(case)

    # Generating random and predefined test cases for evaluation
    database_length = cbr_system.database.count
    
    # Normalizing the attributes of the test cases
    normalized_attributes = (np.array(data) - df_mean) / df_std
    
    # Creating new Water_Mineral_Sample_Case instances for the test cases
    new_case = Water_Mineral_Sample_Case(description="Case" + str(database_length),
                                        attributes=normalized_attributes,
                                        weights=weights,
                                        potability_status=0)

    
    # Recovering cases using the CBR system based on similarity
    recovered_case = cbr_system.recover_case(new_case, Similarity_Manager.global_similarity)
    

    # Updating potability status based on recovered cases and adding new cases to the CBR system
    new_case.update_potability_status(potability_status=recovered_case.potability_status)
    cbr_system.add_case(new_case)

    # Printing the results for the randomly generated case
    print("Recovered Case:", recovered_case.description, "\nIs Safe ?", "True" if recovered_case.potability_status == 1 else "False")

    # Printing the results for the predefined safe case
    print("Recovered Safe Case:", recovered_case.description, "\nIs Safe ?", "True" if recovered_case.potability_status == 1 else "False")
    return recovered_case.potability_status 