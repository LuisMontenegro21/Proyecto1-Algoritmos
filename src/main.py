from TuringMachineEmulator import *
import sys

def main():
    file_path = str(sys.argv[1]) if len(sys.argv) < 3 else None
    w: str = str(input("\nEnter string: ")) # insert Fibonacci number in this case
    w_arr, instructions = select_turing_yaml(file_path=file_path, w=w)
    traverse_tape(w=w, tape=w_arr, position=0, instructions=instructions )
    
if __name__ == '__main__':
    main()