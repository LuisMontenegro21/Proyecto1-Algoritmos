from TuringMachineEmulator import *
import sys

def main():
    file_path = str(sys.argv[1]) if len(sys.argv) < 3 else None
    w: str = str(input("\nEnter string: ")) # insert Fibonacci number in this case
    select_turing_yaml(file_path=file_path, w=w)

    
if __name__ == '__main__':
    main()