### Generate List of EGA files to delete on Aspera server
This operation generates the list of files on EGA Aspera server that can be removed from the box.

- Config File parameters:
   - jtracker_host: The JTracker server IP address. Make sure that this IP address is reachable from your current network.
   - jtracker_user: Your JTracker username or the JTracker username you would like to access the queues
   - queues: The ids of the JTracker queues
   - aspera_user: The username downloading data from EGA Aspera box
   - aspera_host: The address of the EGA Aspera box
- Command arguments:
   - -c/--config: Configuration file containing the previous config file parameters
   - -o/--output-file: The output file where the list of files should be generated.

To see the validation schema of the EGA files to delete operation, run:

``./main.py ega:delete:schema ``

To run the EGA files to delete operation, run:

``./main.py ega:delete --config ega_to_delete.yml --output-file to_delete.tsv``
