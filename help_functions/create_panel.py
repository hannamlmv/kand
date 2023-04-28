"""
Function that creates a panel object from a list of isolate namnes. 
"""
import pandas as pd
from Classes.panel_class import Panel
from Classes.isolate_class import create_isolate_list


def create_panel(isolate_list: list):
    CIB = pd.ExcelFile("Q-linea_files/CIB_TF-data_AllIsolates_20230302.xlsx")
    matrix_EU = pd.read_excel(CIB, "matrix EU")
    number_of_antibiotics = len(matrix_EU.columns[3:])
    isolate_objects = create_isolate_list(matrix_EU)
    chosen_isolate_objects = [
        isolate for isolate in isolate_objects if isolate.get_name() in isolate_list
    ]
    panel = Panel(number_of_antibiotics, chosen_isolate_objects)
    return panel