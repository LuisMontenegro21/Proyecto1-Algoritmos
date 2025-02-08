from TuringMachineEmulator import *
import sys

def main():
    file_path = str(sys.argv[1]) if len(sys.argv) < 3 else None
    n: int = int(input("\nEnter n-Fibonacci to calculate: "))
    binary_num : np.ndarray = convert_to_binary(n=n) # convert to binary equivalence as np.array
    stream: dict = read_yaml(file_path=file_path)
    
    
if __name__ == '__main__':
    main()