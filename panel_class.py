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

    def get_chosen_isolates(self) -> list(Isolate):
        return self.chosen_isolates

    def get_number_of_isolates(self) -> int:
        return len(self.chosen_isolates)

    def get_spread_score(self) -> float:
        return self.spread_score

    def get_coverage_score(self) -> float:
        return self.coverage_score

    def get_redundancy_score(self) -> float:
        return self.redundancy_score

    def get_all_isolate_names(self) -> list(str):
        return [isolate.get_name() for isolate in self.chosen_isolates]

    def get_all_isolate_data(self) -> dict:
        return {
            isolate.get_name(): isolate.get_data() for isolate in self.chosen_isolates
        }

    def append_isolate(self, isolate) -> None:
        self.chosen_isolates.append(isolate)

    def remove_isolate(self, isolate) -> None:
        self.chosen_isolates.remove(isolate)
