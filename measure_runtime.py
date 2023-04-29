"""
Measures runtime for creation of new panels

Date: 18/4
Author: Victor Wong
"""

import time
import matplotlib.pyplot as plt
from main import main as func


def plot_function_times(func, n_values):
    elapsed_times = []
    for n in n_values:
        start_time = time.time()
        func(n)
        end_time = time.time()
        elapsed_time = end_time - start_time
        elapsed_times.append(elapsed_time)
    plt.plot(n_values, elapsed_times)
    plt.xlabel("n")
    plt.ylabel("Elapsed time (s)")
    plt.show()


def main():
    n_values = [2, 4, 8, 16, 32, 64, 128, 256]
    plot_function_times(func, n_values)


if __name__ == "__main__":
    main()
