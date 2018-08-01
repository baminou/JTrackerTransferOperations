
import logging

from entities.ega_audit import EGAAudit
import json
import ega_transfer
import os
from operations.operation import Operation

class Job(Operation):
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
        logging.info("Generate jobs for EGA Starts")

        logging.info("Load EGAFIDs")
        # Load all EGAFIDs from EGA aspera server
        ega_box_fids = ega_transfer.get_ega_box_fids(self._config.get('aspera_info').get('server'),self._config.get('aspera_info').get('user'))

        # Load all EGAFIDs from JTracker servers and repo
        jtracker_fids = ega_transfer.get_all_jtracker_egafids(self._config.get('etcd_jtracker').get('hosts'),self._config.get('old_jtracker').get('dirs'))

        # Load all EGAFIDs from the audit csv file
        audit_fids = ega_transfer.get_audit_fids(args.audit)

        for id in audit_fids:
            if id in ega_box_fids and id not in jtracker_fids:
                job_name, job_data = EGAAudit(args.audit).get_job(id,self._config.get('metadata_repo'))
                logging.info(job_name)
                with open(os.path.join(args.output_dir,job_name+".json"), 'w') as fp:
                    json.dump(job_data,fp,indent=4,sort_keys=True)