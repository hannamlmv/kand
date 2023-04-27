import numpy as np


def validate_number_of_isolates(number_of_isolates: int) -> None:
    """
    Validate number of isolates. Must be integer greater than or equal to 1
    """
    if not isinstance(number_of_isolates, int) or number_of_isolates < 1:
        raise ValueError(
            "Number of isolates must be an integer greater than or equal to 1."
        )


def validate_coefficients(coefficients: dict[str:float]) -> None:
    """
    Validate coefficients. Must be dictionary with str as key and float as value
    """
    if not isinstance(coefficients, dict):
        raise TypeError("Coefficients must be a dictionary.")
    for name, coefficient in coefficients.items():
        if not isinstance(name, str) or name not in [
            "Spread",
            "Coverage",
            "Redundancy",
        ]:
            raise ValueError(
                "Key in coefficients must be one of strings: 'Spread', 'Coverage' or 'Redundancy'."
            )
        if not isinstance(coefficient, float) or coefficient < 0:
            raise ValueError("Coefficient values must be floats greater than 0.")


def validate_coverage_penalties(coverage_penalties: dict[str:float]) -> None:
    """
    Checks to see if the coverage_penalties dictionary contains
    correct data types and if the penalties add up to 1
    """
    if not isinstance(coverage_penalties, dict):
        raise TypeError("Coverage penalties must be a dictionary.")
    penalty_sum = 0
    for sir_category, penalty in coverage_penalties:
        if not isinstance(sir_category, str) or sir_category not in ["S", "I", "R"]:
            raise ValueError(
                "Key in coverage penalties must be one of strings: 'S', 'I' or 'R'."
            )
        if not isinstance(penalty, float) or penalty > 1 or penalty < 0:
            raise ValueError("Penalty value must be a float between 0 and 1.")
        penalty_sum += penalty_sum
    if penalty_sum != 1:
        raise ValueError("Sum of penalties must be equal to 1.")


def validate_redundancy_threshold(redundancy_threshold: int) -> None:
    if not isinstance(redundancy_threshold, int) or redundancy_threshold < 1:
        raise ValueError(
            "Redundancy threshold must be an integer greater or equal to 1."
        )


def validate_parameters(
    parameters: dict,
) -> dict[str : int | float | dict[str:float]]:
    """
    Parses the parameters and checks if the inputs are of correct data type and values.
    """
    number_of_isolates = parameters["Number of isolates"]
    validate_number_of_isolates(number_of_isolates)

    coefficients = parameters["Coefficients"]
    validate_coefficients(coefficients)

    coverage_penalties = parameters["Coverage penalties"]
    validate_coverage_penalties(coverage_penalties)

    redundancy_threshold = parameters["Redundancy threshold"]
    validate_redundancy_threshold(redundancy_threshold)

    coefficients = np.array((coefficient for _, coefficient in coefficients))

    return (number_of_isolates, coefficients, coverage_penalties, redundancy_threshold)
