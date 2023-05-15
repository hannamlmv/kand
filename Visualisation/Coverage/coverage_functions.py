"""
Help functions to create the coverage plots

Date: 2/4
Author: Elin Berg & Julia Ancker
"""

import pandas as pd

def parse_SIR(SIR: str) -> bool:
   """
   Find the isolates with valid SIRs. Not 'Missing BP'
   and not 'nip'.
   """
   if SIR.startswith("Missing BP"):
       return False
   if SIR == "nip":
       return False
   return True

def extract_SIR(chosen_isolates: pd.DataFrame, antibiotics: list) -> dict:
   """
   Extract all SIRs for an antibiotic. Returns a dictionary
   with antibiotcs as keys and lists of the isolates and their
   SIRs in tuples as value.
   """
   chosen_isolates_SIR = {antibiotic: [] for antibiotic in antibiotics}
  
   for index, row in chosen_isolates.iterrows():
       antibiotic_SIR = list(row[3:].items())
       for antibiotic, SIR in antibiotic_SIR:
           if parse_SIR(SIR):
               mic_category = SIR[0]
               chosen_isolates_SIR[antibiotic].append(mic_category)
           else:
               chosen_isolates_SIR[antibiotic].append((None))
   return chosen_isolates_SIR

def extract_SIR_M(chosen_isolates: pd.DataFrame, antibiotics: list) -> dict:
   """
   Extract all SIRs for an antibiotic. Returns a dictionary
   with antibiotcs as keys and lists of the isolates and their
   SIRs in tuples as value, M if there is a missing MIC-value.
   """
   chosen_isolates_SIR = {antibiotic: [] for antibiotic in antibiotics}
  
   for index, row in chosen_isolates.iterrows():
       antibiotic_SIR = list(row[3:].items())
       for antibiotic, SIR in antibiotic_SIR:
           if parse_SIR(SIR):
               mic_category = SIR[0]
               chosen_isolates_SIR[antibiotic].append(mic_category)
           else:
               chosen_isolates_SIR[antibiotic].append(('M'))
   return chosen_isolates_SIR

def filter_mic_values(chosen_isolates_SIR: dict) -> None:
   """ Remove the tuples that have None in their SIR data. """
   for antibiotic, SIR_data in chosen_isolates_SIR.items():
       chosen_isolates_SIR[antibiotic] = list((tup for tup in SIR_data if tup is not None))
   return chosen_isolates_SIR

def collect_number_of_S_I_R(chosen_isolates_SIR: dict) -> dict:
    """
    Counts every S,I,R value for every antibiotic. Returns a dictionary with the 
    antibiotic as the key, and a list with hte counts of the S,I,R-values 
    (in that order).
    """
    count_isolates_SIR={}
    for antibiotic, SIR_data in chosen_isolates_SIR.items():
        S_count=0
        I_count=0
        R_count=0
        
        for SIR in SIR_data:
            if SIR=='S':
                S_count+=1
            if SIR=='I':
                I_count+=1
            if SIR=='R':
                R_count+=1

        count_isolates_SIR[antibiotic]=  list((S_count, I_count, R_count))
    return count_isolates_SIR
