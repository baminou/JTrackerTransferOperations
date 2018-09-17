from operations.ega.utils.ega_audit import EGAAudit
import json
import ega_transfer
import os
from operation_types.yml_config_operation import YmlConfigOperation
from ..utils import yes_or_no

class Job(YmlConfigOperation):

    @staticmethod
    def name():
        return "job"

    @staticmethod
    def description():
        return "Generate the job json files needed to run JTracker workflow"

    def _parser(self, main_parser):
        main_parser.add_argument('-a', '--audit', dest='audit', required=True, help="Path of the TSV file containing jobs that have to be generated.")
        main_parser.add_argument('-m', '--metadata-version', dest='metadata_version', required=True, help="Version of the metada repo to use in the job jsons")
        main_parser.add_argument('-r', '--metadata-repo', dest='metadata_repo', help="Metadata repository path without the version", required=False, default="https://raw.githubusercontent.com/icgc-dcc/ega-file-transfer/master/ega_xml/")
        main_parser.add_argument('-o', '--output', dest='output_dir', help="Output directory where to put the json files.", required=True)

    def _config_schema(self):
        return {
            "etcd_jtracker": {
                "type": "object",
                "properties": {
                    "hosts": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "url": {"type": "string"},
                                "queues": {
                                    "type": "array",
                                    "items": {
                                        "user": {"type": "string"},
                                        "id": {"type": "string"}
                                    },
                                    "required": ["user","id"]
                                },
                            },
                            "required": ['url','queues']
                        }
                    },
                    "required": ['hosts']
                }
            },
            "old_jtracker":{
                "type": "object",
                "properties":{
                    "dirs": {
                        "type": "array",
                        "items": {"type":"string"}
                    },
                    "required": ["dirs"]
                }
            },
            "metadata_repo": {"type": "string"},
            'aspera_info':{
                "type": "object",
                "properties": {
                    "server": {"type": "string"},
                    "user": {"type": "string"}
                }
            },
            "required": ["etcd_jtracker","old_jtracker",'aspera_info']
        }


    def _run(self):

        metadata_repo_url = self.args.metadata_repo+self.args.metadata_version

        #if not yes_or_no("This metadata URL (%s) is going to be inserted in the generated jsons. Okay?" % (metadata_repo_url)):
        #    return

        # Load all EGAFIDs from EGA aspera server
        ega_box_fids = ega_transfer.get_ega_box_fids(self.config.get('aspera_info').get('server'),self.config.get('aspera_info').get('user'))

        # Load all EGAFIDs from JTracker servers and repo
        jtracker_fids = ega_transfer.get_all_jtracker_egafids(self.config.get('etcd_jtracker').get('hosts'),self.config.get('old_jtracker').get('dirs'))

        # Load all EGAFIDs from the audit csv file
        audit_fids = ega_transfer.get_audit_fids(self.args.audit)

        #TODO Check the files that have to be staged and add a warning if not

        for id in audit_fids:
            if id in ega_box_fids and id not in jtracker_fids:
                job_name, job_data = EGAAudit(self.args.audit).get_job(id,metadata_repo_url)
                file_name = os.path.join(self.args.output_dir,job_name+".json")
                with open(file_name, 'w') as fp:
                    json.dump(job_data,fp,indent=4,sort_keys=True)