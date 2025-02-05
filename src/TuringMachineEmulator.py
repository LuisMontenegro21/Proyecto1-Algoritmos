import yaml

def read_yaml(file_path: str):
    with open(file_path, 'r') as stream:
        try:
            instructions = yaml.safe_load(stream=stream)
            return instructions
        except yaml.YAMLError as exception:
            raise exception
        
def convert_to_binary(x: int):
    pass

def add_tape_length(tape: list, direction: str):
    pass

def traverse_tape():
    pass

def iterate(delta, tape, initial_poisition):
    pass