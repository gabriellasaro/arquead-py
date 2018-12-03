import os
from arquea.error import Error
from arquea.info import InfoArquea
from arquea.tools import TypeDir
class CheckDB:

    def __init__(self, directory):
        self.directory = directory
    
    def check(self):
        file_name = 'conf.arquea'
        if os.path.exists(self.directory+file_name) and not os.path.exists(self.directory+file_name+TypeDir().bar_type()):
            return True
        return False
    
    def get_collections(self):
        items = os.listdir(self.directory)
        collections = []
        for x in items:
            if os.path.isdir(self.directory+x):
                collections.append(x)
        return tuple(collections)

    def check_collection_exists(self, collection):
        if collection in self.get_collections():
            return True
        return False

class InterpretFileConf(Error):

    def __init__(self, directory):
        self.directory_file = directory+'conf.arquea'
        self.list_var = ['VERSION']
        self.name_var = {'VERSION':'version'}
        self.info = {}
    
    def start(self):
        self.open_file()
        self.clear()
        if not self.error_status():
            self.info = self.format_data()
    
    def get_data(self):
        return self.info
    
    def open_file(self):
        dFile = open(self.directory_file, 'r')
        data = dFile.readlines()
        dFile.close()
        self.raw_data = data
    
    def clear(self):
        x = 0
        n = len(self.raw_data)
        data = []
        while x<n:
            self.raw_data[x] = self.raw_data[x].strip().replace(' ', '')
            if len(self.raw_data[x])==0:
                x+=1
                continue
            pre = self.raw_data[x].split('=')
            if len(pre)!=2:
                self.set_status_error(True)
                break
            if not pre[0] in self.list_var:
                self.set_status_error(True)
            data.append(pre)
            x+=1
        self.data = data
    
    def format_data(self):
        info = {}
        for x in self.data:
            info[self.name_var[x[0]]] = x[1]
        return info

class NewFileConf():

    def __init__(self, directory):
        self.directory = directory
    
    def create(self):
        file_name = 'conf.arquea'
        data = 'VERSION = {}'.format(InfoArquea().get_version())
        with open(self.directory+file_name, 'w') as document:
            document.write(data)