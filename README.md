## Uperations

This program helps you create standalone and re-usable tools that can be easily integrated in your workflows.
The purpose of this project is to create python tools that can be re-used accross different workflow languages.

Some operations are already accessible to help you build your tools.

The main components to know are Libraries, Operations and Commands.

* Operations: An action that has to be executed.
* Library: A group of operations
* A command to execute in the terminal to run the Operation

### Create a library
The first thing to do is to create a library to contain your operations.
```bash
./main.py base make:library {LIBRARY_NAME}
```

### Add your library to kernel/console.py
```python
def libraries():
    return {
        ...,
        library_name: LIBRARY_NAME
    }
```

### Create an operation
Once you have a library, you can start adding operations.
```bash
./main.py base make:operation {LIBRARY_NAME} {OPERATION_NAME}
```

### Add your operation to the library for access in command line
1. Open ./operations/{LIBRARY_NAME}/__init__.py
2. Import your operation class at the top of the file.
```python
from .{operation_package} import {OperationClass}
```
3. Add to the dict operations
```python
@staticmethod
    def operations():
        return {
            ...,
            {command}:{OperationClass}
        }

```

### List all available operations
```bash
./main.py base list:operations
```

### Retrieve information about a library
```bash
./main.py base {LIBRARY_NAME} -h
```

### Retrieve information about an operation
```bash
./main.py base {LIBRARY_NAME} {OPERATION_NAME} -h
```