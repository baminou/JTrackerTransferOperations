### Generate job files required for JTracker to run EGA workflow

This operation is generating the list of JSON files required for JTracker. Logic:
1. Retrieve all EGAFIDs that are listed as available on EGA Aspera server
2. Retrieve all EGAFIDs that have been integrated to JTracker in the previoux version (Github) and the new version (ETCD)
3. Retrieve all EGAFIDs available in a TSV audit report
4. Keep EGAFIDs that are in the audit, on the Aspera server and that haven't been integrated to JTracker yet.

To generate the jobs, first generate the config file for the operation:
```bash
./main.py base publish ega job
```
The config file is going to be generated under:
```bash
./resources/ega/job/config.yml
```

Enter the informations required in the yaml file

Run the command:
```bash
./main.py ega job -c resources/ega/job/config.yml -a [AUDIT] -o [OUTPUT_DIR]
```
AUDIT: Path of the audit TSV file containing information for the transfer
OUTPUT_DIR: Path of the output directory