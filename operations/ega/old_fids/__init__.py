
from operation_types.operation import Operation
from ..utils.github_jtracker import GithubJTracker
from ega_transfer import get_jtracker_fids
class Oldfids(Operation):

    @staticmethod
    def name():
        return "old_fids"

    @staticmethod
    def description():
        return "List all EGAFIDs in a JTracker repo"

    def _parser(self, main_parser):
        main_parser.add_argument(dest='repos', nargs='+')
        return

    def _run(self):
        jtracker = GithubJTracker(self.args.repos)
        for fid in get_jtracker_fids(jtracker):
            print(fid)
        return