import json


def main():
    visualisation_settings_file_path = "visualisation_settings.json"
    visualisation_settings = json.load(open(visualisation_settings_file_path))

    for plot, show in visualisation_settings.items():
        pass
