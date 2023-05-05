"""
An isolate class

Date: 24/4 
Author: Victor Wong and Hanna Malmvall
"""

class Isolate:
    """ An Isolate Class. """
    
    def __init__(
        self,
        isolate_name: str,
        pathogen: str,
        isolate_data: dict[tuple[float, str]],
    ) -> None:
        """ Initialize an Isolate object. """
        self.name = isolate_name
        self.pathogen = pathogen
        self.data = isolate_data

    def __str__(self) -> str:
        """ Returns a string representation of an Isolate object. """
        return self.name

    def __repr__(self) -> str:
        """ 
        Return a string representation of the Isolate object 
        that can be used to recreate the object. 
        """
        return self.name

    ### Getter methods ###
    def get_name(self) -> str:
        """ Returns the name of the Isolate object. """
        return self.name

    def get_pathogen(self) -> str:
        """ Returns the pathogen identity of the Isolate object. """
        return self.pathogen

    def get_data(self) -> dict:
        """ Returns the MIC and SIR data of the Isolate object. """
        return self.data


