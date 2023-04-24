from isolate_class import Isolate


class Panel:
    def __init__(
        self,
        chosen_isolates: list(Isolate) = [],
        spread_score: float = 0,
        coverage_score: float = 0,
        redundancy_score: float = 0,
    ) -> None:
        self.chosen_isolates = chosen_isolates
        self.spread_score = spread_score
        self.coverage_score = coverage_score
        self.redundancy_score = redundancy_score

    def get_chosen_isolates(self):
        return self.chosen_isolates

    def get_spread_score(self):
        return self.spread_score

    def get_coverage_score(self):
        return self.coverage_score

    def get_redundancy_score(self):
        return self.redundancy_score

    def get_all_isolate_names(self):
        return [isolate.get_name() for isolate in self.chosen_isolates]

    def append_isolate(self, isolate):
        self.chosen_isolates.append(isolate)

    def remove_isolate(self, isolate):
        self.chosen_isolates.remove(isolate)
