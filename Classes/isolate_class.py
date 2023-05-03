"""
An isolate class

Date: 24/4 
Author: Victor Wong and Hanna Malmvall
"""


class Isolate:
    def __init__(
        self,
        isolate_name: str,
        pathogen: str,
        isolate_data: dict[tuple[float, str]],
    ) -> None:
        self.name = isolate_name
        self.pathogen = pathogen
        self.data = isolate_data

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return self.name

    ### Getter methods ###
    def get_name(self) -> str:
        return self.name

    def get_pathogen(self) -> str:
        return self.pathogen

    def get_data(self) -> dict:
        return self.data

