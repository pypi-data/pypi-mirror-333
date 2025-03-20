from abc import ABC, abstractmethod
class ShortMemory(ABC):
    def __init__(self, session_id: str):
        self.session_id = session_id

    @abstractmethod
    def load_messages(self) -> List[str]:
        """Carica i messaggi della sessione"""
        pass

    @abstractmethod
    def save_messages(self, messages: List[str]):
        """Salva i messaggi della sessione"""
        pass
