import numpy as np
import pandas as pd

class Similarity_Manager:
    @staticmethod
    def local_similarity(case1, case2):
        return np.sum(np.abs(case1.attributes[:-2] - case2.attributes[:-2]))
        
    def global_similarity(case1, case2):
        local_similarities = np.array([Similarity_Manager.local_similarity(case1, case2)])
        weighted_similarity = np.sum(local_similarities * case1.weights) / np.sum(case1.weights)
        return weighted_similarity