from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

def plot_results(results: np.ndarray) -> None:
    if len(results) % 2 != 0:
        raise ValueError("Uneven number of indices in the array")
    
    
    string_inputs = results[0::2] # even indices hold the strings
    if isinstance(string_inputs[0], str):
        string_inputs = [len(str(s)) for s in string_inputs]
    else:
        string_inputs = np.array(string_inputs, dtype=np.float64)  # Ensure numeric format
    execution_times = results[1::2] # odd indices hold the time execution
    df = pd.DataFrame({'String' : string_inputs, 'Execution Time' : execution_times})

    plt.figure(figsize=(10,6))
    sns.regplot(x="String", y="Execution Time", data=df, marker="o", line_kws={"color": "red"})
    plt.xlabel("Input Chain")
    plt.ylabel("Execution time")
    plt.title("Turing Machine Execution Time vs Input Size")
    plt.grid(True)
    plt.show()
