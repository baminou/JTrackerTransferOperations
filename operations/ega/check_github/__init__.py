
from kernel.operation import Operation
from ..utils.github_jtracker import GithubJTracker
from ..utils.song import get_analysis
from ..utils import project_allowed_on_aws
import sys

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
        main_parser.add_argument('--output','-o',dest='output', help='Song server to check against', required=False)
        main_parser.add_argument('--filter-aws',dest='filter_aws', help="Skip the studies not allowed on AWS", action='store_true')
        return

    def _run(self):
        jt = GithubJTracker(self.args.repos)

        handle = open(self.args.output, 'w') if self.args.output else sys.stdout

        for job in jt.get_jobs():
            if self.args.filter_aws and job.get('project_code') in project_allowed_on_aws():
                continue
            analysis = get_analysis(self.args.song,job.get('project_code'),job.get('bundle_id'))
            for f in job.get('files'):
                line = job.get('bundle_id') + '\t'+ f.get('ega_file_id') +'\t'+ job.get('project_code') + '\t' + (analysis.get('analysisState') if not analysis.get('analysisState') == None else "ERROR")
                print(line)
                handle.write(line+'\n')
        return