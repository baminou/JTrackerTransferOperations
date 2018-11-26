
from kernel.operation import Operation
import requests

class Publishstate(Operation):

    @staticmethod
    def name():
        return "Publishstate"

    @staticmethod
    def description():
        return "Check publish state of bundle on song server."

    def _parser(self, main_parser):
        main_parser.add_argument(dest='song', help="Song server in collab or aws", choices=['collab','aws'])
        main_parser.add_argument(dest='study', help="Study id")
        main_parser.add_argument(dest='bundle_id', help="Bundle id to check")
        return

    def _run(self):
        if self.args.song == "aws":
            song_url = "https://virginia.song.icgc.org"
        elif self.args.song == "collab":
            song_url = "https://song.cancercollaboratory.org"
        else:
            raise Exception("Choose a song server between aws and collab")
        state = requests.get("/".join([song_url,'studies',self.args.study,'analysis',self.args.bundle_id])).json().get('analysisState')
        print("%s\t%s\t%s" % (self.args.study, self.args.bundle_id,state))
        return state