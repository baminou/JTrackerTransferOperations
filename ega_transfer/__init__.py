
import logging
from operations.ega.utils.ega_audit import EGAAudit
from entities.ega import EGA
from operations.ega.utils.etcd_jtracker import ETCDJTracker
from operations.ega.utils.github_jtracker import GithubJTracker
import os
from collections import OrderedDict

def get_jtracker_fids(jtracker_instance,state=None):
    """
    Retrieve all EGAFIDs from a jtracker instance
    :param jtracker_instance: A Jtracker instance containing jobs with ids
    :param state: A state to filter the returned EGAFIDs
    :return: A list of EGAFID
    """
    logging.info("Retrieving JTracker EGAFIDs from "+jtracker_instance.__class__.__name__)
    fids = []
    for id in jtracker_instance.get_job_ids(state):
        logging.debug("Reading EGA files from "+id)
        files = jtracker_instance.get_job_data(id).get('files')
        for file in files:
            logging.debug(file)
            fids.append(file.get('ega_file_id'))
    logging.info("JTracker EGAFIDs retrieved successfully "+jtracker_instance.__class__.__name__)
    return fids


def get_audit_fids(tsv_file):
    """
    Retrieve all EGAFIDs contained in an audit tsv file
    :param tsv_file: An EGA TSV file from https://github.com/icgc-dcc/ega-file-transfer/tree/master/ega_xml
    :return: A list of EGAFIDs
    :raises FileNotFoundError: TSV file not found
    """
    if not os.path.isfile(tsv_file):
        raise FileNotFoundError(tsv_file)

    logging.info("Retrieve EGAFIDs from audit report %s" % (tsv_file))
    fids = EGAAudit(tsv_file).get_egaf_ids()
    logging.debug(fids)
    logging.info("EGAFIDs retrieved from audit report %s" % (tsv_file))
    return fids

def get_ega_box_fids(aspera_server, aspera_user):
    """
    Retrieve all EGAFIDs from EGA box aspera server
    :param aspera_server: A valid accessible aspera server
    :param aspera_user: A valid user for the aspera server
    :return: A list of EGAFIDs
    """
    logging.info("Loading EGAFIDs from EGA aspera server")
    ega = EGA(aspera_server,aspera_user)
    fids = ega.dbox_egafids()
    logging.info("EGAFIDs Aspera server loaded")
    return fids

def get_etcd_jtracker_egafids(host, user, queue, state):
    """
    Retrieve all EGA FIDs on a jtracker server in a queue
    :param host: A running JTracker server
    :param user: A JTracker user
    :param queue: The queue of jobs
    :param state: The state of the jobs to retrieve
    :return: A list of EGAFIDs
    """
    jtracker = ETCDJTracker(host, user, queue)
    return get_jtracker_fids(jtracker, state)

def get_github_jtracker_egafids(dirs, state):
    jtracker = GithubJTracker(dirs)
    return get_jtracker_fids(jtracker,state)

def get_all_jtracker_egafids(hosts, dirs, states=['completed', 'failed', 'backlog', 'running', 'resume', 'queued']):
    jtracker_fids = []
    for state in states:
        jtracker_fids = jtracker_fids + get_github_jtracker_egafids(dirs, state)
        for host in hosts:
            for queue in host.get('queues'):
                jtracker_fids = jtracker_fids + get_etcd_jtracker_egafids(host.get('url'),queue.get('user'),queue.get('id'),state)
    return jtracker_fids

def get_files_to_stage(egafids, tsv_file, entityType):
    keys = []
    result = []
    
    if not os.path.isfile(tsv_file):
        raise FileNotFoundError(tsv_file)
    logging.info("Retrieve EGAFIDs from audit report to stage: %s" % (tsv_file))
    if entityType == 'analysis':
       keys = ['project_code','submitter_sample_id','ega_sample_id','ega_analysis_id','file_name','ega_file_id',
            'encrypted_file_md5sum','file_md5sum','dataset_id','file_size']
    elif entityType == 'run':
       keys = ['project_code','submitter_sample_id','ega_sample_id','ega_experiment_id','ega_run_id','file_name','ega_file_id',
           'encrypted_file_md5sum','file_md5sum','dataset_id','file_size']
       
    for fid in egafids:
        if entityType == 'run':

           values = EGAAudit(tsv_file).get_info_from_egafid(fid,"ICGC DCC Project Code",
                                                       "ICGC Submitted Sample ID","EGA Sample Accession","EGA Experiment Accession",
                                                       "EGA Run Accession","EGA Raw Sequence Filename","EGA File Accession","MD5 Checksum",
                                                       "Unencrypted Checksum","EGA Dataset Accession","File Size")
        elif entityType == 'analysis':
           values = EGAAudit(tsv_file).get_info_from_egafid(fid,"ICGC DCC Project Code",
                                                       "ICGC Submitted Sample ID","EGA Sample Accession","EGA Analysis Accession",
                                                       "EGA Raw Sequence Filename","EGA File Accession","MD5 Checksum",
                                                       "Unencrypted Checksum","EGA Dataset Accession","File Size")

        result.append(OrderedDict(zip(keys,values)))
        logging.debug(values)
    logging.info("To stage informations retrieved")
    return result

def get_files_to_delete():
    return
