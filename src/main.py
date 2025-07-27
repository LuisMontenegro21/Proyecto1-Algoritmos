from TuringMachineEmulator import select_turing_yaml
import os

def main():
    path_dict:dict = {}
    path_: str = "src/instructions"
    
    for i, dir in enumerate(os.listdir(path_)):
        path_dict[i+1] = os.path.join(path_, dir)
        print(f"{i+1} - {dir}")

    index: int = int(input("Select path number of the Turing Machine:"))
    file_path: str = path_dict.get(index, None)
    if file_path:
        multiple_strings: str = str(input("\nSimulate many strings? y/n: "))
        if multiple_strings == 'y':
            select_turing_yaml(file_path=file_path, w="", multiple_input_chains=True)
        elif multiple_strings == 'n':
            w: str = str(input("\nEnter string: ")) # insert Fibonacci number in this case
            select_turing_yaml(file_path=file_path, w=w)
        else:
            print(f"Invalid token '{multiple_strings}', 'y' or 'n' expected")
    else:
        print(f"No path found for index '{index}'")    
if __name__ == '__main__':
    main()