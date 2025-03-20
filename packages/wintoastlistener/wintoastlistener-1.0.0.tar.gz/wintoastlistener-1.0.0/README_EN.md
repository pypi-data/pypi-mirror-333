# WinToastListener
[README_CN](./README.md)  
A python library implemented by python3, for listening to Toast message notifications on windows.

![Demo](./images/example.gif)  

## Supported platforms  
**Supported**  
Windows10 and above  

**Untested**  
Windows8  
P.S.: I don't have the system and can't test it. Welcome to test the relevant system and let me know the conclusion.  

**Not supported**  
Windows7 and below  

## Installation

`pip install wintoastlistener`

## Minimum usage example

```python
from wintoastlistener import ToastListener


def example_callback(event_data, resources):
    print(event_data)
    print(resources)


listener = ToastListener(callback=example_callback)
listener.listen()
```

[More examples](./examples)

## Document
[Document](https://github.com/Gu-f/WinToastListener/wiki/Document)  