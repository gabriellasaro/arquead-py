import os, json
from random import randint
from arquea.error import Error
from arquea.files import CheckDB
from arquea.tools import TypeDir
class Collection():

    def __init__(self, directory, collection, dc = False):
        if not dc:
            self.collection_directory = directory+collection+TypeDir().bar_type()
        else:
            self.collection_directory = directory
        
    def get_documents(self):
        return tuple(os.listdir(self.collection_directory))

class CreateCollection(Error):

    def __init__(self, directory):
        self.list_dir = CheckDB(directory).get_collections()
        self.directory = directory
    
    def new(self, name = None):
        if not name:
            return self.set_status_error(True, 501)
        
        if not name in self.list_dir:
            os.mkdir(self.directory+name)
            check = CheckDB(self.directory).get_collections()
            if not name in check:
                return self.set_status_error(True, 502)
        else:
            return self.set_status_error(True, 503)

class Document(Collection):

    def write_file(self, objectId, data):
        file_name = str(objectId)+'.json'
        with open(self.collection_directory+file_name, 'w') as document:
            document.write(json.dumps(data))
            document.close()

class NewDocument(Document):
    
    def insert_one(self, data):
        return self.insert(data)
    
    def insert_many(self, data):
        info = []
        for x in data:
            info.append(self.insert(x))
        return tuple(info)
    
    def insert(self, data):
        if not '_id' in data:
            objectId = self.auto_object_id()
            data['_id'] = objectId
        else:
            data['_id'] = str(data['_id']).replace(' ', '_')
            objectId = data['_id']
            if str(objectId)+'.json' in self.get_documents():
                return {'status':503, 'objectId':objectId}
        self.write_file(objectId, data)
        return {'status':200, 'objectId':objectId}
    
    def auto_object_id(self):
        while True:
            objectId = randint(100000000000, 999999999999)
            if not str(objectId)+'.json' in self.get_documents():
                break
        return objectId

class UpdateDocument(Document, Error):

    def update_many(self, value, key, data, limit = 1):
        if '_id' in data:
            self.set_status_error(True, 508)
            return {'success':0, 'total':0, 'objectId_success':[]}
        documents = SearchDocument(self.collection_directory, 0, True).value_in_key(value, key, limit)
        results = {'success':0, 'total':len(documents), 'objectId_success':[]}
        if not documents:
            self.set_status_error(True, 506)
            return results
        for doc in documents:
            objectId = doc['_id']
            doc.update(data)
            self.write_file(objectId, doc)
            results['success']+=1
            results['objectId_success'].append(objectId)
        return results

class SearchDocument(Collection):

    def value_in_key(self, value, key, limit = 0):
        if len(key)==1:
            if key[0] == '_id':
                file_dir = str(value)+'.json'
                if file_dir in self.get_documents():
                    return (self.get_data_file(file_dir),)
                else:
                    return ()
            else:
                results = 0
                data_documents = []
                for document in self.get_documents():
                    data = self.get_data_file(document)
                    if key[0] in data:
                        if data[key[0]] == value:
                            data_documents.append(data)
                            results+=1
                            if limit>0:
                                if results == limit:
                                    break
                return tuple(data_documents)
        else:
            results = 0
            data_documents = []
            for document in self.get_documents():
                data = self.get_data_file(document)
                a = 0
                value2 = None
                for n in key:
                    if a == 0:
                        a=1
                        if n in data:
                            value2 = data[n]
                        else:
                            break
                    else:
                        if type(value2) is int:
                            value2 = None
                            break
                        if type(value2) is str:
                            value2 = None
                            break
                        if type(value2) is list:
                            if n>(len(value2)-1) or n<0:
                                break
                            value2 = value2[n]
                        else:
                            if n in value2:
                                value2 = value2[n]
                if value == value2:
                    if limit>0:
                        if results == limit:
                            break
                    data_documents.append(data)
                    results+=1
            return tuple(data_documents)
    
    def get_data_file(self, file_dir):
        dFile = open(self.collection_directory+file_dir, 'r')
        data = dFile.read()
        dFile.close()
        return json.loads(data)

class RemoveDocument(Collection, Error):

    def remove_many(self, value, key, limit = 1):
        documents = SearchDocument(self.collection_directory, 0, True).value_in_key(value, key, limit)
        results = {'success':0, 'total':len(documents), 'objectId_success':[]}
        for doc in documents:
            objectId = str(doc['_id'])+'.json'
            os.remove(self.collection_directory+objectId)
            results['success']+=1
            results['objectId_success'].append(doc['_id'])
        return results
