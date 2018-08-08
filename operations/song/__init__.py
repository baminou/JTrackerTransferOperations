

from ..library import Library
from .UnpublishAnalysis import Unpublishanalysis
from .validate_payload import Validatepayload
from .get_analysis import Getanalysis

class Song(Library):

    @staticmethod
    def name():
        return "song"

    @staticmethod
    def description():
        return "SONG recurrent operations"

    @staticmethod
    def parser(main_parser):
        return

    @staticmethod
    def operations():
        return {
            'unpublish_analysis': Unpublishanalysis,
            'validate_payload': Validatepayload,
            'get_analysis': Getanalysis
        }