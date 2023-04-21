"""
isolate_cqlass.py

Contains a class for isolate objects

Date: 20/4-23
"""


class Isolate:
    def __init__(self, name: str, antibiotics: list, sir_mic: list):
        self.name = name
        self.mic = {
            antibiotic: (
                (MIC_value, SIR_category) for MIC_value, SIR_category in sir_mic
            )
            for antibiotic in antibiotics
        }

    def __str__(self) -> str:
        return f"{self.name}: {self.mic}"

    def __repr__(self):
        return self.name

    def get_name(self):
        return self.name

    def get_mic(self, antibiotic_name=None):
        if antibiotic_name:
            return self.mic[antibiotic_name]
        return self.mic
