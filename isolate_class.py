class Isolate:
    def __init__(self, name: str, SIR_data: list):
        self.name = name
        self.SIR_data = SIR_data

    def __str__(self) -> str:
        return f"{self.name}: {self.SIR_data}"

    def __repr__(self):
        return self.name

    def get_name(self):
        return self.name

    def get_mic(self):
        return self.SIR_data
