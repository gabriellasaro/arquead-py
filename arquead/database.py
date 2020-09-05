from os import mkdir, listdir
from os.path import isdir, normpath, exists, join
from arquead.collection import Collection
from arquead.error import Error
from arquead.info import Version

class Database:

    def __init__(self, path):
        self.__path = normpath(path)
    
    def is_arquead(self):
        if type(self.__path) is not str:
            return False
        
        if not isdir(self.__path):
            return False
    
    def get_collections(self):
        return tuple(listdir(self.__path))
    
    def create_collection(self, name=None):
        if type(name) is not str:
            return Error("Parâmetro inválido ou nulo")
        if name in self.get_collections():
            return Error("Já existe uma coleção com este nome.")
        
        mkdir(join(self.__path, name))

        if not name in self.get_collections():
            return Error("Erro ao criar diretório para coleção.")
        return Error()
    
    def create_database(self):
        if type(self.__path) is not str:
            return Error("Parâmetro inválido ou nulo")
        
        if exists(self.__path):
            return Error("Já existe um diretório com este nome.")

        mkdir(self.__path)

        err = self.create_collection('_arquea')
        if err.success():
            collection = Collection(self.__path)
            new = collection.insert({
                'id': 'conf',
                'version': Version()
            })
            if new[1].err():
                return Error("Não foi possível criar arquivo de configuração.")
            return Error()
        return err
