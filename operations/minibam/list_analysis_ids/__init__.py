
from operation_types.json_operation import JsonOperation
import requests
import json

class Listanalysisids(JsonOperation):

    @staticmethod
    def name():
        return "list_analysis_ids"

    @staticmethod
    def description():
        return "List analysis ids in allowed codes"

    def _config_schema(self):
        return {}

    def _parser(self, main_parser):
        return

    def _run(self):
        for queue in self.json.get('jtracker_host').get('queues'):
            jobs = get_jobs(self.json.get('jtracker_host').get('url'),queue.get('user'),queue.get('id'))
            for job in jobs:
                study_id = get_study_id(job)
                if study_id not in self.json.get('exclude_projects'):
                    for analysis_id in get_analysis_ids(job):
                        print(job.get('id')+"\t"+study_id+"\t"+analysis_id+"\t"+get_file_name(job,analysis_id))
        return


def get_jobs(jtracker_host, username, queue_id, state="completed"):
    return json.loads(requests.get('%s/api/jt-jess/v0.1/jobs/owner/%s/queue/%s?state=%s' % (jtracker_host, username, queue_id, state)).text)

def find_job(jobs_list, job_id):
    for job in jobs_list:
        if job.get('id') == job_id:
            return job
    raise Exception("Job not found: %s" % (job_id))

def get_study_id(job):
    return json.loads(job.get('job_file')).get('study_id')

def get_file_name(job, analysis):
    if json.loads(job.get('job_file')).get('normal_bam').get('song_analysis_id') == analysis:
        return json.loads(job.get('job_file')).get('normal_bam').get('minibam').get('bam_file_name')
    for tumour in json.loads(job.get('job_file')).get('tumour_bams'):
        if tumour.get('song_analysis_id') == analysis:
            return tumour.get('minibam').get('bam_file_name')

def get_analysis_ids(job):
    ids = [json.loads(job.get('job_file')).get('normal_bam').get('song_analysis_id')]
    for tumour in json.loads(job.get('job_file')).get('tumour_bams'):
        ids.append(tumour.get('song_analysis_id'))
    return ids