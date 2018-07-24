
import subprocess
import os

class EGA:

    def __init__(self, aspera_host, aspera_user):
        self._aspera_host = aspera_host
        self._aspera_user = aspera_user

    def dbox(self):
        files = []
        dbox_filename = 'dbox_content'
        subprocess.check_output(['ascp','-QTl','100m','--ignore-host-key','--mode=recv','--host='+self._aspera_host,'--user='+self._aspera_user,dbox_filename,'/tmp'])
        with open(os.path.join('/tmp',dbox_filename), 'r') as f:
            for line in f.readlines():
                files.append(line.strip('\n'))
        os.remove(os.path.join('/tmp',dbox_filename))
        return files

    def dbox_egafids(self):
        ids = []
        for file in self.dbox():
            if file.endswith('.aes'):
                ids.append(file.split('/')[2].split('.')[0])
        return ids

    def retrieve_files(self, egafid):
        files = []
        for file in self.dbox():
            if egafid in file:
                files.append(file)
        return files
