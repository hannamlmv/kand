import pandas as pd
from extract_and_parse import extract_antibiotic_data, parse_antibiotic_data


class Isolate:
    def __init__(self, isolate_name: str, isolate_data: dict) -> None:
        self.name = isolate_name
        self.data = isolate_data

    def __repr__(self) -> str:
        return self.name

    def get_name(self):
        return self.name

    def get_data(self):
        return self.data


def create_isolate_list(matrix_EU: pd.DataFrame, antibiotics: list):
    all_isolates = []
    for _, row in matrix_EU.iterrows():
        isolate, antibiotic_data = row[0], list(row[3:].items())
        isolate_data = {}
        # Store the MIC value and SIR data for all antibiotics that are not nip or missing bp
        for antibiotic, data in zip(antibiotics, antibiotic_data):
            if parse_antibiotic_data(data):
                isolate_data[antibiotic] = extract_antibiotic_data(data)
        # Add an isolate object to all_isolates with the current isolate name and isolate_data
        all_isolates.append(Isolate(isolate, isolate_data))
    return all_isolates
