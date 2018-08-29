import os
from arquea.error import ReturnMessage, Error
from arquea.files import CheckDB, InterpretFileConf, NewFileConf
from arquea.data import Collection, CreateCollection, NewDocument, SearchDocument, RemoveDocument
class Arquea(Error):

    def connect(self, directory):
        self.directory = directory

        if not self.directory[-1:] == '/':
            self.directory = directory+'/'
        
        if not os.path.isdir(self.directory):
            return ReturnMessage(self.directory, 404).show()
        
        db = CheckDB(self.directory)
        if not db.check():
            return ReturnMessage(self.directory, 408).show()

        conf = InterpretFileConf(self.directory)
        conf.start()
        if conf.error_status():
            return ReturnMessage(self.directory+'conf.arquea', 302).show()
        
        if not 'version' in conf.get_data():
            return ReturnMessage(self.directory+'conf.arquea', 301).show()
        if not conf.get_data()['version']:
            return ReturnMessage(self.directory+'conf.arquea', 301).show()
        
        self.conf = conf.get_data()
        return ReturnMessage(self.directory, 200).show()
    
    def get_collections(self):
        return CheckDB(self.directory).get_collections()
    
    def get_db_info(self):
        return self.conf
    
    def get_last_err(self):
        return ReturnMessage(self.directory, self.error_code()).show()
    
    def create_database(self, name = None):
        if not name:
            return ReturnMessage(name, 501).show()
        if not name in os.listdir():
            os.mkdir(name)
            name = name+'/'
            create_file = NewFileConf(name).create()
            return ReturnMessage(name, 200).show()
        return ReturnMessage(name, 505).show()
    
    def create_collection(self, name = None):
        new = CreateCollection(self.directory)
        new.new(name)
        if new.error_status():
            return ReturnMessage(self.directory, new.error_code()).show()
        return ReturnMessage(self.directory, 200).show()
    
    collection = None

    def set_collection(self, collection = None):
        if not collection:
            self.collection = None
            return ReturnMessage(self.directory, 501).show()
        if not collection in self.get_collections():
            self.collection = None
            return ReturnMessage(self.directory, 406).show()
        self.collection = collection
        return ReturnMessage(self.directory, 200).show()
    
    def get_documents(self):
        if not self.collection:
            self.set_status_error(True, 501)
            return []
        if not self.collection in self.get_collections():
            self.set_status_error(True, 406)
            return []
        return Collection(self.directory, self.collection).get_documents()
    
    def insert_one(self, data = None):
        if not self.collection or not data:
            return ReturnMessage(self.directory, 501).show()
        if not self.collection in self.get_collections():
            return ReturnMessage(self.directory, 406).show()
        insert = NewDocument(self.directory, self.collection)
        insert.insert_one(data)
        if insert.error_status():
            return ReturnMessage(self.directory, insert.error_code()).show()
        return ReturnMessage(self.directory, 200).show()
    
    def find_document(self, value = None, key = None, limit = 0):
        if not self.collection:
            self.set_status_error(True, 501)
            return []
        if not CheckDB(self.directory).check_collection_exists(self.collection):
            self.set_status_error(True, 406)
            return []
        if not value:
            self.set_status_error(True, 501)
            return []
        if not key:
            return self.set_status_error(True, 501)
        return SearchDocument(self.directory, self.collection).value_in_key(value, key, limit)
    
    def update(self, value = None, key = None, data = None, limit = 1):
        if not self.collection:
            self.set_status_error(True, 501)
            return []
        if not CheckDB(self.directory).check_collection_exists(self.collection):
            self.set_status_error(True, 406)
            return []
        if not value:
            self.set_status_error(True, 501)
            return []
        if not key:
            return self.set_status_error(True, 501)
        if not data:
            return self.set_status_error(True, 501)
        results = NewDocument(self.directory, self.collection)
        data = results.update_many(value, key, data, limit)
        if results.error_status():
            self.set_status_error(results.error_status(), results.error_code())
            return data
        return data

    def remove(self, value = None, key = None, limit = 1):
        if not self.collection:
            self.set_status_error(True, 501)
            return []
        if not CheckDB(self.directory).check_collection_exists(self.collection):
            self.set_status_error(True, 406)
            return []
        if not value:
            self.set_status_error(True, 501)
            return []
        if not key:
            return self.set_status_error(True, 501)
        results = RemoveDocument(self.directory, self.collection)
        data = results.remove_many(value, key, limit)
        if results.error_status():
            self.set_status_error(results.error_status(), results.error_code())
            return data
        return data