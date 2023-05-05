"""
A panel class

Date: 24/4 
Author: Victor Wong and Hanna Malmvall
"""

import pandas as pd
from Classes.isolate_class import Isolate

class Panel:
    """A Panel Class."""

    def __init__(
        self,
        number_of_antibiotics: int,
        chosen_isolates: list[Isolate] = [],
        spread_score: float = 0,
        coverage_score: float = 0,
        redundancy_score: float = 0,
    ) -> None:
        """Initialize a Panel object."""
        self.chosen_isolates = chosen_isolates
        self.spread_score = spread_score
        self.coverage_score = coverage_score
        self.redundancy_score = redundancy_score

        assert (
            isinstance(number_of_antibiotics, int) and number_of_antibiotics > 0
        ), "Number of antibiotics must be larger than 0"
        self.number_of_antibiotics = number_of_antibiotics

    ### Getter methods ###
    def get_chosen_isolates(self) -> list[Isolate]:
        """Returns the list of Isolate objects currently in the Panel."""
        return self.chosen_isolates

    def get_number_of_isolates(self) -> int:
        """Returns the number of Isolate objects which are in the Panel."""
        return len(self.chosen_isolates)

    def get_spread_score(self) -> float:
        """Returns the spread score of the Panel object."""
        return self.spread_score

    def get_coverage_score(self) -> float:
        """Returns the coverage score of the Panel object."""
        return self.coverage_score

    def get_redundancy_score(self) -> float:
        """Returns the redundancy score of the Panel object."""
        return self.redundancy_score

    def get_number_antibiotics(self) -> int:
        """Returns number of antibiotics of the Panel object."""
        return self.number_of_antibiotics

    def get_all_isolate_names(self) -> list[str]:
        """Returns a list of names for all isolates in the Panel object."""
        return [isolate.get_name() for isolate in self.chosen_isolates]

    def get_all_isolate_data(self) -> dict:
        """Returns a dictionary with isolate names and their data
        for all isolates in the Panel object."""
        return {
            isolate.get_name(): isolate.get_data() for isolate in self.chosen_isolates
        }

    ### Methods to add and remove isolates from the panel ###
    def append_isolate(self, isolate) -> None:
        """Adds an isolate to the list of chosen isolates."""
        self.chosen_isolates.append(isolate)

    def remove_isolate(self, isolate) -> None:
        """Removes an isolate to the list of chosen isolates."""
        self.chosen_isolates.remove(isolate)

    ### Other methods ###
    def to_csv(self, file_path: str):
        """Convert the isolates in the panel to a csv file"""
        df = pd.DataFrame(self.get_all_isolate_names(), columns=["Isolate"])
        df.to_csv(file_path, index=False)

    def to_DataFrame(self):
        """Convert the isolates in the panel to a pandas DataFrame"""
        return pd.DataFrame(self.get_all_isolate_names(), columns=["Isolate"])
