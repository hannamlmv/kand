class Isolate:
    def __init__(self, isolate_name, isolate_data) -> None:
        self.name = isolate_name
        self.data = isolate_data

    def __repr__(self) -> str:
        return self.name

    def get_name(self):
        return self.name

    def get_data(self):
        return self.data
