### Generate List of EGA files to delete on Aspera server
This operation generates the list of files on EGA Aspera server that can be removed from the box.

Publish the configuration file
```bash
./main.py base publish ega to_delete
```

Need help to run the operation
```bash
./main.py ega to_delete -h
```

Run the command
```bash
./main.py ega to_delete resources/ega/to_delete/config.yml -o [OUTPUT_FILE]
```
- OUTPUT_FILE: File where to write the list of files to delete