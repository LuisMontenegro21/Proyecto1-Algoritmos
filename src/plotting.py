from matplotlib import pyplot as plt
import numpy as np

def plot_results(results: list) -> None:
    string_inputs = []
    execution_times = []
    for string, result in results:
        string_inputs.append(string)
        execution_times.append(result)
    
    # turn str into int for graph
    numeric_inputs = [int(s) for s in string_inputs]
    
    coefs = np.polyfit(numeric_inputs, execution_times, 6)
    poly_d = np.poly1d(coefs)
    
    # print poly. regr.
    print("Regresión polinomial: ")
    print(poly_d)

    x_range = np.linspace(min(numeric_inputs), max(numeric_inputs), 100)
    y_fit = poly_d(x_range)

    plt.figure(figsize=(10, 6))
    plt.scatter(numeric_inputs, execution_times, marker='o', label="input")
    plt.plot(x_range, y_fit, color="red", label="Polynomial Regression")
    plt.xlabel("Input String")
    plt.ylabel("Exc. Time")
    plt.title("TM Fib vs Time Exc.")
    plt.grid(True)
    plt.legend()
    plt.show()