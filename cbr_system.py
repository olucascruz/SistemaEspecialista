import numpy as np

class CBR_System:
    def __init__(self):
        self.database = []
    
    def add_case(self, case):
        self.database.append(case)
        
    def get_database(self):
        return self.database
        
    def recover_case(self, new_case, similarity_measure):
        similarities = [similarity_measure(new_case, case)
                        for case in self.database]
        most_similar_index = np.argmin(similarities)
        return self.database[most_similar_index]