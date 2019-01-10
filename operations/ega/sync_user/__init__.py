
from kernel.operation import Operation
import requests
from ..sync_files import SyncFiles

class Syncuser(Operation):

    @staticmethod
    def name():
        return "Syncuser"

    @staticmethod
    def description():
        return "Sync all queues of an user with git repo"

    def _parser(self, main_parser):
        main_parser.add_argument(dest='host', help="JTracker host url with port")
        main_parser.add_argument(dest='username', help="Username")
        main_parser.add_argument(dest='wf_name', help="Workflow name")
        main_parser.add_argument(dest='git_local_repo', help="Path of git local repository")
        return

    def _run(self):
        for queue in requests.get('%s/api/jt-jess/v0.1/queues/owner/%s/workflow/%s' % (self.args.host, self.args.username,self.args.wf_name)).json():
            sync = SyncFiles()
            sync.config = {'jtracker_host':self.args.host,'jtracker_user':self.args.username,'jtracker_queue':queue['id'],'git_repo':self.args.git_local_repo}
            try:
                sync.run()
            except Exception as err:
                print(str(err))
        return