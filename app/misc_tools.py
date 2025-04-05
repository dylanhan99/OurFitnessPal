from typing import Dict, Any
import threading

class OFPStorage():
    '''
        A simple helper class to simply map key:value.
        key: Any 
        value: Any
    '''
    def __init__(self):
        self._globals: Dict[Any, Any] = {}

    def set(self, key: Any, value: Any) -> None:
        self._globals[key] = value
        
    def get(self, key: Any, default: Any = None) -> Any:
        return self._globals.get(key, default)

    def erase(self, key: Any) -> bool:
        if key not in self._globals:
            return False
        del self._globals[key]
        return True
        
            