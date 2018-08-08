
from operation_types.operation import Operation
import logging
import os
import minibam_transfer
import shutil
import argparse

class SyncFiles(Operation):

    @staticmethod
    def name():
        return "sync"

    @staticmethod
    def description():
        return "Synchronize mini-bam file transfer on JTracker with Github Repo"

    @staticmethod
    def _parser(self, main_parser):
        main_parser.add_argument('-p', '--payload', dest='payload', required=True,
                                             type=argparse.FileType('r'), help="Song payload json file")

    def _schema(self):
        return {
            "jtracker_host": {"type": "string"},
            "jtracker_user": {"type": "string"},
            "queues": {
                "type": "array",
                "items": {"type": "string"}
            },
            "git_dirs":{
                "type": "object",
                "properties": {
                    "queued": {"type":"string"},
                    "failed": {"type":"string"},
                    "completed": {"type":"string"},
                    "running": {"type":"string"},
                    "backlog": {"type":"string"},
                    "resume": {"type": "string"}
                },
                "required": ["queued","failed","completed","running","backlog"]
            },
            "required": ["jtracker_host","jtracker_user","git_dirs","queues"]
        }

    def _run(self):
        logging.info("Sync mini-bam files with git repository")
        jobname_state = minibam_transfer.get_jobnames_state(self._config.get('jtracker_host'),self._config.get('jtracker_user'),self._config.get('queues'))

        for job in jobname_state:
            for state in self._config.get('git_dirs'):
                for file in os.listdir(self._config.get('git_dirs')[state]):
                    if job in file:
                        found = True
                        if state == jobname_state[job]:
                            break
                        else:
                            self.mv_job_to_state(os.path.join(self._config.get('git_dirs')[state],file),file,jobname_state[job],self._config.get('git_dirs')[jobname_state[job]])

    def mv_job_to_state(self, file_path, file_name, state, dir_path):
        final_path = os.path.join(dir_path,file_name)
        if state == 'completed':
            final_path = os.path.join(dir_path,file_name.strip('.json'))
            if not os.path.isdir(final_path):
                os.mkdir(final_path)
            final_path = os.path.join(final_path,file_name)

        shutil.move(file_path,final_path)