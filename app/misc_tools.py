from typing import Dict, Any
import threading

class BaseSingleton:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            with cls._lock:
                cls._instance = super().__new__(cls)
        return cls._instance

class OFPGlobals(BaseSingleton):
    '''
        A singleton helper class serving as a global store for the SERVER. 
        Shared among all users.
    '''
    def __init__(self, *args, **kwargs):
        self._globals = {}

    def set(self, key: str, value: Any) -> None:
        with self._lock:
            self._globals[key] = value
        
    def get(self, key: str, default: Any = None) -> Any:
        with self._lock:
            self._globals.get(key, default)

    def erase(self, key: str) -> bool:
        with self._lock:
            if key not in self._globals:
                return False
            del self._globals[key]
            return True
        
            