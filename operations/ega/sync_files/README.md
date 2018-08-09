### Synchronize JTracker jobs with a github repository

This operation is moving the files in a github repository to reflect what is on JTracker.

The repository must be in the following format:
```bash
.
├── backlog-jobs
├── completed-jobs
├── failed-jobs
├── queued-jobs
```

To have help, run:
```
./main.py ega sync -h
```

Start by publishing the config file:
```bash
./main.py base publish ega sync
```

Run the operation after completing the config file:
```bash
./main.py ega sync resources/sync/config.yml
```