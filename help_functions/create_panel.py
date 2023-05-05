"""
Function that creates a panel object from a list of isolate namnes. 

Date: 27/4 
Author: Hanna Malmvall
"""

import pandas as pd
from Classes.panel_class import Panel
from help_functions.create_isolate_list import create_isolate_list

def create_panel(isolate_list: list) -> Panel:
    """ Create a Panel objects with Isolate objects from a list of isolate names. """
    CIB = pd.ExcelFile("Q-linea_files/CIB_TF-data_AllIsolates_20230302.xlsx")
    matrix_EU = pd.read_excel(CIB, "matrix EU")
    number_of_antibiotics = len(matrix_EU.columns[3:])
    isolate_objects = create_isolate_list(matrix_EU)
    chosen_isolate_objects = [
        isolate for isolate in isolate_objects if isolate.get_name() in isolate_list
    ]
    panel = Panel(number_of_antibiotics, chosen_isolate_objects)
    return panel