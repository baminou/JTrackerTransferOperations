### EGA Transfer to Collaboratory

This library contains multiple operations that are often used to manage the EGA data transfer to Collaboratory.

To list all available operations for the EGA transfer, run:
```bash
./main.py base list:operations -l ega
```

```bash
Library    Command    Operation    Description
---------  ---------  -----------  --------------------------------------------------
ega        job        job          Generate the job json files needed to run JTracker
ega        dbox       dbox         List all files on EGA Aspera server
ega        to_stage   to_stage     Generate a list of files to be staged on EGA Asper
ega        to_delete  to_delete    Generate a list of files to be deleted on EGA Aspe
ega        runnable   Runnable     List the jobs that can be run from a Github Reposi
ega        is_alive   Isalive      Isalive has not been documented yet.
ega        sync       sync         Synchronize EGA files from JTracker server with EG
```

To have more informations about any of those operations, run:
```bash
./main.py ega {Command} -h
```