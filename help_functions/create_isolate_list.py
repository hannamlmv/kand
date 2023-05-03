"""
Creates a list of isolates from a dataframe

Date: 25/4 
Author: Victor Wong
"""

import pandas as pd
from help_functions.extract_and_parse import parse_antibiotic_data, extract_antibiotic_data
from Classes.isolate_class import Isolate


def create_isolate_list(matrix_EU: pd.DataFrame) -> list[Isolate]:
    all_isolates = []
    for _, row in matrix_EU.iterrows():
        isolate, pathogen, antibiotic_data = row[0], row[1], list(row[3:].items())
        if " " in isolate:
            break
        isolate_data = {}
        # Store the MIC value and SIR data for all antibiotics that are not nip or missing bp
        for antibiotic, data in antibiotic_data:
            if parse_antibiotic_data(data):
                isolate_data[antibiotic] = extract_antibiotic_data(data)
        # Add an isolate object to all_isolates with the current isolate name and isolate_data
        all_isolates.append(Isolate(isolate, pathogen, isolate_data))
    return all_isolates