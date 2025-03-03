import yaml
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
        
def convert_to_array(w: str, binary_encoding: bool=False, unary_encoding: bool = False) -> list:
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
        chain_null : list = list(binary) # add null to both ends
        return chain_null # return a list of the binary      
    
    elif unary_encoding and w.isdigit():
        w: int = int(w)
        unary: list = ['1' for _ in range(w)] # fill array with 1
        chain: list =  [None] + unary + 20*[None]

        return chain

    else:
        chain_null: list = [None] + list(w) + [None] # if no binary needed, return as a np.ndarray
        return chain_null
  
def select_turing_yaml(file_path: str, w: str, multiple_input_chains: bool=False) -> None:
    '''
    Selects which yaml to use and checks if it needs a binary codification or not
    '''
    instructions: dict = read_yaml(file_path=file_path) 
    binary_code: str = instructions.get('cod', {}).get('binary', 'n') # check if has binary code, else, do not pass to binary
    results_arr: list

    if binary_code == 'y':
        arr: list = convert_to_array(w=w, unary_encoding=True) # if Fibonacci, needs to be encoded 
    else:
        arr: list = convert_to_array(w=w) 

    if multiple_input_chains:
        results_arr: list = simulate_multiple_chains(position=1, instructions=instructions)
        # for string, result in results_arr:
        #     print(f"String: {string} with time: {result}\n")
    else:
        traverse_tape(w=w, tape=arr, position=1, instructions=instructions, delta_dict=get_transition_map(instructions=instructions))
   

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

def traverse_tape(w: str, tape: list, position: int, instructions: dict, delta_dict:dict, avoid_printing:bool=False) -> float:
    halt_state = instructions['q_states']['final'] # get the final state
    initial_time: float = set_time()
    final_tape, final_tape_state = iterate(transition_map=delta_dict, tape=tape, initial_poisition=position, initial_state=instructions['q_states']['initial'], avoid_printing=avoid_printing) 
    final_time: float = set_time()
    time_execution: float = get_time(initial_time=initial_time, final_time=final_time)
    is_accepted(w=w, tape=final_tape, final_state=final_tape_state, halt_state=halt_state, execution_time=time_execution, unary_to_decimal=True)
    return time_execution


def ensure_in_bounds(tape: list, position: int, blank_symbol=None, chunk_size: int = 10) -> tuple[list, int]:
    """
    If 'position' is out of range, extend the tape with chunk_size blanks on left or right.
    Returns the (possibly new) tape and the (possibly updated) position.
    """
    if position < 0:
        needed = abs(position)
        # For efficiency, extend by at least 'chunk_size'
        needed = max(needed, chunk_size)
        # Prepend blanks
        tape = [blank_symbol] * needed + tape
        position += needed
    elif position >= len(tape):
        needed = position - len(tape) + 1
        needed = max(needed, chunk_size)
        # Append blanks
        tape += [blank_symbol] * needed
    return tape, position

def iterate(transition_map: dict , tape: list, initial_poisition: int, initial_state: int, avoid_printing: bool) -> tuple[list, int]:
    position: int = initial_poisition # define initial position
    current_state: int = initial_state # define initial state

    while True:
        tape, position = ensure_in_bounds(tape, position, chunk_size=10)
        current_symbol:str = tape[position]
        transition = transition_map.get((current_state, current_symbol))
        if transition is None:
            break
        
        # update the tape
        new_symbol = transition['output']['tape_output']
        tape[position] = new_symbol


        move = transition['output']['tape_displacement']
        # move throughout the tape
        if  move == 'R':
            position += 1
        elif move == 'L':
            position -= 1
        elif move == 'S' or move == 'N':
            pass # position = position

        current_state = transition['output']['final_state']
        # print the production after updating the current state
        if not avoid_printing:
            print_instant_production(state=current_state, tape=tape, position=position)
    
    return tape, current_state


def is_accepted(w: str, tape: list, final_state: int, halt_state: int, execution_time:float=None, unary_to_decimal:bool=False):
    '''
    prints if the chain was accepted or not by the Turing Machine 
    '''
    acception: str = "rejected"
    chain_concatenated : str = ''.join([i if i is not None else '' for i in tape])
    if unary_to_decimal:
        chain_concatenated = sum([int(i) for i in chain_concatenated])
    if final_state == halt_state:
        acception = "accepted"
    print(f"\nInput chain '{w}' was {acception} by the TM with result: {chain_concatenated}\ntime: {execution_time}")

    


def print_instant_production(state: int, tape: list, position: int):
    '''
    print instant productions 
    '''
    snapshot: list = tape[:]

    # replace None with B for display 
    snapshot = ['B' if sym is None else sym for sym in snapshot]

    # append the state 
    if 0 <= position < len(snapshot):
        snapshot[position] = f"[Q{state},{snapshot[position]}]"

    # Join and print
    print("".join(str(symbol) for symbol in snapshot))

def set_time() -> float:
    '''Sets time'''
    return time.perf_counter()

def get_time(initial_time: float, final_time: float) -> float:
    '''Returns difference between times'''
    return final_time - initial_time 


def simulate_multiple_chains(position: int, instructions: dict) -> list:
    '''
    this function simulates many strings to later be passed for plotting with results being a 2D array with [<chain>, <time>] format.
    '''
    time_result: float = 0.0
    time_exc_arr: list = []
    simulation_strings: list = instructions.get('simulation_strings', [])
    delta_dict: dict = get_transition_map(instructions=instructions) # get delta instructions before hand 
    for string in simulation_strings:
        tape: list = convert_to_array(w=string, unary_encoding=True)
        time_result = traverse_tape(w=string, tape=tape, position=position, instructions=instructions, delta_dict=delta_dict, avoid_printing=True)
        time_exc_arr.append((string, time_result)) 
    return time_exc_arr
