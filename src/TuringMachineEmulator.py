import yaml
import numpy as np
import time
from plotting import plot_results

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
        
def convert_to_array(w: str, binary_encoding: bool=False, unary_encoding: bool = False) -> np.ndarray:
    '''
    converts the chain to list and returns it as np.ndarray.
    optionally codifies the input chain to binary
    '''
    if not isinstance(w, str): # in case no str arg was passed
        raise TypeError(f"TypeError: {w} must be type 'str', {type(w)} found instead")

    if binary_encoding and w.isdigit():
        w: int = int(w)
        binary: int = format(w, 'b') # transform to binary str
        print(f"Binary: {binary}\n")
        chain_null : list = list(binary) + [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None] # add null to both ends
        return np.array(chain_null) # return a np.ndarray of the binary
    
    elif unary_encoding and w.isdigit():
        w: int = int(w)
        unary: list = ['|' for _ in range(w)] # fill array with |
        chain: list = ['1', '#', '1'] + unary # add starting case 
        return np.array(chain)

    else:
        chain_null: list = [None] + list(w) + [None] # if no binary needed, return as a np.ndarray
        return np.array(chain_null)
  
def select_turing_yaml(file_path: str, w: str, multiple_input_chains: bool=False) -> None:
    '''
    Selects which yaml to use and checks if it needs a binary codification or not
    '''
    instructions: dict = read_yaml(file_path=file_path) 
    binary_code: str = instructions.get('binary_cod', {}).get('binary', 'n') # check if has binary code, else, do not pass to binary
    results_arr: np.ndarray

    if binary_code == 'y':
        arr: np.ndarray = convert_to_array(w=w, binary_encoding=True) # if Fibonacci, needs to be encoded 
    else:
        arr: np.ndarray = convert_to_array(w=w) 

    if multiple_input_chains:
        results_arr: np.ndarray = simulate_multiple_chains(position=0, instructions=instructions)
        #plot_results(results_arr)
    else:
        traverse_tape(w=w, tape=arr, position=0, instructions=instructions, delta_dict=get_transition_map(instructions=instructions))
   

def get_transition_map(instructions: dict) -> dict:
    '''Gathers only the delta transitions of the function
        Keys are tuples (state, input), values are the corresponding transitions
    '''
    transition_map = {
        (entry['params']['initial_state'], entry['params']['tape_input']): {
            'params': entry['params'],
            'output': entry['output']
        }
        for entry in instructions['delta']
    }
    return transition_map

def traverse_tape(w: str, tape: np.ndarray, position: int, instructions: dict, delta_dict:dict, avoid_printing:bool=False) -> float:
    halt_state = instructions['q_states']['final'] # get the final state
    initial_time: float = set_time()
    final_tape, final_tape_state = iterate(transition_map=delta_dict, tape=tape, initial_poisition=position, initial_state=instructions['q_states']['initial'], avoid_printing=avoid_printing) 
    final_time: float = set_time()
    time_execution: float = get_time(initial_time=initial_time, final_time=final_time)
    is_accepted(w=w, tape=final_tape, final_state=final_tape_state, halt_state=halt_state, execution_time=time_execution)
    return time_execution


def iterate(transition_map: dict , tape: np.ndarray, initial_poisition: int, initial_state: int, avoid_printing: bool) -> tuple[np.ndarray, int]:
    position: int = initial_poisition # define initial position
    current_state: int = initial_state # define initial state
    while True:
        current_symbol = tape[position] if position < len(tape) else None
        transition = transition_map.get((current_state, current_symbol))
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
            pass # position = position

        current_state = transition['output']['final_state']
        # print the production after updating the current state
        if not avoid_printing:
            print_instant_production(state=current_state, tape=tape, position=position)
    
    return tape, current_state


def is_accepted(w: str, tape: np.ndarray, final_state: int, halt_state: int, execution_time:float=None):
    '''
    prints if the chain was accepted or not by the Turing Machine 
    '''
    acception: str = "rejected"
    chain_concatenated : str = ''.join([i if i is not None else '' for i in tape])
    if final_state == halt_state:
        acception = "accepted"
    print(f"\nInput chain '{w}' was {acception} by the TM with result: {chain_concatenated}\ntime: {execution_time}\nTape: {tape}")

    


def print_instant_production(state: int, tape: np.ndarray, position: int):
    '''
    print instant productions 
    '''
    tape: np.ndarray = np.array(['B' if symbol is None else symbol for symbol in tape], dtype=object) # replace None instances for Blank
    tape[position] = f'[S_{state}, {tape[position]}]' # change the current position for the state and position it is
    tape_content: str = ''.join(str(symbol) for symbol in tape) # join the symbols found in the current array
    print(f"\t{tape_content}") # print content currently in the tape


def set_time() -> float:
    '''Sets time'''
    return time.perf_counter()

def get_time(initial_time: float, final_time: float) -> float:
    '''Returns difference between times'''
    return final_time - initial_time 


def simulate_multiple_chains(position: int, instructions: dict) -> np.ndarray:
    '''
    this function simulates many strings to later be passed for plotting with results being a 2D array with [<chain>, <time>] format.
    '''
    time_result: float = 0.0
    time_exc_arr:np.ndarray = np.array([], dtype=object)
    simulation_strings: list = instructions.get('simulation_strings', [])
    delta_dict: dict = get_transition_map(instructions=instructions) # get delta instructions before hand 
    for string in simulation_strings:
        tape: np.ndarray = convert_to_array(w=string, binary_encoding=True)
        time_result = traverse_tape(w=string, tape=tape, position=position, instructions=instructions, delta_dict=delta_dict, avoid_printing=True)
        time_exc_arr = np.append(time_exc_arr, [string , time_result], axis=0) # odd numbers are time execution, even are the chain
    return time_exc_arr
