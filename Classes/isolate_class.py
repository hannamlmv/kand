"""
An isolate class

Date: 24/4 
Author: Victor Wong and Hanna Malmvall
"""

import pandas as pd
from help_functions.extract_and_parse import (
    extract_antibiotic_data,
    parse_antibiotic_data,
)


class Isolate:
    def __init__(
        self,
        isolate_name: str,
        pathogen: str,
        isolate_data: dict[tuple[float, str]],
    ) -> None:
        self.name = isolate_name
        self.pathogen = pathogen
        self.data = isolate_data

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return self.name

    def get_name(self) -> str:
        return self.name

    def get_pathogen(self) -> str:
        return self.pathogen

    def get_data(self) -> dict:
        return self.data


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
