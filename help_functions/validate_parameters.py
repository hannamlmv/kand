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


def validate_coverage_demands(coverage_demands: dict[str:float]) -> None:
    """
    Checks to see if the coverage_demands dictionary contains
    correct data types and if the demands are greater than 0
    """
    if not isinstance(coverage_demands, dict):
        raise TypeError("Coverage demands must be a dictionary.")
    demand_sum = 0
    for sir_category, demand in coverage_demands.items():
        if not isinstance(sir_category, str) or sir_category not in ["S", "I", "R"]:
            raise ValueError(
                "Key in coverage demands must be one of strings: 'S', 'I' or 'R'."
            )
        if not isinstance(demand, int) or demand < 0:
            raise ValueError("Demand value must be an int greater or equal to than 0.")
        demand_sum += demand
    if demand_sum == 0:
        raise ValueError("Sum of demand values can not be 0.")

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

    coverage_demands = parameters["Coverage demands"]
    validate_coverage_demands(coverage_demands)

    redundancy_threshold = parameters["Redundancy threshold"]
    validate_redundancy_threshold(redundancy_threshold)

    coefficients_array = np.array(
        [coefficient for _, coefficient in coefficients.items()]
    )

    return (
        number_of_isolates,
        coefficients_array,
        coverage_demands,
        redundancy_threshold,
    )
