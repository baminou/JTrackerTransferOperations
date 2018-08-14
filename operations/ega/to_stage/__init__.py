


import logging

import ega_transfer
import csv
from operation_types.yml_config_operation import YmlConfigOperation
import argparse

class ToStage(YmlConfigOperation):

    @staticmethod
    def name():
        return "to_stage"

    @staticmethod
    def description():
        return "Generate a list of files to be staged on EGA Aspera server"

    def _parser(self, main_parser):
        main_parser.add_argument('-a', '--audit', dest='audit', required=True)
        main_parser.add_argument('-t', '--ega_entity_type', dest='ega_entity_type', required=True, help="This argument only accept one of two values: run or analysis", choices=['run','analysis'])
        main_parser.add_argument('-o', '--output-file', dest='output_file', required=True)

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
        logging.info("Generate to stage for EGA Starts")

        logging.info("Load EGAFIDs")
        # Load all EGAFIDs from EGA aspera server
        ega_box_fids = ega_transfer.get_ega_box_fids(self.config.get('aspera_info').get('server'),self.config.get('aspera_info').get('user'))

        # Load all EGAFIDs from JTracker servers and repo
        jtracker_fids = ega_transfer.get_all_jtracker_egafids(self.config.get('etcd_jtracker').get('hosts'),self.config.get('old_jtracker').get('dirs'))

        # Load all EGAFIDs from the audit csv file
        audit_fids = ega_transfer.get_audit_fids(self.args.audit)

        to_stage = ega_transfer.get_files_to_stage(list(set(audit_fids) - set(ega_box_fids + jtracker_fids)), self.args.audit, self.args.ega_entity_type)
        with open(self.args.output_file, 'w') as fp:
            dict_writer = csv.DictWriter(fp, to_stage[0].keys(), delimiter='\t')
            dict_writer.writeheader()
            dict_writer.writerows(to_stage)
