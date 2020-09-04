from os import path, listdir, mkdir, sep
from os.path import normpath
from arquead.info import Version
class Arquea():

    def __init__(self):
        self.number_status = 0
        self.db_dir = None
        
    def connect_level(self):
        return self.number_status
    
    def valid_connect(func):
        def check(self, *args, **kwargs):
            if self.number_status!=2:
                return {'status':509, 'success':False}
            return func(self, *args, **kwargs)
        return check
    
    # def error(self, error, success):
    #     return {'status':error, 'success':success}
    
    def connect(self, db_dir = None, collection = None):
        if not db_dir:
            return {'status':404, 'success':False}
        
        if not db_dir[-1:] == '/' and not db_dir[-1:] == '\\':
            db_dir = db_dir+sep
        
        if not path.isdir(db_dir):
            return {'status':404, 'success':False}
        
        self.db_dir = normpath(db_dir)
        # Check BD
        if not '_arquea' in self.get_collections():
            return {'status':5000, 'success':False}
        data = FindDocuments(db_dir+'_arquea/').value_in_key('conf', ['_id'], 1)
        if not data:
            return {'status':5001, 'success':False}
        
        if not data[0]['version'] in Version().get_compatible():
            return {'status':5002, 'success':False, 'message':'Imcompatível'}
        
        self.conf = data[0]
        self.number_status = 1
        
        if collection:
            return self.set_collection(collection)
        return {'status':200, 'success':True}
    
    def create_database(self, db_dir = None):
        if type(db_dir) is not str:
            return {'status':501, 'success':False}
        if not path.exists(db_dir):
            if not db_dir[-1:] == '/' or not db_dir[-1:] == '\\':
                db_dir = db_dir+sep
            
            mkdir(db_dir)
            collection = db_dir+'_arquea/'
            self.number_status = 1
            self.db_dir = db_dir
            if self.create_collection('_arquea')['success']:
                new = NewDocument(collection).insert_one({
                    '_id':'conf',
                    'version':Version().__str__()
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
        return tuple(listdir(self.db_dir))

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
    
    # @valid_connect
    # def checksum_sha256(self, object_id):
    #     return CheckSum(self.collection_dir, object_id).sha256()

    # @valid_connect
    # def checksum_md5(self, object_id):
    #     return CheckSum(self.collection_dir, object_id).md5()
    
    # @valid_connect
    # def get_documents(self):
    #     return Documents(self.collection_dir).get_documents()
    
    # @valid_connect
    # def insert_one(self, data = None):
    #     if type(data) is not dict:
    #         return {'status':501}
    #     return NewDocument(self.collection_dir).insert_one(data)
    
    # @valid_connect
    # def insert_many(self, data = None):
    #     if not type(data) is list and not type(data) is tuple:
    #         return {'status':501}
    #     return NewDocument(self.collection_dir).insert_many(data)
    
    # @valid_connect
    # def find_document(self, value = None, key = None, limit = 0):
    #     if value is None:
    #         return {'status':501}
    #     if type(key) is not list and type(key) is not tuple:
    #         return {'status':501}
    #     return FindDocuments(self.collection_dir).value_in_key(value, key, limit)
    
    # @valid_connect
    # def update(self, value = None, key = None, data = None, limit = 1):
    #     if value is None:
    #         return {'success':0, 'total':0, 'objectId_success':[]}
    #     if type(key) is not list and type(key) is not tuple:
    #         return {'success':0, 'total':0, 'objectId_success':[]}
    #     if type(data) is not dict:
    #         return {'success':0, 'total':0, 'objectId_success':[]}
    #     return UpdateDocument(self.collection_dir).update_many(value, key, data, limit)
    
    # @valid_connect
    # def remove(self, value = None, key = None, limit = 1):
    #     if value is None:
    #         return {'success':0, 'total':0, 'objectId_success':[]}
    #     if type(key) is not list and type(key) is not tuple:
    #         return {'success':0, 'total':0, 'objectId_success':[]}
    #     return RemoveDocument(self.collection_dir).remove_many(value, key, limit)