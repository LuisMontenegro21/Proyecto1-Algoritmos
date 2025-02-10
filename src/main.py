from TuringMachineEmulator import *
import sys

def main():
    file_path = str(sys.argv[1]) if len(sys.argv) < 3 else None
    w: str = str(input("\nEnter string: ")) # insert Fibonacci number in this case
    w_arr, instructions = select_turing_yaml(file_path=file_path, w=w)
    print(f"\nCodified array: {w_arr} with type {type(w_arr)}")
    print(f"\nInstructions headlines: {instructions.keys()}")
    
if __name__ == '__main__':
    main()