
from kernel.operation import Operation
from ..utils.etcd_jtracker import ETCDJTracker
from ega_transfer import get_jtracker_fids

class Newfids(Operation):

    @staticmethod
    def name():
        return "new_fids"

    @staticmethod
    def description():
        return "List all EGAFIDs in a JTracker server"

    def _parser(self, main_parser):
        main_parser.add_argument(dest='server')
        main_parser.add_argument(dest='user')
        main_parser.add_argument(dest='queues',nargs='+')

        return

    def _run(self):
        for queue in self.args.queues:
            jtracker = ETCDJTracker(self.args.server, self.args.user, queue)
            for fid in get_jtracker_fids(jtracker):
                print(fid)
        return