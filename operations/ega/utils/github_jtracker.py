

from entities.jtracker import JTracker
import os
import fnmatch
import json
import logging

STATES = ['completed','backlog','running','failed','queued']

class GithubJTracker(JTracker):

    def __init__(self, respositories):
        super().__init__()
        self._repositories = respositories
        self._jobs = {}
        self._load_repositories()
        return

    def _load_repositories(self):
        for repo in self._repositories:
            if not self.validate_folder(repo):
                raise Exception("The repo is not a valid jtracker repository: " + repo)

            for state in STATES:
                for job_path in self._list_jobs_in_repo(os.path.join(repo,"job_state."+state)):
                    with open(job_path, 'r') as fp:
                        self._jobs[job_path] = json.load(fp)
        return

    def validate_folder(self, repo):
        content = os.listdir(repo)
        return 'job_state.completed' in content

    def _get_state(self, job_name):
        for state in STATES:
            if "job."+state in job_name:
                return state

    def get_job_ids(self, state=None):
        if state == None:
            return self._jobs.keys()
        return [id for id in self._jobs.keys() if "job_state."+state in id]

    def get_jobs(self, state=None):
        jobs = []
        for id in self.get_job_ids(state=state):
            jobs.append(self.get_job(id))
        return jobs


    def get_job(self, id):
        return self._jobs[id]

    def get_job_data(self, id):
        return self.get_job(id)

    def _list_jobs_in_repo(self, repo):
        jobs = []
        for root, dirnames, filenames in os.walk(repo):
            for filenames in fnmatch.filter(filenames, 'job.*.json'):
                jobs.append(os.path.join(root,filenames))
        return jobs