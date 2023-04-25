from panel_class import Panel


def calc_scores(panel: Panel):
    antibiotic_mic = extract_panel_data(panel)
    scores = (
        calc_spread_score(antibiotic_mic), 
        calc_coverage_score(antibiotic_mic), 
        calc_redundancy_score(antibiotic_mic)
        )

    def extract_panel_data(panel:Panel):
        panel_data = {}
        for isolate in panel.get_chosen_isolates():
            for abx, (MIC, SIR) in isolate.get_data().items():
                if abx not in panel_data:
                    panel_data[abx] = [(MIC, SIR)]
                else:
                    panel_data[abx].append((MIC, SIR))
        return panel_data

    def calc_spread_score(panel_data:dict):
        """ Calculates the spread score """
        pass

    def calc_coverage_score(panel_data:dict):
        """ Calculates the coverage score """
        coverage_score = 0
        for MIC_SIR in panel_data.values():
            number_of_mics = len(MIC_SIR)
            coverage = min(1, 0.2 * number_of_mics)
            sir_coverage = 1
            panel_SIRs = [SIR for _,SIR in MIC_SIR]
            for category, penalty in {"S": 0.3, "I": 0.2, "R": 0.4}.items():
                if category not in panel_SIRs:
                    sir_coverage -= penalty
            coverage_score += coverage * sir_coverage
        return coverage_score / len(panel_data)

    def calc_redundancy_score(panel_data:dict, redundancy_threshold = 1):
        """ Calculates the redundancy score """
        number_of_MICS = 0
        number_of_redundant_MICS = 0
        for MIC_SIR in panel_data.values():
            MIC_counter = {}
            for MIC, _ in MIC_SIR:
                number_of_MICS += 1
                if MIC not in MIC_counter:
                    MIC_counter[MIC] = 1
                else:
                    MIC_counter[MIC] += 1
                    if MIC_counter[MIC] > redundancy_threshold:
                        number_of_redundant_MICS += 1
        if number_of_MICS == 0:
            return 0
        return number_of_redundant_MICS / number_of_MICS

    
    return scores