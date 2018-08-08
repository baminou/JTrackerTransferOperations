from operation_types.operation import Operation
from entities.ega import EGA

class Dbox(Operation):

    @staticmethod
    def name():
        return "dbox"

    @staticmethod
    def description():
        return "List all files on EGA Aspera server"

    def _parser(self, main_parser):
        main_parser.add_argument(dest='aspera_server')
        main_parser.add_argument(dest='aspera_user')

    def _run(self):
        ega = EGA(self.args.aspera_server, self.args.aspera_user)
        for file in ega.dbox():
            print(file)