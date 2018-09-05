
from operations.library import Library
from .upload import Upload
from .download import Download

class ICGC(Library):

    @staticmethod
    def name():
        return "icgc"

    @staticmethod
    def description():
        return "Not description provided"

    @staticmethod
    def operations():
        return {
            'upload': Upload,
            'download': Download
        }