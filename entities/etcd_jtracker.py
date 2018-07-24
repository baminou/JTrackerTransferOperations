#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .jtracker import JTracker
import requests
import json
import logging


class ETCDJTracker(JTracker):

    def __init__(self, server, user, queue):
        super().__init__()
        self._server = server
        self._user = user
        self._queue = queue
        self._jobs = self._load_jobs()
        return

    def _load_jobs(self):
        return requests.get(self._server+"/api/jt-jess/v0.1/jobs/owner/"+self._user+"/queue/"+self._queue).json()

    def get_job_ids(self, state=None):
        ids = []
        for job in self._jobs:
            if job.get('state') == state:
                ids.append(job.get('id'))
        return ids

    def get_job_data(self, id):
        return json.loads(self.get_job(id).get('job_file'))

    def get_job(self, id):
        for job in self._jobs:
            if job.get('id') == id:
                return job
        raise ValueError("ID not found: "+id)
