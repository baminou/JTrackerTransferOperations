### Generate list of EGA accession information in TSV format for files to stage

This operation generates a TSV file containing a list of files to stage on EGA server.
Explanation of the logic:

1. Retrieve all EGAFIDs on EGA aspera server
2. Retrieve all EGAFIDs in old and new jtracker
3. Retrieve all EGAFIDs in the .tsv audit file
4. List the files that are in the audit, not in JTracker and not on aspera server

First publish the config file
```bash
./main.py base publish ega to_stage
```

For help, run:

```bash
./main.py ega to_stage -h
```

To run the operation:
```bash
./main.py ega to_stage resources/ega/to_stage/config.yml -a [AUDIT_TSV] -o [OUTPUT_FILE]
```

- AUDIT_TSV: Audit.tsv file containing the EGA information
- OUTPUT_FILE: Output file for the files to stage
