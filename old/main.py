import pandas as pd
from panel_class import Panel
from isolate_class import Isolate
from data_extraction_functions import *


def main():
    chosen_isolates_csv = pd.read_csv("Chosen_isolates_list.csv")
    CIB = pd.ExcelFile("Q-linea_files\CIB_TF-data_AllIsolates_20230302.xlsx")
    matrix_EU = pd.read_excel(CIB, "matrix EU")
    antibiotics = list(chosen_isolates_csv.columns[3:])

    # Extract isolates in chosen isolates csv file from excel
    chosen_isolates = extract_chosen_isolates(chosen_isolates_csv, matrix_EU)

    isolates = [
        Isolate(isolate_name, cleaned_SIR_data)
        for isolate_name, cleaned_SIR_data in extract_isolate_SIR_data(
            chosen_isolates, antibiotics
        )
    ]
    for i in isolates:
        print(i.get_mic())


if __name__ == "__main__":
    main()
