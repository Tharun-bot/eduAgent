from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

class BaseAgent(ABC):
    """
    Abstract base class for all educational agents.
    """
    
    def __init__(self, name: str, model: Any, memory: Optional[Dict] = None):
        """
        Initialize the agent.
        
        :param name: Name of the agent.
        :param model: LLM or AI model used by the agent.
        :param memory: Optional memory storage for context retention.
        """
        self.name = name
        self.model = model
        self.memory = memory if memory is not None else {}
    
    @abstractmethod
    def respond(self, query: str) -> str:
        """
        Abstract method to handle user queries and return responses.
        Must be implemented by subclasses.
        
        :param query: User input query.
        :return: Response from the agent.
        """
        pass
    
    def remember(self, key: str, value: Any):
        """
        Store information in memory.
        
        :param key: Memory key.
        :param value: Memory value.
        """
        self.memory[key] = value
    
    def recall(self, key: str) -> Optional[Any]:
        """
        Retrieve stored information from memory.
        
        :param key: Memory key.
        :return: Memory value or None if not found.
        """
        return self.memory.get(key)
    
    def clear_memory(self):
        """
        Clear all stored memory.
        """
        self.memory.clear()

    def __repr__(self):
        return f"{self.__class__.__name__}(name={self.name}, model={self.model})"