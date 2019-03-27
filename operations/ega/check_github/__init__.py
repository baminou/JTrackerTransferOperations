
from kernel.operation import Operation
from ..utils.github_jtracker import GithubJTracker
from ..utils.song import get_analysis

class Checkgithub(Operation):

    @staticmethod
    def name():
        return "Checkgithub"

    @staticmethod
    def description():
        return "Check if jobs in github repo are published"

    def _parser(self, main_parser):
        main_parser.add_argument('--repos','-r',dest='repos', nargs='+',help="List of repos to check", required=True)
        main_parser.add_argument('--song','-s',dest='song', help='Song server to check against',required=True)
        return

    def _run(self):
        jt = GithubJTracker(self.args.repos)
        for job in jt.get_jobs():
            analysis = get_analysis(self.args.song,job.get('project_code'),job.get('bundle_id'))
            print(job.get('bundle_id')+'\t'+job.get('project_code')+'\t'+(analysis.get('analysisState') if not analysis.get('analysisState')==None else "ERROR"))
        pass