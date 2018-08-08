from operations.ega.utils.ega_audit import EGAAudit
import json
import ega_transfer
import os
from operation_types.yml_config_operation import YmlConfigOperation
import argparse

class Job(YmlConfigOperation):

    @staticmethod
    def name():
        return "job"

    @staticmethod
    def description():
        return "Generate the job json files needed to run JTracker workflow"

    def _parser(self, main_parser):
        main_parser.add_argument('-c', '--config', dest='config', required=True, help="A valid configuration yaml file", type=argparse.FileType('r'))
        main_parser.add_argument('-a', '--audit', dest='audit', required=True)
        main_parser.add_argument('-o', '--output', dest='output_dir', required=True)

    def _schema(self):
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
            "required": ["etcd_jtracker","old_jtracker","metadata_repo",'aspera_info']
        }


    def _run(self):

        # Load all EGAFIDs from EGA aspera server
        ega_box_fids = ega_transfer.get_ega_box_fids(self.config.get('aspera_info').get('server'),self.config.get('aspera_info').get('user'))

        # Load all EGAFIDs from JTracker servers and repo
        jtracker_fids = ega_transfer.get_all_jtracker_egafids(self.config.get('etcd_jtracker').get('hosts'),self.config.get('old_jtracker').get('dirs'))

        # Load all EGAFIDs from the audit csv file
        audit_fids = ega_transfer.get_audit_fids(self.args.audit)

        for id in audit_fids:
            if id in ega_box_fids and id not in jtracker_fids:
                job_name, job_data = EGAAudit(self.args.audit).get_job(id,self.config.get('metadata_repo'))
                file_name = os.path.join(self.args.output_dir,job_name+".json")
                with open(file_name, 'w') as fp:
                    json.dump(job_data,fp,indent=4,sort_keys=True)