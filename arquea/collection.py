from os import listdir

class Collection:

    def __init__(self, path):
        self.__path = path
    
    def get_name(self):
        pass

    def get_documents(self):
        return tuple(listdir(self.__path))

    def get_path(self):
        return self.__path
