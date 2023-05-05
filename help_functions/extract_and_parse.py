"""
Functions to parse antibiotic data in a cell of an 
Excel file and extract the data wanted in tuples. 

Date: 10/4 
Author: Victor Wong
"""

def parse_antibiotic_data(data: str):
    """ Checks if the data is 'nip' or Missing BP'. """
    if type(data) is not str:
        return False
    if data == "nip" or data.startswith("Missing BP"):
        return False
    return True

def extract_antibiotic_data(data: str):
    """ Returns MIC value and SIR category. If off-scale, set MIC value to None. """
    sir_category = data[0]
    if "<" in data or ">" in data:
        return (None, sir_category)
    else:
        mic_value = float(
            "".join([char for char in data if char.isdigit() or char == "."])
        )
        return (mic_value, sir_category)
