from abc import ABC, abstractmethod
import os

class Analyzer(ABC):
    name = "base_analyzer"  # Unique identifier
    supported_mimes = []  # e.g., ['.png', '.jpg']
    
    @abstractmethod
    def decode(*args, **kwargs) -> str:
        """decodes the file for the payload"""
        pass
    
    @abstractmethod
    def encode(*args, **kwargs):
        """encodes data into the file"""
        pass
