### List runnable jobs in a Github repository

This operation lists all job files that have the files available on EGA Aspera server.

To have more information about this operation, run:
```bash
./main.py ega runnable -h
```

Run the operation:
```
./main.py ega runnable [JOB_DIRECTORY] [ASPERA_HOST] [ASPERA_USER]
```

- JOB_DIRECTORY: A directory containing a list of valid job json files
- ASPERA_HOST: Aspera server containing the files to be transferred
- ASPERA_USER: Aspera username used to download files on Aspera server