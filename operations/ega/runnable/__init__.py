
from operations.operation import Operation
import os
import json
from entities.ega import EGA

class Runnable(Operation):

    @staticmethod
    def name():
        return "Runnable"

    @staticmethod
    def description():
        return "List the jobs that can be run from a Github Repository"

    @staticmethod
    def parser(main_parser):
        main_parser.add_argument('job_directory', help="Directory containing .json job files.")
        main_parser.add_argument('aspera_host', help="EGA Aspera host")
        main_parser.add_argument('aspera_user', help="EGA Aspera user")

    @staticmethod
    def _run(args):
        job_dir = args.job_directory
        aspera_host = args.aspera_host
        aspera_user = args.aspera_user

        ega = EGA(aspera_host, aspera_user)
        dbox = ega.dbox_egafids()

        for file in os.listdir(job_dir):
            if file.endswith('.json'):
                is_runnable = True
                with open(os.path.join(job_dir,file), 'r') as fp:
                    data = json.load(fp)
                    study = data.get('project_code')
                    for file_obj in data.get('files'):
                        if not file_obj.get('ega_file_id') in dbox:
                            is_runnable = False
                if is_runnable:
                    print(file)
