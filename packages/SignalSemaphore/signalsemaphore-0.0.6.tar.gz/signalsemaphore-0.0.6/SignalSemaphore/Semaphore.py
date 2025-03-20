from typing import Callable, Dict, List

class Semaphore:
    """
    A simple signaling system to register and emit events.  
    Example usage:
    >>> semaphore = Semaphore()
    >>> def handler(data):
    ...     print(f"Received: {data}")
    >>> semaphore.connect("event", handler)
    >>> semaphore.emit("event", "Hello")
    Received: Hello
    >>> semaphore.disconnect("event", handler)
    >>> semaphore.emit("event", "Hello")  # No output expected
    """
    def __init__(self):
        self._handlers: Dict[str, List[Callable]] = {}
                                                            
    def connect(self, event: str, handler: Callable) -> None:
        """Registers a handler for a given event."""
        if event not in self._handlers:
            self._handlers[event] = []
        if handler not in self._handlers[event]:
            self._handlers[event].append(handler)
                                                                                                                    
    def disconnect(self, event: str, handler: Callable) -> None:
        """Removes a registered handler from an event."""
        if event in self._handlers and handler in self._handlers[event]:
            self._handlers[event].remove(handler)
        if not self._handlers[event]:
            del self._handlers[event]
                                                                                                                                                                                    
    def emit(self, event: str, *args, **kwargs) -> None:
        """Emits an event, triggering all registered handlers."""
        for handler in self._handlers.get(event, []):
            handler(*args, **kwargs)
    
    def disconnect_all(self) -> None:
        handlers = [(e, h) for e in self._handlers for h in self._handlers[e]]
        for h in handlers:
            self.disconnect(h[0], h[1])

    def __del__(self):
        self.disconnect_all()

if __name__ == "__main__":
    import doctest
    doctest.testmod()

    def handler(data):
        print(f"Received {data}")

    semaphore = Semaphore()
    semaphore.connect("event", handler)
    semaphore.emit("event", "Hello")
    del semaphore
