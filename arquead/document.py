from json import loads
from hashlib import sha256, md5
from os import sep, listdir
from os.path import basename


class Document:
    
    def __init__(self, path):
        self.__path = path
        
    def get_current_content(self):
        return self.read_file(self.get_current_version())

    def get_object_id(self):
        return basename(self.__path), self.get_current_version()
    
    def get_versions(self):
        versions = []
        for doc in listdir(self.__path):
            versions.append(int(doc[:-5]))
        
        versions.sort()
        return versions

    def get_current_version(self):
        return str(self.get_versions().pop())

    def get_path_by_version(self, version=None):
        return self.__path + sep + version + ".json"

    def read_file(self, version):
        doc = open(self.get_path_by_version(version), 'r')
        data = doc.read()
        doc.close()
        return loads(data)
    
    def sha256(self):
        return sha256(bytes(self.get_current_content(), 'utf-8')).hexdigest()
    
    def md5(self):
        return md5(bytes(self.get_current_content(), 'utf-8')).hexdigest()
