import yaml
import numpy as np

def read_yaml(file_path: str):
    '''
    reads yaml input and returns the instructions 
    params: file_path str
    '''
    with open(file_path, 'r') as stream: # load the path 
        try:
            instructions = yaml.safe_load(stream=stream) # load the tokens
            return instructions
        except yaml.YAMLError as exception:
            raise exception
        
def convert_to_binary(n: int) -> np.ndarray:
    '''
    converts an integer to binary and returns it as np.ndarray
    '''
    if not isinstance(n, int): # in case no int arg was passed
        raise TypeError(f"TypeError: {n} must be type 'int', {type(n)} found instead")

    binary: str = format(n, 'b') # transform to binary str
    return np.array(list(binary)) # return a np.ndarray of the binary


# TODO not necesary
def add_tape_length(tape: np.ndarray, direction: str):
    pass

def traverse_tape(n: int, binary_num: np.ndarray, position: int, instructions: dict) -> None:
    halt_state = instructions['q_states']['final'] # get the final state


def iterate(delta: dict , tape: np.ndarray, initial_poisition: int):
    pass


def is_accepted(n: int, binary_num: np.ndarray, final_state: int, halt_state: int):
    pass

def print_instant_production(state: int, tape: np.ndarray, position: int):
    '''
    print instant productions 
    '''
    tape: np.ndarray = np.array(['B' if symbol is None else symbol for symbol in tape]) # replace None instances for Blank
    tape[position] = f'[{state}, {tape[position]}]' # change the current position for the state and position it is
    tape_content: str = ''.join(str(symbol) for symbol in tape) # join the symbols found in the current array
    print(f"\t{tape_content}") # print content currently in the tape