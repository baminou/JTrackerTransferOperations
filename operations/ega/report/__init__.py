
from operation_types.yml_config_operation import YmlConfigOperation
import csv
import ega_transfer
import time
import matplotlib
#matplotlib.use('TkAgg')
#matplotlib.use('agg')
import matplotlib.pyplot as plt
import numpy as np
from argparse import FileType



class Report(YmlConfigOperation):

    @staticmethod
    def name():
        return "Report"

    @staticmethod
    def description():
        return "Create a visual report of the EGA transfer"

    def _config_schema(self):
        return {
            "aspera_info": {
                "type": "object",
                "properties": {
                    "server": {"type": "string"},
                    "user": {"type":"string"}
                },
                "required": ['server','user']
            },
            "required": ['aspera_info']
        }

    def _parser(self, main_parser):
        main_parser.add_argument('tsv',help='Audit TSV file', type=FileType('r'))
        return

    def _run(self):

        files = dict()
        reader = csv.DictReader(self.args.tsv, delimiter='\t')

        for row in reader:
            egafid = row.get('EGA File Accession')
            study = row.get('ICGC DCC Project Code')
            file_size = row.get('File Size')
            type = row.get('File Type')
            sss = row.get('ICGC Submitted Sequencing Strategy')
            files[egafid] = {'study':study,'size':file_size,'type':type,'sequencing_strategy':sss}

        ega_box_fids = ega_transfer.get_ega_box_fids(self.config.get('aspera_info').get('server'),self.config.get('aspera_info').get('user'))
        jtracker_fids_failed = ega_transfer.get_all_jtracker_egafids(self.config.get('etcd_jtracker').get('hosts'),self.config.get('old_jtracker').get('dirs'),['failed'])
        jtracker_fids_completed = ega_transfer.get_all_jtracker_egafids(self.config.get('etcd_jtracker').get('hosts'),self.config.get('old_jtracker').get('dirs'),['completed'])
        jtracker_fids_backlog = ega_transfer.get_all_jtracker_egafids(self.config.get('etcd_jtracker').get('hosts'),self.config.get('old_jtracker').get('dirs'),['backlog'])
        jtracker_fids_running = ega_transfer.get_all_jtracker_egafids(self.config.get('etcd_jtracker').get('hosts'),self.config.get('old_jtracker').get('dirs'),['running'])
        jtracker_fids_resume = ega_transfer.get_all_jtracker_egafids(self.config.get('etcd_jtracker').get('hosts'),self.config.get('old_jtracker').get('dirs'),['resume'])
        jtracker_fids_queued = ega_transfer.get_all_jtracker_egafids(self.config.get('etcd_jtracker').get('hosts'),self.config.get('old_jtracker').get('dirs'),['queued'])


        completed = 0
        backlog = 0
        failed = 0
        resume = 0
        queued = 0
        running = 0
        undefined = 0
        staged = 0
        for egafid in files:
            if egafid in jtracker_fids_failed:
                failed+=1
            elif egafid in jtracker_fids_backlog:
                backlog+=1
            elif egafid in jtracker_fids_completed:
                completed+=1
            elif egafid in jtracker_fids_resume:
                resume+=1
            elif egafid in jtracker_fids_queued:
                queued+=1
            elif egafid in jtracker_fids_running:
                running+=1
            elif egafid in ega_box_fids:
                staged+=1
            else:
                undefined+=1

        labels = 'completed', 'backlog', 'failed', 'resume', 'queued', 'running', 'undefined', 'staged'
        sizes = [completed, backlog, failed, resume, queued, running, undefined, staged]

        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
                shadow=False, startangle=90)

        plt.show()
        return True
