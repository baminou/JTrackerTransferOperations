from operation_types.yml_config_operation import YmlConfigOperation
import logging
import ega_transfer
from entities.ega import EGA

class ToDelete(YmlConfigOperation):

    @staticmethod
    def name():
        return "to_delete"

    @staticmethod
    def description():
        return "Generate a list of files to be deleted on EGA Aspera server"

    def _parser(self, main_parser):
        main_parser.add_argument('-o', '--output-file', dest='output_file', required=True)

    def _config_schema(self):
        return {
            "jtracker_host": {"type": "string"},
            "jtracker_user": {"type": "string"},
            "queues": {
                "type": "array",
                "items": {"type": "string"}
            },
            "aspera_user": {"type": "string"},
            "aspera_host": {"type": "string"},
            "required": ["jtracker_host", "jtracker_user","queues","aspera_user", "aspera_host"]
        }

    def _run(self):
        logging.info("Generate a list of files to delete from the EGA Aspera server")

        logging.info("Get EGA box file IDs")
        ega_box_fids = ega_transfer.get_ega_box_fids(self.config.get('aspera_host'),self.config.get('aspera_user'))
        ega_completed_fids = []

        for queue in self.config.get('queues'):
            ega_completed_fids = ega_completed_fids + ega_transfer.get_etcd_jtracker_egafids(self.config.get('jtracker_host'),self.config.get('jtracker_user'),queue,'completed')

        ega = EGA(self.config.get('aspera_host'),self.config.get('aspera_user'))

        with open(self.args.output_file,'w') as fp:
            for fid in ega_box_fids:
                if fid in ega_completed_fids:
                    for file in ega.retrieve_files(fid):
                        fp.write(file+"\n")
