
from kernel.operation import Operation
import os
import requests
import json

class Dumpworkflowjobs(Operation):

    @staticmethod
    def name():
        return "Dumpworkflowjobs"

    @staticmethod
    def description():
        return "Dump all jobs from ETCD into multiple <queue>.jsonl"

    def _parser(self, main_parser):
        main_parser.add_argument(dest='username', help="Username")
        main_parser.add_argument(dest='wf_name', help="Workflow name")
        main_parser.add_argument(dest='jt_server', help="JTracker server URL")
        main_parser.add_argument('-o', '--output', dest='output_dir', help="Output directory where to dump <queues>.jsonl", required=True)

    def get_workflows(self, jt_server, username):
        print('%s/api/jt-wrs/v0.1/workflows/owner/%s' % (jt_server, username))
        return requests.get('%s/api/jt-wrs/v0.1/workflows/owner/%s' % (jt_server, username)).json()

    def get_queues(self, jt_server, username, wf_name):
        return requests.get('%s/api/jt-jess/v0.1/queues/owner/%s/workflow/%s' % (jt_server, username, wf_name)).json()

    def get_jobs(self, jt_server, username, queue_id):
        return requests.get('%s/api/jt-jess/v0.1/jobs/owner/%s/queue/%s' % (jt_server, username, queue_id)).json()

    def _run(self):
        if not os.path.isdir(self.args.output_dir):
            os.mkdir(self.args.output_dir)

        for queue in self.get_queues(self.args.jt_server,self.args.username,self.args.wf_name):
            print(queue.get('id'))
            with open(os.path.join(self.args.output_dir, queue.get('id') + '.jsonl'), 'w') as fp:
                for job in self.get_jobs(self.args.jt_server,self.args.username, queue.get('id')):
                    json.dump(job, fp)
                    fp.writelines('\n')
