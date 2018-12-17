
from kernel.operation import Operation
import subprocess
from shutil import which
from termcolor import colored

class Command(Operation):

    @staticmethod
    def name():
        return "Command"

    @staticmethod
    def description():
        return "Run any command from the terminal"

    def _parser(self, main_parser):
        main_parser.add_argument('command', help="Command to be run")
        return

    def _run(self):
        if which(self.args.command) is None:
            print(colored("Command %s doest not exist in the system." % (self.args.command),'red'))
            return
        proc = subprocess.Popen([self.args.command]+ self.unknown_args,shell=False)
        proc.communicate()
        proc.kill()