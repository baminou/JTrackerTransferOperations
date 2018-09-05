
from operation_types.docker_operation import Dockeroperation

class Download(Dockeroperation):

    @staticmethod
    def name():
        return "Download"

    @staticmethod
    def description():
        return "Download file from ICGC portal"

    def _parser(self, main_parser):
        return

    def _docker_container(self):
        return "quay.io/baminou/dckr_icgc_download"