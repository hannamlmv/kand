"""
Creates the redundancy plots and the uniqueness print-out

Date: 2/4
Author: Therese Björkman & Hanad Abdullahi
"""

import pandas as pd
import numpy as np
from collections import Counter
from sklearn.metrics.pairwise import cosine_similarity
import plotly.graph_objs as go
import re
import plotly.figure_factory as ff
from prettytable import PrettyTable

def read_csv(Csv_name: str):
    """ Reads the CSV file. """
    return pd.read_csv(Csv_name)

def read_the_excel(excel_name: str, sheet_name: str):
    """ Reads the excel file. """
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
    chosen_isolate = excel_sheet.loc[chosen_rows].drop(columns=["Pathogen","Source RMT","D-test"])
    return chosen_isolate

def get_antibiotic_names(excel_name: str, sheet_name: str):
    """
    Uses the function read_the_excel to read the excel file and then take 
    out the names of the antibiotics.
    """
    matrix = read_the_excel(excel_name, sheet_name)
    return list(matrix.drop(columns=["Isolate", "Pathogen","Source RMT","D-test"]).columns)

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
    SIR_category = re.findall('^[a-zA-Z]+', str(antibiotic_data[1]))
    MIC_value = ['0']

    if 'Missing BP' in antibiotic_data[1] or 'nip' in antibiotic_data[1]:
        MIC_value = ['0']
        SIR_category = ['Missing BP']
    
    elif 'nip' in antibiotic_data[1]:
        MIC_value = ['0']
        SIR_category = ['Not in panel'] 

    elif '<' in antibiotic_data[1] or '>' in antibiotic_data[1]:
        MIC_value = ['0']
        SIR_category = ['Off-scale']

    else:
        MIC_value = re.findall('(\d+\.?\d*)', str(antibiotic_data[1]))
    return(MIC_value[0], SIR_category[0])

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
        isolate_data[isolate] = [extract_antibiotic_data((antibiotic, value)) for antibiotic, value in antibiotic_data.items()]
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

def r_score(dict_with_iso: dict, excel_name: str, sheet_name: str, threshold_redundancy: int):
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
    SIR = ['S', 'I', 'R']

    for antibiotic, values in dict_with_iso.items():
        SIR_total = {category: 0 for category in SIR}
        list_val2 = []
        counts = count_values(values)
        redundant_mic_pos = 0
        non_redundant_mic_pos = 0
        for k, v in counts.items():
            if k[0] != '0':
                non_redundant_mic_pos +=1 
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

        if sum(amount_of_extra_isolates.values()) + sum(total_amount_of_isolates.values()) != 0:
            r_score = sum(amount_of_extra_isolates.values())/sum(total_amount_of_isolates.values())
        else:
            r_score = 0
    return r_score, SIR_total_per_antibiotic

# ------------------------------------------------------------------------------------------------------------
# ------------------------------------------ Visualization ---------------------------------------------------
# ------------------------------------------------------------------------------------------------------------

def heatmap_plot(isolate_data: dict, Csv_name: str, excel_name: str, sheet_name: str, plot : bool):
    """
    Takes in a dictionary containing the isolate data and uses this data to create a 
    heatmap that shows how similar each isolate is to eachother.
    """
    chosen_isolate = choose_isolates(Csv_name, excel_name, sheet_name)
    chosen_isolate_names = chosen_isolate.Isolate.values.tolist()
    worst_isolate_values = {isolate: 0 for isolate in chosen_isolate_names}
    first_values = {isolate: [float(tup[0] if tup[0] is not None else 0) for tup in isolate_data[isolate]] for isolate in chosen_isolate_names}

    
    similarity_matrix = np.zeros((len(chosen_isolate_names), len(chosen_isolate_names)))
    for i in range(len(chosen_isolate_names)):
        for j in range(len(chosen_isolate_names)):
            if i == j:
                similarity_matrix[i][j] = 1
            else:
                list1 = first_values[chosen_isolate_names[i]]
                list2 = first_values[chosen_isolate_names[j]]
                if all(val == 0 for val in (list1 + list2)):
                    similarity_matrix[i][j] = 1
                elif any(val is None for val in (list1 + list2)):
                    continue
                else:
                    cosine_similarity_val = cosine_similarity([list1, list2])[0][1]
                    similarity_matrix[i][j] = cosine_similarity_val

    fig = go.Figure(
        data=go.Heatmap(
        z=similarity_matrix,
        x=chosen_isolate_names,
        y=chosen_isolate_names,
        colorscale='mint',
        customdata=[(x, y) for x in chosen_isolate_names for y in chosen_isolate_names],
        hovertemplate='Isolat 1: %{x}<br>Isolat 2: %{y}<br>Likhet: %{z}<br>',
        zhoverformat='.2f'
    )
)

    fig.update_layout(
        title={
        'text': "Likhet mellan isolat",
        'x': 0.5,
        'xanchor': 'center',
        'font_size': 17
        },
    xaxis_title='Isolat',
    yaxis_title='Isolat',
    template="plotly_dark"
)
    if plot:
        fig.show()
    return worst_isolate_values, similarity_matrix
   
def barplot(SIR_total_per_anti, plot:bool):
    """
    Plots the bar plot containing the amounts of MIC-values that are redundant for each antibiotic. It also
    shows the amount of redundant MIC-values from each SIR-cateegory in different colors.
    """ 
    colors = {'A': 'limegreen', 'B': 'gold', 'C': 'tomato'}
    keys = list(SIR_total_per_anti.keys())
    keys = list(map(lambda x: x.replace('Trimethoprim-sulfamethoxazole', 'T.sulfamethoxazole'), keys))
    values = list(SIR_total_per_anti.values())
    S = [dict['S'] for dict in values]
    I = [dict['I'] for dict in values]
    R = [dict['R'] for dict in values]

    fig = go.Figure(data=[
        go.Bar(name='Känslig', x = keys, y = S, marker={'color': colors['A']}),
        go.Bar(name='Intermediär', x = keys, y = I, marker={'color': colors['B']}),
        go.Bar(name='Resistent', x = keys, y = R, marker ={'color': colors['C']})
    ])

    fig.update_layout(barmode='stack', template="plotly_dark" ,title={
        'text': "Antalet redundanta isolat för varje antibiotika",
        'x': 0.5,
        'xanchor': 'center',
        'font_size': 17
    }, xaxis_title = "Antibiotika", yaxis_title = "Antal isolat")
    if plot:
        fig.show()

def phylo(similarity: np.array, Csv_name: str, excel_name: str, sheet_name: str, plot:bool):
    """
    Plots a tree plot to see how closely related the isolates are when comparing their MIC-values.
    """
    chosen_isolate = choose_isolates(Csv_name, excel_name, sheet_name)
    chosen_isolate_names = chosen_isolate.Isolate.values.tolist()
    distance_matrix = 1 - similarity

    fig = ff.create_dendrogram(distance_matrix, orientation='bottom', labels=chosen_isolate_names)

    fig.update_layout(
    autosize  = True, 
    title={
        'text': "Likhet mellan isolat",
        'x': 0.5,
        'xanchor': 'center',
        'font_size': 17},
    xaxis_title='Isolat',
    yaxis_title='Distans',
    template="plotly_dark")

    if plot:
        fig.show()
     
def unique_score(isolate_selection: dict,  Antibiotic_names : list, perform:bool):
    """
    This function produces a dictionary that displays how many unique mic-values each isolate has.
    This by comparing each isolates MIC-value with every other isolates MIC-value with the same index. 
    If an isolate has a value at a specific index, that no other isolate has at the same index. 
    Then the mic-value, the region(SIR) and the name of the antibiotic is saved.
    """
    result = {}
    for key, value in isolate_selection.items():
        other_values = [l for key2, l in isolate_selection.items() if key2 != key]
        unique_tuples = [(value[i][0], value[i][1], i) for i in range(len(value)) 
                        if not any(value[i] == l[i] for l in other_values)]
        result[key] = (len(unique_tuples), unique_tuples)

    for key, value in result.items():
        new_tuple_list = []
        removed_tuple_list = []
        for tuple_item in value[1]:
            if tuple_item[1] == 'Missing bp' or tuple_item[1] == 'Off-scale' or tuple_item[1] == 'Not in panel' :
                removed_tuple_list.append((int(tuple_item[0])-1, tuple_item[1], Antibiotic_names[tuple_item[2]]))
            else:
                new_tuple_item = (tuple_item[0], tuple_item[1], Antibiotic_names[tuple_item[2]])
                new_tuple_list.append(new_tuple_item)
        result[key] = (value[0], new_tuple_list + removed_tuple_list)

    sorted_dict = dict(sorted(result.items(), key=lambda item: item[1][0]))
    table = PrettyTable()
    table.field_names = ["Isolat", "Antal unika MIC-värden", "Antibiotika (MIC-värde, SIR-kategori))"]
    table.hrules = True
    for key, value in sorted_dict.items():
        table.add_row([key, value[0], "\n".join([f"{x[2]} ({x[0]}, {x[1]})" for x in value[1]])])
    if perform:
        print(table)

def main(csv, display_barplot: bool, display_heatmap: bool, display_phylo:bool, print_unique_scores: bool):
    """The main function calls upon all the other functions and takes boolean inputs that the 
    user chooses themselves. A true means that the visualisation or print out will be performed, 
    and a false would mean that it would not be performed.
    """
    # The specified threshold for how many values that are allowed to have the same MIC-value until it is considered redundant
    threshold_redundancy = 1

    # The names of the excel file and the specific excel sheet as well as the name of the CSV-file containing the panel
    excel = "Q-linea_files/CIB_TF-data_AllIsolates_20230302.xlsx"
    excel_sheet = 'refMIC-matrix_US'

    # Here we get all the names of the isolates in the panel, this will later be used as a key
    isolate_data = create_isolate_data(csv, excel, excel_sheet,)

    # Get the MIC values for each isolate
    anti_mic_values = antibiotic_names_gets_values(csv, excel, excel_sheet)

    # Get the r-score for each antibiotic and their SIR_category
    redundancy_value, SIR_total_per_anti = r_score(anti_mic_values, excel, excel_sheet, threshold_redundancy)

    # Plot the barplot
    barplot(SIR_total_per_anti, display_barplot)

    # Plot the heatmap and get the worst isolate score???
    worst, similarity = heatmap_plot(isolate_data, csv, excel, excel_sheet, display_heatmap)

    # Plot the phylogram
    phylo(similarity, csv, excel, excel_sheet, display_phylo)
    
    #Will calculate the list of antibiotic names
    Names = get_antibiotic_names(excel,excel_sheet)
    #print out the unique score, depending on the boolean input of print_unique_scores:
    unique_score(isolate_data, Names, print_unique_scores)

if __name__ == "__main__":
   main("Chosen_isolates_folder/Chosen_isolates.csv", True, True, True, True)


