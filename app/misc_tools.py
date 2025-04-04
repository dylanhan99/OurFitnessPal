from typing import Dict, Any
import threading

class OFPStorage():
    '''
        A simple thread safe helper class to simply map key:value.
        key: Any 
        value: Any
    '''
    def __init__(self):
        self._globals: Dict[Any, Any] = {}
        self._lock = threading.Lock()

    def set(self, key: Any, value: Any) -> None:
        with self._lock:
            self._globals[key] = value
        
    def get(self, key: Any, default: Any = None) -> Any:
        with self._lock:
            self._globals.get(key, default)

    def erase(self, key: Any) -> bool:
        with self._lock:
            if key not in self._globals:
                return False
            del self._globals[key]
            return True
        
            