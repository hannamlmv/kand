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
        pass


    def calc_coverage_score(panel_data:dict):
        pass


    def calc_redundancy_score(panel_data:dict):
        pass

    
    return scores