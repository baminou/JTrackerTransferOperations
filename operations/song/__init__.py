

from ..library import Library
from .UnpublishAnalysis import Unpublishanalysis
from .validate_payload import Validatepayload
from .get_analysis import Getanalysis
from .upload_song_payload import Uploadsongpayload
from .upload import Upload

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
            'get_analysis': Getanalysis,
            'upload_payload': Uploadsongpayload,
            'upload': Upload
        }