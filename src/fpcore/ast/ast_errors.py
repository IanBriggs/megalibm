

from utils import Logger


logger = Logger()




class ArityError(Exception):
    def __init__(self, expected_arity, operation, arguments,
                 available_operations):
        self.expected_arirty = expected_arirty
        self.operation = operation
        self.arguments = arguments
        self.available_operations = available_operations
