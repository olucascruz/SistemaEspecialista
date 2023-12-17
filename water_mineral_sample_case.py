import numpy as np

class Water_Mineral_Sample_Case:
    def __init__(self, description, attributes, weights, potability_status):
        self.description = description
        self.attributes = np.array(attributes)
        self.weights = np.array(weights)
        self.potability_status = potability_status

    def update_potability_status(self, potability_status):
        self.potability_status = potability_status