
from kernel.operation import Operation

import requests

class Listqueues(Operation):

    @staticmethod
    def name():
        return "list_queues"

    @staticmethod
    def description():
        return "List queue ids on jtracker"

    def _parser(self, main_parser):
        main_parser.add_argument(dest='jtracker_server')
        main_parser.add_argument(dest='port')
        main_parser.add_argument(dest='username')
        main_parser.add_argument(dest='workflow_name')
        return

    def _run(self):
        for queue in requests.get('%s:%s/api/jt-jess/v0.1/queues/owner/%s/workflow/%s' % (self.args.jtracker_server, self.args.port, self.args.username,self.args.workflow_name)).json():
            print(queue.get('id'))
        return
