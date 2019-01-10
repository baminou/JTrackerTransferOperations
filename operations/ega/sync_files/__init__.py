
from operation_types.yml_config_operation import YmlConfigOperation
from ..utils.etcd_jtracker import ETCDJTracker
import os
import json
import shutil

class SyncFiles(YmlConfigOperation):

    @staticmethod
    def name():
        return "sync"

    @staticmethod
    def description():
        return "Synchronize EGA files from JTracker server with EGA files in git repository on a local machine"

    def _parser(self, main_parser):
        return

    def _config_schema(self):
        return {
            "jtracker_host": {"type":"url"},
            "jtracker_user": {"type":"string"},
            "jtracker_queue": {"type": "string"},
            "git_repo": {"type":"string"},
            "required":["jtracker_host","jtracker_user","jtracker_queue","git_repo"]
        }

    def _run(self):
        etcd_jt = ETCDJTracker(self.config.get('jtracker_host'), self.config.get('jtracker_user'), self.config.get('jtracker_queue'))

        repo_path = self.config.get('git_repo')

        cpt = 0

        for etcd_job in etcd_jt.get_jobs():
            cpt = cpt + 1
            state = etcd_job.get('state')
            bundle_id = json.loads(etcd_jt.get_job(etcd_job.get('id')).get('job_file')).get('bundle_id')

            for root, dirs, files in os.walk(repo_path):
                for filename in files:
                    if filename.startswith('job.') and filename.endswith('.json'):
                        if bundle_id in filename:
                            print(str(cpt)+" - "+state+' - '+os.path.join(root,filename)+' - '+str(not state in os.path.join(root,filename)))
                            if not state in os.path.join(root,filename):
                                out_dir_path = os.path.join(repo_path,state+"-jobs")
                                if os.path.isdir(out_dir_path):
                                    self.mv_job_to_state(os.path.join(root,filename),filename,state, out_dir_path)
                                    print(os.path.join(root,filename) + ' - '+state)
        return True

    def mv_job_to_state(self, file_path, file_name, state, dir_path):
        print(dir_path)
        final_path = os.path.join(dir_path,file_name)
        if state == 'completed':
            final_path = os.path.join(dir_path,file_name.replace('.json',''))
            if not os.path.isdir(final_path):
                os.mkdir(final_path)
            final_path = os.path.join(final_path,file_name)

        print(final_path)
        shutil.move(file_path,final_path)