from abc import ABC, abstractmethod

class EquipmentModel(ABC):
    def __init__(self, name):
        self.name = name
        self.inputs = {}  # Dictionary of input streams (name: Data object)
        self.outputs = {} # Dictionary of output streams (name: Data object)
        self.parameters = {} # Dictionary of equipment-specific parameters

    @abstractmethod
    def process(self):
        """This abstract method should be overridden by subclasses to implement
        the specific behavior of each equipment type."""
        pass

    def set_parameter(self, parameter_name, value):
        """Sets the value of a equipment-specific parameter."""
        if parameter_name in self.parameters:
            self.parameters[parameter_name] = value
        else:
            print(f"Error: Parameter '{parameter_name}' not found in {self.name}")

    def get_parameter(self, parameter_name):
        """Retrieves a parameter value."""
        if parameter_name in self.parameters:
            return self.parameters[parameter_name]
        else:
            print(f"Error: Parameter '{parameter_name}' not found in {self.name}")
            return None  # Or raise an exception

    def __repr__(self):
        return f"{self.name} (Type: {self.__class__.__name__})" #Show Class name in print