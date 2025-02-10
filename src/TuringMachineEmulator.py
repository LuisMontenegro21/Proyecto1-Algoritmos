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
        
def convert_to_array(w: str, binary_encoding: bool=False) -> np.ndarray:
    '''
    converts the chain to list and returns it as np.ndarray.
    optionally codifies the input chain to binary
    '''
    if not isinstance(w, str): # in case no str arg was passed
        raise TypeError(f"TypeError: {w} must be type 'str', {type(w)} found instead")

    if binary_encoding and w.isdigit():
        binary: str = format(w, 'b') # transform to binary str
        chain_null : list = [None] + list(binary) + [None] # add null to both ends
        return np.array(chain_null) # return a np.ndarray of the binary
    else:
        chain_null: list = [None] + list(w) + [None] # if no binary needed, return as a np.ndarray
        return np.array(chain_null)
  
def select_turing_yaml(file_path: str, w: str) -> tuple[np.ndarray, dict]:
    '''
    Selects which yaml to use and checks if it needs a binary codification or not
    '''
    instructions: dict = read_yaml(file_path=file_path)
    if instructions['binary_cod']['binary'] == 'y':
        arr: np.ndarray = convert_to_array(w=w, binary_encoding=True) # if Fibonacci, needs to be encoded 
        return arr, instructions
    else:
        arr: np.ndarray = convert_to_array(w=w) # if Fibonacci, needs to be encoded 
        return arr, instructions


def traverse_tape(w: str, tape: np.ndarray, position: int, instructions: dict) -> None:
    halt_state = instructions['q_states']['final'] # get the final state

    delta_dict = {} # gather only the transitions
    for index, entry in enumerate(instructions['delta']):
        delta_dict[index] = {'params': entry['params'], 'output': entry['output']}
    
    final_tape, final_tape_state = iterate(delta=delta_dict, tape=tape, initial_poisition=position)
    is_accepted(w=w, tape=final_tape, final_state=final_tape_state, halt_state=halt_state)


def iterate(delta: dict , tape: np.ndarray, initial_poisition: int) -> tuple[np.ndarray, int]:
    position: int = initial_poisition # define initial position
    current_state = delta[0]['params']['initial_state'] # define initial state
    while True:
        current_symbol = tape[position] if position < len(tape) else None
        transition = None
        # search for appropiate transition 
        for key, value in delta.items():
            if value['params']['initial_state'] == current_state and value['params']['tape_input'] == current_symbol:
                transition = value
                break
        # if no transition found, break
        if transition is None:
            break
        
        # update the tape
        if transition['output']['tape_output'] is not None:
            tape[position] = transition['output']['tape_output']

        # move throughout the tape
        if transition['output']['tape_displacement'] == 'R':
            position += 1
        elif transition['output']['tape_displacement'] == 'L':
            position -= 1
        elif transition['output']['tape_displacement'] == 'S':
            position = position # continue

        current_state = transition['output']['final_state']
        # print the production after updating the current state 
        print_instant_production(state=current_state, tape=tape, position=position)
    
    return tape, current_state


def is_accepted(w: str, tape: np.ndarray, final_state: int, halt_state: int):
    '''
    prints if the chain was accepted or not by the Turing Machine 
    '''
    chain_concatenated : str = ''.join([i if i is not None else '' for i in tape])
    if final_state == halt_state:
        print(f"Input chain '{w}' was accepted by the TM with result:\n{chain_concatenated}")
    else:
        print(f"Input chain '{w}' was rejected by the TM with result:\n{chain_concatenated}")

def print_instant_production(state: int, tape: np.ndarray, position: int):
    '''
    print instant productions 
    '''
    tape: np.ndarray = np.array(['B' if symbol is None else symbol for symbol in tape]) # replace None instances for Blank
    tape[position] = f'[{state}, {tape[position]}]' # change the current position for the state and position it is
    tape_content: str = ''.join(str(symbol) for symbol in tape) # join the symbols found in the current array
    print(f"\t{tape_content}") # print content currently in the tape