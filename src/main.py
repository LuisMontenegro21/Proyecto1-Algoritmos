from TuringMachineEmulator import *
import sys

def main():
    file_path: str = str(sys.argv[1]) if len(sys.argv) < 3 else None
    multiple_strings: str = str(input("\nSimulate many strings? y/n: "))
    if multiple_strings == 'y':
        select_turing_yaml(file_path=file_path, w="", multiple_input_chains=True)
    elif multiple_strings == 'n':
        w: str = str(input("\nEnter string: ")) # insert Fibonacci number in this case
        select_turing_yaml(file_path=file_path, w=w)
    else:
        print(f"Invalid token '{multiple_strings}', 'y' or 'n' expected")
    
if __name__ == '__main__':
    main()