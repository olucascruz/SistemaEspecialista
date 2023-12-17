import json
import numpy as np
import pandas as pd
from cbr_system import CBR_System
from similarity_manager import Similarity_Manager
from water_mineral_sample_case import Water_Mineral_Sample_Case

if __name__ == '__main__':

    df_norm_global = pd.read_csv('.\waterQualityNormalized.csv')

    with open('./weights.json', 'r') as arquivo_json:
        lista_carregada = json.load(arquivo_json)

    weights = np.array(lista_carregada)

    cbr_system = CBR_System()

    for index, row in df_norm_global.iterrows():
        case = Water_Mineral_Sample_Case(description="Case" + str(index),
                                        attributes=row.values[:-1],
                                        weights=weights,
                                        potability_status=row['is_safe'])
        cbr_system.add_case(case)

    new_case = Water_Mineral_Sample_Case(description="CaseX",
                                        attributes=np.random.uniform(-1, 1, 20),
                                        weights=weights,
                                        potability_status=0)

    recovered_case = cbr_system.recover_case(new_case, Similarity_Manager.global_similarity)
    
    print("Caso Recuperado:", recovered_case.description, "\nIs Safe ?", "True" if recovered_case.potability_status == 1 else "False")