
from kernel.library import Library
from .sync_files import SyncFiles
from .list_analysis_ids import Listanalysisids

class Minibam(Library):

    @staticmethod
    def name():
        return "minibam"

    @staticmethod
    def description():
        return "Minibam generation on Collaboratory operations"

    @staticmethod
    def parser(main_parser):
        return

    @staticmethod
    def operations():
        return {
            'sync': SyncFiles,
            'list:analysis': Listanalysisids
        }