import os
from arquea.error import ReturnMessage, Error
from arquea.files import CheckDB, InterpretFileConf, NewFileConf
from arquea.data import Collection, CreateCollection, NewDocument, UpdateDocument, SearchDocument, RemoveDocument
from arquea.checksum import CheckSum
from arquea.tools import TypeDir
class Arquea(Error):

    def __init__(self):
        self.number_status = 0
        self.directory = None
    
    def valid_connect(self):
        if self.number_status==2:
            return True
        return False
    
    def connect_level(self):
        return self.number_status
    
    def connect(self, directory = None, collection = None):
        if not directory:
            return ReturnMessage(404).show()
        self.directory = directory
        
        if not self.directory[-1:] == '/' or not self.directory[-1:] == '\\':
            self.directory = directory+TypeDir().bar_type()
        
        if not os.path.isdir(self.directory):
            return ReturnMessage(404).show()
        
        db = CheckDB(self.directory)
        if not db.check():
            return ReturnMessage(408).show()

        conf = InterpretFileConf(self.directory)
        conf.start()
        if conf.error_status():
            return ReturnMessage(302).show()
        
        if not 'version' in conf.get_data():
            return ReturnMessage(301).show()
        if not conf.get_data()['version']:
            return ReturnMessage(301).show()
        
        self.conf = conf.get_data()
        self.number_status = 1
        
        if collection:
            return self.set_collection(collection)
        return ReturnMessage(200).show()
    
    def get_current_directory(self):
        return self.directory
    
    def set_collection(self, collection = None):
        if self.connect_level()==0:
            return ReturnMessage(501).show()
        if not collection in self.get_collections():
            print(collection)
            print(self.get_collections())
            self.collection = None
            return ReturnMessage(406).show()
        self.collection = collection
        self.number_status = 2
        return ReturnMessage(200).show()
    
    def get_current_collection(self):
        return self.collection
    
    def get_collections(self):
        if not self.connect_level()>=1:
            return ()
        return CheckDB(self.directory).get_collections()
    
    def get_db_info(self):
        return self.conf
    
    def get_last_err(self):
        return ReturnMessage(self.error_code()).show()
    
    def create_database(self, name = None):
        if not name:
            return ReturnMessage(501).show()
        if not os.path.exists(name):
            os.mkdir(name)
            name = name+TypeDir().bar_type()
            NewFileConf(name).create()
            return ReturnMessage(200).show()
        return ReturnMessage(505).show()
    
    def create_collection(self, name = None):
        if self.connect_level()==0:
            return ReturnMessage(509).show()
        new = CreateCollection(self.directory)
        new.new(name)
        if new.error_status():
            return ReturnMessage(new.error_code()).show()
        return ReturnMessage(200).show()
    
    def checksum_sha256(self, objectId):
        if not self.valid_connect():
            self.set_status_error(True, 509)
            return {'total':0}
        check = CheckSum(self.directory, self.collection)
        result = check.get_sha256(objectId)
        if check.error_status():
            self.set_status_error(True, check.error_code())
            return {'total':0}
        return result
    
    def get_documents(self):
        if not self.valid_connect():
            self.set_status_error(True, 509)
            return ()
        return Collection(self.directory, self.collection).get_documents()

    def insert_one(self, data = None):
        if not self.valid_connect():
            self.set_status_error(True, 509)
            return {'status':509, 'objectId':None}
        insert = NewDocument(self.directory, self.collection)
        return insert.insert_one(data)

    def insert_many(self, data = None):
        if not self.valid_connect():
            self.set_status_error(True, 509)
            return ()
        if not type(data) is list and not type(data) is tuple:
            self.set_status_error(True, 501)
            return ()
        insert = NewDocument(self.directory, self.collection)
        return insert.insert_many(data)

    def find_document(self, value = None, key = None, limit = 0):
        if not self.valid_connect():
            self.set_status_error(True, 509)
            return ()
        if not value:
            self.set_status_error(True, 501)
            return ()
        if not key:
            self.set_status_error(True, 501)
            return ()
        return SearchDocument(self.directory, self.collection).value_in_key(value, key, limit)
    
    def update(self, value = None, key = None, data = None, limit = 1):
        if not self.valid_connect():
            self.set_status_error(True, 509)
            return {'success':0, 'total':0, 'objectId_success':[]}
        if not value:
            self.set_status_error(True, 501)
            return {'success':0, 'total':0, 'objectId_success':[]}
        if not key:
            self.set_status_error(True, 501)
            return {'success':0, 'total':0, 'objectId_success':[]}
        if not data:
            self.set_status_error(True, 501)
            return {'success':0, 'total':0, 'objectId_success':[]}
        results = UpdateDocument(self.directory, self.collection)
        data = results.update_many(value, key, data, limit)
        if results.error_status():
            self.set_status_error(results.error_status(), results.error_code())
            return data
        return data

    def remove(self, value = None, key = None, limit = 1):
        if not self.valid_connect():
            self.set_status_error(True, 509)
            return {'success':0, 'total':0, 'objectId_success':[]}
        if not value:
            self.set_status_error(True, 501)
            return {'success':0, 'total':0, 'objectId_success':[]}
        if not key:
            self.set_status_error(True, 501)
            return {'success':0, 'total':0, 'objectId_success':[]}
        results = RemoveDocument(self.directory, self.collection)
        data = results.remove_many(value, key, limit)
        if results.error_status():
            self.set_status_error(results.error_status(), results.error_code())
            return data
        return data
