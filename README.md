## JTrackerTransferOperations -> EGATransfer Operations


This CLI build with [Uperations Framework](https://uperations.com) contains operations to manage the transfer. The purpose of this transfer
is to move EGA files to Collaboratory. The transfer is orchastred with [JTracker](https://jtracker.io).

The process is done in few steps:
1. EGA team stages files to be transferred on their Aspera Server
2. We generate the jobs for the files that have to be transferred according to what is staged.
3. We run the [workflow](https://github.com/icgc-dcc/ega-file-transfer-to-collab-jt) to transfer the files
4. Once the files are transferred, EGA team can clear the files from their Aspera server


### Install this repository
```bash
git clone https://github.com/icgc-dcc/JTrackerTransferOperations.git
cd JTrackerTransferOperations
pip3 install -r requirements.txt
```

Once everything is installed, you should be able to see all available operations.
```bash
./main.py base list:operations
```

### 1. Create the list of files to be staged
```bash
./main.py ega to_stage -a :AUDIT_TSV -t :TYPE -o :OUTPUT_FILE
```
**AUDIT_TSV**: A tsv file containing informations about donors (eg. https://github.com/icgc-dcc/ega-file-transfer/blob/master/ega_xml/v20170522/BRCA-EU/BRCA-EU_Audit_ICGC23.tsv)

**TYPE**: run or analysis

**OUTPUT_FILE**: Output file where to generate the list of files to stage


### 2. Generate the transfer jobs
```bash
./main.py ega job -a {AUDIT_TSV} -m {METADATA_VERSION} -r {METADATA_REPO} -o {OUTPUT_DIR}
```

**AUDIT_TSV**: A tsv file containing informations about donors (eg. https://github.com/icgc-dcc/ega-file-transfer/blob/master/ega_xml/v20170522/BRCA-EU/BRCA-EU_Audit_ICGC23.tsv)

**METADATA_VERSION**: Metadata version (eg. v20170522)

**METADATA_REPO** URL of the metadata repository (eg. https://github.com/icgc-dcc/ega-file-transfer/blob/master/ega_xml/v20170522)

### 3. Synchronize the transfer status with Github
As the transfer is running, the jobs are synchronized between JTracker and [this Github repository](https://github.com/icgc-dcc/ega-file-transfer/tree/master/ega_transfer_jobs). This makes
it easier to see the status of the jobs with a folder structure.

#### Synchronize one queue
```bash
./main.py ega sync config.yml
```
```yaml
#config.yml
jtracker_host: # JTracker host with port
jtracker_user: # JTracker username
jtracker_queue: # Queue ID
git_repo:  # Local repository containing backlog-jobs completed-jobs failed-jobs queued-jobs
```
#### Synchronize all queues under JTracker user
```bash
./main.py ega sync:user :HOST :USERNAME :WF_NAME :GIT_LOCAL_REPO
```
**HOST**: JTracker host IP or URL

**USERNAME**: Username on JTracker

**WF_NAME**: Name of the workflow on JTracker

**GIT_LOCAL_REPO**: Local path to the git repository: https://github.com/icgc-dcc/ega-file-transfer/tree/master/ega_transfer_jobs

### 4. Delete files that have been transferred
Once the files have been transferred to Collaboratory, they can be removed from EGA's aspera server. The list of files to be
removed has to be sent to EGA.
```bash
./main.py ega to_delete config.yml
```
```yaml
#config.yaml
jtracker_host: # JTracker server url with port number
jtracker_user: # JTracker user name
queues:
  - # List of queues under the user
aspera_host: # Aspera server
aspera_user: # Aspera username
```

##Transfer helper commands
### What is on EGA's aspera server
This fonction is going to list all EGAFID files on aspera server. Aspera's server contains one file called dbox on their server
that is listing what is staged. This command outputs the content of this file on the terminal.
```bash
./main.py ega dbox :ASPERA_SERVER :ASPERA_USER
```
**ASPERA_SERVER**: The URL of EGA aspera user

**ASPERA_USER**: The username to connect to the aspera user
