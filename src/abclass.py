from abc import *

class GenerateInput(metaclass=ABCMeta):
    @abstractmethod
    def set_parameters(self):
        pass
    
    @abstractmethod
    def write_scripts(self):
        pass
