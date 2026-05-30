from abc import ABC, abstractclassmethod

from src.email import Email



class Rule(ABC):
    @abstractclassmethod
    def score(self, email: Email) -> dict:
        pass
