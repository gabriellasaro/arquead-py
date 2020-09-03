from json import loads
from hashlib import sha256, md5
from os import sep

class Document:
    
    def __init__(self, path):
        self.__path = path
    
    def get_content(self):
        pass

    def get_object_id(self):
        pass

    def get_versions(self):
        pass

    def get_current_version(self):
        pass

    def get_path_by_version(self, version = None):
        return self.__path + sep + version + ".json"

    def read_file(self, version):
        doc = open(self.get_path_by_version(version), 'r')
        data = doc.read()
        doc.close()
        return loads(data)
    
    def sha256(self, version = None):
        return sha256(bytes(self.read_file(version), 'utf-8')).hexdigest()
    
    def md5(self, version = None):
        return md5(bytes(self.read_file(version), 'utf-8')).hexdigest()