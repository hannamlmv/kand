import time
import matplotlib.pyplot as plt
from main import main


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


if __name__ == "__main__":
    plot_function_times(main, [2 * i for i in range(6, 13)])
