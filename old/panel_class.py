"""
panel_class.py

Contains a class for panel objects

Date: 20/4-23
"""

from collections import Counter


class Panel:
    def __init__(
        self,
        available_isolates: list,
        antibiotics: list,
        chosen_isolates: list = [],
        hyperparameters: list = [1, 1, 1, 1],
    ):
        self.available_isolates = available_isolates
        self.chosen_isolates = chosen_isolates
        self.antibiotics = antibiotics
        self.spread = self.spread_score()
        self.coverage = self.coverage_score()
        self.redundancy = self.redundancy_score()
        self.hyperparameters = hyperparameters
        self.antibiotic_mic = self.create_antibiotic_mic()

    def create_antibiotic_mic(self):
        """ Gives a dictionary containing the mic-values present
        on the panel for each antibiotic"""
        antibiotic_mic = {}
        for antibiotic in self.antibiotics:
            antibiotic_mic[antibiotic] = [
                isolate.get_mic(antibiotic)
                for isolate in self.chosen_isolates
                if None not in isolate.get_mic(antibiotic)
            ]
        return antibiotic_mic

    def spread_score(self):
        """ " Calculates the spread score"""
        
        total_concentration_range = [
            "Min C",
            0.00195,
            0.00391,
            0.00781,
            0.01563,
            0.03125,
            0.0625,
            0.125,
            0.25,
            0.5,
            1.0,
            2.0,
            4.0,
            8.0,
            16.0,
            32.0,
            64.0,
            128.0,
            256.0,
            512.0,
            1024.0,
            "Max C",
        ]

        def count_gap_length(valid_list: list) -> float:
            total_gap_length = 0
            gap_length = 0

            for value in valid_list:
                if value == 0:
                    gap_length += 1
                else:  # if current value == 1
                    if gap_length >= 2:
                        total_gap_length += gap_length - 1
                    gap_length = 0
            # If the last values were also 0s and the gap length is at least 2.
            # Add the length of the gap to the total gap length
            if gap_length >= 2:
                total_gap_length += gap_length - 1
            return total_gap_length


        def check_edges(valid_list: list) -> float:
            edge_penalty = 0

            # Add 0.5 penalty if the edge values are empty.
            if valid_list[0] == 0:  # Check first value
                edge_penalty += 0.5
            if valid_list[-1] == 0:  # Check last value
                edge_penalty += 0.5

            return edge_penalty
        spread_scores = []
        for antibiotic in self.antibiotics:
            mic_values = self.antibiotic_mic[antibiotic]
            for i in mic_values:
                
        pass
        # return score

    def coverage_score(self):
        """ " Calculates the coverage score"""
        coverage_scores = []
        for antibiotic in self.antibiotics:
            number_of_mics = len(self.antibiotic_mic[antibiotic])
            coverage = 0.2 * number_of_mics
            if coverage > 1:
                coverage = 1
            sir_coverage = 1
            for category, penalty in {"S": 0.3, "I": 0.2, "R": 0.4}.items():
                if category not in [
                    self.antibiotic_mic[antibiotic][i][1]
                    for i in range(len(self.antibiotic_mic[antibiotic]))
                ]:
                    sir_coverage -= penalty
            coverage_scores.append(coverage * sir_coverage)
        return sum(coverage_scores) / len(coverage_scores)

    def redundancy_score(self):
        """ " Calculates the redundancy score"""
        total_mics = 0
        redundant_mics = 0
        for antibiotic in self.antibiotics:
            total_mics += len(self.antibiotic_mic[antibiotic])
            count_mics = dict(
                Counter(mic_sir[0])
                for mic_sir in self.create_antibiotic_mic()[antibiotic]
            )
            redundant_mics += sum(
                number - 1 for number in count_mics.values() if number > 1
            )
        if total_mics == 0:
            return 0
        else:
            return redundant_mics / total_mics

    def add_isolate(self):
        """ " Adds one isolate to give the optimal panel"""
        # Find isolate which gives minimum cost
        isolates_cost = {}
        for isolate in self.available_isolates:
            isolates_cost[isolate] = try_isolate(isolate)

        def try_isolate(isolate):
            """ " Investigates which isolate gives the optimal panel"""
            # Add isolates and calculate temporary scores
            self.chosen_isolates.append(isolate)
            temp_scores = [
                -self.spread_score(),
                -self.coverage_score(),
                self.redundancy_score(),
                len(self.chosen_isolates),
            ]
            self.chosen_isolates.remove(isolate)
            # Calculate the overall cost
            cost = sum([i * j for (i, j) in zip(self.hyperparameters, temp_scores)])
            return cost

        # Add isolate
        best_isolate = min(isolates_cost, key=isolates_cost.get)
        self.chosen_isolates.append(best_isolate)
        self.available_isolates.remove(best_isolate)

        # Update all scores
        self.spread = self.spread_score()
        self.coverage = self.coverage_score()
        self.redundancy = self.redundancy_score()
        self.antibiotic_mic = self.create_antibiotic_mic()