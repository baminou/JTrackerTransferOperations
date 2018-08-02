


import logging

import ega_transfer
import csv
from operations.operation import Operation
import argparse

class ToStage(Operation):

    @staticmethod
    def name():
        return "to_stage"

    @staticmethod
    def description():
        return "Generate a list of files to be staged on EGA Aspera server"

    @staticmethod
    def parser(main_parser):
        main_parser.add_argument('-c', '--config', dest='config', required=True,  help="A valid configuration yaml file", type=argparse.FileType('r'))
        main_parser.add_argument('-a', '--audit', dest='audit', required=True)
        main_parser.add_argument('-o', '--output-file', dest='output_file', required=True)

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


    def _run(self,args):
        logging.info("Generate to stage for EGA Starts")

        logging.info("Load EGAFIDs")
        # Load all EGAFIDs from EGA aspera server
        ega_box_fids = ega_transfer.get_ega_box_fids(self._config.get('aspera_info').get('server'),self._config.get('aspera_info').get('user'))

        # Load all EGAFIDs from JTracker servers and repo
        jtracker_fids = ega_transfer.get_all_jtracker_egafids(self._config.get('etcd_jtracker').get('hosts'),self._config.get('old_jtracker').get('dirs'))

        # Load all EGAFIDs from the audit csv file
        audit_fids = ega_transfer.get_audit_fids(args.audit)

        to_stage = ega_transfer.get_files_to_stage(list(set(audit_fids) - set(ega_box_fids + jtracker_fids)), args.audit)
        with open(args.output_file, 'w') as fp:
            dict_writer = csv.DictWriter(fp, to_stage[0].keys(), delimiter='\t')
            dict_writer.writeheader()
            dict_writer.writerows(to_stage)