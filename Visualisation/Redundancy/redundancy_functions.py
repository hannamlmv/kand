"""
Help functions for the redundancy plots

Date: 2/4
Author: Therese Björkman & Hanad Abdullahi
"""

import pandas as pd
from collections import Counter
import re


def read_csv(Csv_name: str):
    """Reads the CSV file."""
    return pd.read_csv(Csv_name)


def read_the_excel(excel_name: str, sheet_name: str):
    """Reads the excel file."""
    excel_file = pd.ExcelFile(excel_name)
    title_excel = sheet_name
    return pd.read_excel(excel_file, title_excel)


def choose_isolates(Csv_name: str, excel_name: str, sheet_name: str):
    """
    Looks at the isolates from the CSV-file and picks out these isolates
    and their MIC-values from the excel sheet.
    """
    csv = read_csv(Csv_name)
    excel_sheet = read_the_excel(excel_name, sheet_name)
    chosen_rows = excel_sheet["Isolate"].isin(csv["Isolate"])
    chosen_isolate = excel_sheet.loc[chosen_rows].drop(
        columns=["Pathogen", "Source RMT", "D-test"]
    )
    return chosen_isolate


def get_antibiotic_names(excel_name: str, sheet_name: str):
    """
    Uses the function read_the_excel to read the excel file and then take
    out the names of the antibiotics.
    """
    matrix = read_the_excel(excel_name, sheet_name)
    return list(
        matrix.drop(columns=["Isolate", "Pathogen", "Source RMT", "D-test"]).columns
    )


def antibiotic_dict(antibiotic_names: list):
    """
    Takes a list of antibiotic names and initiates a dictionary where
    the antibiotics are the keys.
    """
    return {antibiotic: [] for antibiotic in antibiotic_names}


def extract_antibiotic_data(antibiotic_data: tuple):
    """
    Takes a touple containing an the MIC-value as well as the SIR-category
    in a string for an antibiotic as well as the antibiotic name and extracts
    the SIR-category and the MIC-value respectively. If there is no MIC value
    it is set to zero and will later be sorted away. The same will be done
    if the MIC-value is Off-scale.
    """
    SIR_category = re.findall("^[a-zA-Z]+", str(antibiotic_data[1]))
    MIC_value = ["0"]

    if "Missing BP" in antibiotic_data[1] or "nip" in antibiotic_data[1]:
        MIC_value = ["0"]
        SIR_category = ["Missing BP"]

    elif "nip" in antibiotic_data[1]:
        MIC_value = ["0"]
        SIR_category = ["Not in panel"]

    elif "<" in antibiotic_data[1] or ">" in antibiotic_data[1]:
        MIC_value = ["0"]
        SIR_category = ["Off-scale"]

    else:
        MIC_value = re.findall("(\d+\.?\d*)", str(antibiotic_data[1]))
    return (MIC_value[0], SIR_category[0])


def create_isolate_data(Csv_name: str, excel_name: str, sheet_name: str):
    """
    Uses the function choose_isolates to get the wanted isolates and create a dictionary where
    the isolates are the keys and their values are all the MIC-valaues for that isolate.
    """
    chosen_isolate = choose_isolates(Csv_name, excel_name, sheet_name)
    isolate_data = {}
    for _, row in chosen_isolate.iterrows():
        isolate = row[0]
        antibiotic_data = row.iloc[1:].to_dict()
        isolate_data[isolate] = [
            extract_antibiotic_data((antibiotic, value))
            for antibiotic, value in antibiotic_data.items()
        ]
    return isolate_data


def count_values(lst: list):
    """
    A counter that is used to count the frequency of elements in a list and return a
    dictionary that maps each unique element in the list to its frequency. This will
    be used to count the R-score.
    """
    return dict(Counter(lst))


def antibiotic_names_gets_values(Csv_name: str, excel_name: str, sheet_name: str):
    """
    Creates a dictionary where the antibiotic is the key and the value includes all
    it's MIC-values and their SIR category in touples for every isolate.
    """
    isolates = choose_isolates(Csv_name, excel_name, sheet_name)
    choosen_isolate_names = isolates.Isolate.values.tolist()
    isolate_data = create_isolate_data(Csv_name, excel_name, sheet_name)
    antibiotic_names = get_antibiotic_names(excel_name, sheet_name)
    anti_dict = {antibiotic_name: [] for antibiotic_name in antibiotic_names}

    for isolate_name in choosen_isolate_names:
        isolate_data_row = isolate_data[isolate_name]
        for j, antibiotic_name in enumerate(antibiotic_names):
            anti_dict[antibiotic_name].append(isolate_data_row[j])
    return anti_dict


def r_score(
    dict_with_iso: dict, excel_name: str, sheet_name: str, threshold_redundancy: int
):
    """
    Calculates the amount of redundant MIC-values that exists for each antibiotic and categorizes these
    after the SIR-category of the MIC-value.
    """
    antibiotic_names = get_antibiotic_names(excel_name, sheet_name)
    redundant_dictionary = {antibiotic: 0 for antibiotic in antibiotic_names}
    total_mic_dictionary = {antibiotic: 0 for antibiotic in antibiotic_names}
    amount_of_extra_isolates = {antibiotic: 0 for antibiotic in antibiotic_names}
    total_amount_of_isolates = {antibiotic: 0 for antibiotic in antibiotic_names}
    SIR_total_per_antibiotic = {antibiotic: [] for antibiotic in antibiotic_names}
    list_val = {antibiotic: [] for antibiotic in antibiotic_names}
    SIR = ["S", "I", "R"]

    for antibiotic, values in dict_with_iso.items():
        SIR_total = {category: 0 for category in SIR}
        list_val2 = []
        counts = count_values(values)
        redundant_mic_pos = 0
        non_redundant_mic_pos = 0
        for k, v in counts.items():
            if k[0] != "0":
                non_redundant_mic_pos += 1
                list_val2.append(v)
                if v > threshold_redundancy:
                    list_val[antibiotic].append((v, k[1]))
                    redundant_mic_pos += 1

        sum_r = sum(pair[0] for pair in list_val[antibiotic])
        for mic, sir in list_val[antibiotic]:
            SIR_total[sir] += mic

        redundant_dictionary[antibiotic] = redundant_mic_pos
        total_mic_dictionary[antibiotic] = non_redundant_mic_pos
        amount_of_extra_isolates[antibiotic] = sum_r - redundant_mic_pos
        total_amount_of_isolates[antibiotic] = sum(list_val2)
        SIR_total_per_antibiotic[antibiotic] = SIR_total

    return SIR_total_per_antibiotic
