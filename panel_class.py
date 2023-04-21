"""
panelclass.py

Contains a class for panel objects and a sub-class for isolate objects.

Date: 20/4-23
"""


class Isolate:
    def __init__(self, name: str, antibiotics: list, sir_mic: list):
        self.name = name
        self.mic = {
            antibiotics[i]: (sir_mic[i][0], sir_mic[i][1])
            for i in range(len(antibiotics))
        }

    def get_name(self):
        return self.name

    def get_mic(self, antibiotic_name=None):
        if antibiotic_name:
            return self.mic[antibiotic_name]
        return self.mic


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
        self.hyperparameters = hyperparameters  # a list with hyperparameters to be used when constructing panel
        self.antibiotic_mic = self.create_antibiotic_mic()

    def create_antibiotic_mic(self):
        antibiotic_mic = {}
        for antibiotic in self.antibiotics:
            antibiotic_mic[antibiotic] = [
                isolate.get_mic(antibiotic)
                for isolate in self.chosen_isolates
                if None not in isolate.get_mic(antibiotic)
            ]
        return antibiotic_mic

    def spread_score(self):
        pass
        # calculate spreadead score based on self.chosen_isolates
        # return score

    def coverage_score(self):
        pass
        # calculate coverageerage score based on self.chosen_isolates
        # return score

    def redundancy_score(self):
        total_mics = 0
        redundant_mics = 0
        pass

        # calculate redundancyundance score based on self.chosen_isolates
        # eturn redundant_mics/total_mics

    def add_isolate(self):

        # Find isolate which gives minimum cost
        isolates_cost = {}
        for isolate in self.available_isolates:
            isolates_cost[isolate] = try_isolate(isolate)
            remove_isolate(isolate)

        def try_isolate(isolate):
            # Add isolates and calculate temporary scores
            self.chosen_isolates.append(isolate)
            temp_scores = [
                -self.spread_score(),
                -self.coverage_score(),
                self.redundancy_score(),
                len(self.chosen_isolates),
            ]
            # Calculate the overall cost
            cost = sum([i * j for (i, j) in zip(self.hyperparameters, temp_scores)])
            return cost

        def remove_isolate(isolate):
            self.chosen_isolates.remove(isolate)

        # Add isolate
        best_isolate = min(
            isolates_cost, key=isolates_cost.get
        )  # gives the key with the maximum value
        self.chosen_isolates.append(best_isolate)
        self.available_isolates.remove(best_isolate)

        # Update all scores
        self.spread = self.spread_score()
        self.coverage = self.coverage_score()
        self.redundancy = self.redundancy_score()
        self.antibiotic_mic = self.create_antibiotic_mic()
