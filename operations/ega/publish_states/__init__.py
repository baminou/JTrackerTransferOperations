
from kernel.operation import Operation
from ..publish_state import Publishstate
import argparse
import requests
import json

class Publishstates(Operation):

    @staticmethod
    def name():
        return "Publishstates"

    @staticmethod
    def description():
        return "Publishstates has not been documented yet."

    def _parser(self, main_parser):
        main_parser.add_argument(dest='jtracker_host', help="Song server in collab or aws")
        main_parser.add_argument(dest='queue_id', help="JTracker queue ID")
        main_parser.add_argument(dest='owner_name', help="JTracker owner name")
        main_parser.add_argument(dest='song', help="Song server to check", choices=['aws','collab'])
        return

    def _run(self):
        request_url = "/".join([self.args.jtracker_host,'api','jt-jess','v0.1','jobs','owner',self.args.owner_name,'queue',self.args.queue_id+'?state=completed'])
        for job in requests.get(request_url).json():
            job_file = json.loads(job.get('job_file'))
            args = argparse.Namespace()
            args.song = self.args.song
            args.study = job_file.get('project_code')
            args.bundle_id = job_file.get('bundle_id')
            Publishstate().execute(args, None)
