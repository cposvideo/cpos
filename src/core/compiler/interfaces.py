from abc import ABC, abstractmethod

class CompilerStage(ABC):
    @abstractmethod
    def run(self, ctx): ...

class CompilerError(Exception): pass
