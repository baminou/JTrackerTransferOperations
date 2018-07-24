### Generate job files required for JTracker to run EGA workflow

- Config File parameters:
   - etcd_jtracker: 
      - hosts:
         - url: JTracker server IP address
         - queues:
            - user: JTracker username
            - id: JTracker queue id
   - old_jtracker:
      - dirs: List of Old JTracker directories
   - aspera_info:
      - server: The address of the EGA Aspera box
      - user: The username downloading data from EGA Aspera box
   - metadata_repo: The URL of the metadata repository: E.g https://raw.githubusercontent.com/icgc-dcc/ega-file-transfer/master/ega_xml/v20180321
- Command arguments:
   - -c/--config: Configuration file containing the previous config file parameters
   - -a/--audit: Audit file containing the jobs to be generated
   - -o/--output: The output directory for the json files

To see the validation schema of the EGA files to delete operation, run:

``./main.py ega:job:schema``

To run the EGA files to delete operation, run:

``./main.py ega:job --config ega_job.yml --output outdir``
