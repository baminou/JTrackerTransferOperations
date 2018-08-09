### Operations

This folder contains all the operations listed under every libraries. All the available operations extend the mother class Operation.
The Operation class has some abstract methods that have to be overriden by your newly created tool and some events that can also be overriden.

##### To know the list of available operations, run:
```bash
./main.py base list:operations
```

#### Create a new operation
Make sure that you already have a library created
```bash
./main.py base create:operation {LIBRARY_NAME} {OPERATION_NAME}
```

### def _parser(self, main_parser) method
Add argument parsers to the command running your operation. Example:
```python
def _parser(self, main_parser):
    main_parser.add_argument('test_arg', help="A test argument for your operation")
    return
```

### def _run(self) method
This method contains the logic of your operation. You can access the arguments parsed before like so:
```python
def _run(self):
    print(self.test_arg)
```

### def name() method
The name of your operation

### def description() method
A brief description of your operation

## Events
If you want to add some logic surrounding your operation, you can use events.

### def _before_start() method
This event is fired right before executing the operation

### def _on_completed() method
This event is fired once the run is successully completed

### def _on_running() method
Fired every 2 seconds while the tool is running.
