

from ..library import Library
from .job import Job
from .dbox import Dbox
from .to_stage import ToStage
from .to_delete import ToDelete

class EGA(Library):

    @staticmethod
    def name():
        return "ega"

    @staticmethod
    def description():
        return "EGA Transfer to collaboratory operations"

    @staticmethod
    def parser(main_parser):
        return

    @staticmethod
    def operations():
        return {
            'job': Job,
            'dbox': Dbox,
            'to_stage': ToStage,
            'to_delete': ToDelete
        }