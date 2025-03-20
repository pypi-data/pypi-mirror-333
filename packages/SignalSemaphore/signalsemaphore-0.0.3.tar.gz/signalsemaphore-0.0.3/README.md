# SignalSemaphore

A lightweight Python event signaling system.

## Installation
```
pip install signalsemaphore
```

## Usage
```python
from SignalSemaphore import Semaphore

semaphore = Semaphore()

def handler(data):
    print(f"Received: {data}")

semaphore.connect("event", handler)
semaphore.emit("event", "Hello")
semaphore.disconnect("event", handler)
```