"""
isolate_class.py

Contains a class for isolate objects

Date: 20/4-23
"""
import pandas as pd

class Isolate:
    def __init__(self, name: str, SIR_data: list):
        self.name = name
        self.SIR_data = SIR_data

    def __str__(self) -> str:
        return f"{self.name}: {self.SIR_data}"

    def __repr__(self):
        return self.name

    def get_name(self):
        return self.name

    def get_mic(self):
        return self.SIR_data
    
    def store_MIC_SIR_data(chosen_isolates: pd.DataFrame, antibiotics:list):
        MIC_SIR_dict  {}
        for index, row in chosen_isolates.iterrows():
            isolate_name, pathogen, MIC_SIR_data_list = row[0], row[1], list(row[3:].items())
            for antibiotic, MIC_SIR_data in MIC_SIR_data_list:
                if parse_MIC_SIR(MIC_SIR_data):
                    
