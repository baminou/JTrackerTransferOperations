### Operations

Operations are actions to do on a JTracker workflow. Those operations can go from
generating jobs for a specific workflow to synchronize files on a JTracker server
with jobs in a Github repository. To create a new operation, extend the Operation
class in operation.py.

List of available operations:
#### EGA workflow
- [ega:dbox](ega_dbox) - List the files on the EGA aspera server
- [ega:job](ega_job)  - Generate jobs for the EGA transfer workflow
- [ega:delete](ega_to_delete) - List the files that can be deleted from EGA aspera server
- [ega:stage](ega_to_stage) - Generate a tsv file containing files that has to be staged on EGA aspera server

#### Minibam workflow
- [minibam:sync](minibam_sync_files/README.md) - Synchronize the files on JTracker server with Github repo: https://github.com/ICGC-TCGA-PanCancer/oxog-ops/tree/master/minibam-icgc-jobs