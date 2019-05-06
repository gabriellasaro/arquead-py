from os import path, listdir, mkdir
from arquea.documents import NewDocument
from tools import bar_type



# from arquea.error import ReturnMessage
# from arquea.conf import InterpretConfFile, NewConfFile

# from arquea.data import Collection, CreateCollection, NewDocument, UpdateDocument, SearchDocument, RemoveDocument
# from arquea.checksum import CheckSum

# from arquea.info import VersionArquea
class Arquea():

    def __init__(self):
        self.number_status = 0
        self.db_dir = None
        
    def connect_level(self):
        return self.number_status
    
    def valid_connect(self, func):
        def check(*args, **kwargs):
            if self.number_status!=2:
                return {'status':509, 'success':False}
            return func(*args, **kwargs)
        return check
    
    def error(self, error, success):
        return {'status':error, 'success':success}
    
    def connect(self, db_dir = None, collection = None):
        if not db_dir:
            return {'status':404, 'success':False}
        
        if not db_dir[-1:] == '/' or not db_dir[-1:] == '\\':
            directory = directory+bar_type()
        
        if not path.isdir(db_dir):
            return {'status':404, 'success':False}
        
        # db = CheckDB(directory)
        # if not db.check():
        #     return ReturnMessage(408).show()

        # conf = InterpretConfFile(directory)
        # conf.start()
        # if not conf.valid_action():
        #     return ReturnMessage(302).show()
        
        # if not 'version' in conf.data_conf:
        #     return ReturnMessage(301).show()
        
        # # Verifica se a versão do banco de dados é compatível com a lib.
        # if not conf.data_conf['version'] in VersionArquea().get_compatible():
        #     return ReturnMessage(202).show()
        
        # self.conf = conf.data_conf
        self.conf = {'version':'0.3.0'}

        self.db_dir = db_dir

        self.number_status = 1
        
        if collection:
            return self.set_collection(collection)
        return {'status':200, 'success':True}
    
    # Tudo certo daqui para baixo.
    def create_database(self, name = None):
        if type(name) is not str:
            return {'status':501, 'success':False}
        if not path.exists(name):
            mkdir(name)
            name = name+bar_type()+'_arquea'
            self.number_status = 1
            if self.create_collection('_arquea')['success']:
                new = NewDocument(name+'_arquea').insert_one({
                    '_id':'conf',
                    'version':'0.3.0'
                })
                if new['success']:
                    return {'status':200, 'success':True}
            return {'status':500, 'success':False}
        return {'status':500, 'success':False}
    
    def get_conf(self):
        return self.conf
    
    def get_current_directory(self):
        return self.db_dir
    
    def get_collections(self):
        return tuple(listdir())

    def create_collection(self, name = None):
        if self.connect_level()==0:
            return {'status':506, 'success':False}
        if type(name) is not str:
            return {'status':501, 'success':False}
        
        if not name in self.get_collections():
            mkdir(self.db_dir+name)
            if not name in self.get_collections():
                return {'status':500, 'success':False}
            return {'status':200, 'success':True}
        return {'status':500, 'success':False}
    
    def set_collection(self, collection = None):
        if self.connect_level()==0:
            return {'status':501, 'success':False}
        if not collection in self.get_collections():
            self.collection = None
            return {'status':406, 'success':False}
        self.collection = collection
        self.collection_dir = self.db_dir+collection+"/"
        self.number_status = 2
        return {'status': 200, 'success':True}
    
    def get_current_collection(self):
        return self.collection
    
    
    # Tudo certo até aqui.


    
    # def get_last_err(self):
    #     return ReturnMessage(self.error_code()).show()

    def checksum_sha256(self, objectId):
        if not self.valid_connect():
            self.set_status_error(True, 509)
            return {'total':0}
        check = CheckSum(self.db_dir, self.collection)
        result = check.get_sha256(objectId)
        if check.error_status():
            self.set_status_error(True, check.error_code())
            return {'total':0}
        return result
    
    def get_documents(self):
        if not self.valid_connect():
            self.set_status_error(True, 509)
            return ()
        return Collection(self.db_dir, self.collection).get_documents()

    def insert_one(self, data = None):
        if type(data) is not dict:
            self.set_status_error(True, 501)
            return {'status':501, 'objectId':None}
        if not self.valid_connect():
            self.set_status_error(True, 509)
            return {'status':509, 'objectId':None}
        insert = NewDocument(self.db_dir, self.collection)
        return insert.insert_one(data)

    def insert_many(self, data = None):
        if not self.valid_connect():
            self.set_status_error(True, 509)
            return ()
        if not type(data) is list and not type(data) is tuple:
            self.set_status_error(True, 501)
            return ()
        insert = NewDocument(self.db_dir, self.collection)
        return insert.insert_many(data)

    def find_document(self, value = None, key = None, limit = 0):
        if not self.valid_connect():
            self.set_status_error(True, 509)
            return ()
        if value is None:
            self.set_status_error(True, 501)
            return ()
        if type(key) is not list and type(key) is not tuple:
            self.set_status_error(True, 501)
            return ()
        return SearchDocument(self.db_dir, self.collection).value_in_key(value, key, limit)
    
    def update(self, value = None, key = None, data = None, limit = 1):
        if not self.valid_connect():
            self.set_status_error(True, 509)
            return {'success':0, 'total':0, 'objectId_success':[]}
        if value is None:
            self.set_status_error(True, 501)
            return {'success':0, 'total':0, 'objectId_success':[]}
        if type(key) is not list and type(key) is not tuple:
            self.set_status_error(True, 501)
            return {'success':0, 'total':0, 'objectId_success':[]}
        if type(data) is not dict:
            self.set_status_error(True, 501)
            return {'success':0, 'total':0, 'objectId_success':[]}
        results = UpdateDocument(self.db_dir, self.collection)
        data = results.update_many(value, key, data, limit)
        if results.error_status():
            self.set_status_error(results.error_status(), results.error_code())
            return data
        return data

    def remove(self, value = None, key = None, limit = 1):
        if not self.valid_connect():
            self.set_status_error(True, 509)
            return {'success':0, 'total':0, 'objectId_success':[]}
        if value is None:
            self.set_status_error(True, 501)
            return {'success':0, 'total':0, 'objectId_success':[]}
        if type(key) is not list and type(key) is not tuple:
            self.set_status_error(True, 501)
            return {'success':0, 'total':0, 'objectId_success':[]}
        results = RemoveDocument(self.db_dir, self.collection)
        data = results.remove_many(value, key, limit)
        if results.error_status():
            self.set_status_error(results.error_status(), results.error_code())
            return data
        return data
