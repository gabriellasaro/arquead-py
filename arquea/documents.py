import json
from random import randint
from os import listdir, mkdir
from shutil import rmtree
from uuid import uuid4

class Documents:

    def __init__(self, collection_dir):
        self.collection_dir = collection_dir
    
    def get_documents(self):
        return tuple(listdir(self.collection_dir))

class NewDocument(Documents):
    
    def auto_object_id(self):
        return str(uuid4())
    
    def insert_one(self, data):
        return self.insert(data)
    
    def insert_many(self, data):
        result = []
        for item in data:
            result.append(self.insert(item))
        return tuple(result)
    
    def insert(self, data):
        if not '_id' in data:
            object_id = self.auto_object_id()
            if object_id in self.get_documents():
                return {'status':503, 'success':False}
            data['_id'] = object_id
        else:
            data['_id'] = str(data['_id']).replace(' ', '_')
            object_id = data['_id']
            if object_id in self.get_documents():
                return {'status':503, 'success':False}
        
        data['_version'] = 1
        
        mkdir(self.collection_dir+object_id)
        if not object_id in self.get_documents():
            return {'status':500, 'success':False}
        
        with open(self.collection_dir+object_id+"/1.json", "w") as document:
            document.write(json.dumps(data))
        return {'status':200, 'success':True, 'objectId':object_id}

class VersionDocuments(Documents):

    def get_versions(self, object_id):
        raw_data = listdir(self.collection_dir+object_id)
        versions = []
        for version in raw_data:
            versions.append(int(version[:-5]))
        versions.sort(reverse=True)

        documents = []
        for version in versions:
            documents.append("%d.json" % version)
        return tuple(documents)
    
    def last_version_document(self, object_id):
        return self.get_versions(object_id)[0]
    
    def last_version_in_documents(self):
        objects = []
        for document in self.get_documents():
            objects.append(
                "%s%s/%s" % (self.collection_dir, document, self.last_version_document(document))
            )
        return tuple(objects)

class FindDocuments(VersionDocuments):

    def value_in_key(self, value, keys, limit = 0, id_only=False):
        self.value = value
        self.keys = keys
        self.limit = limit
        self.id_only = id_only

        if len(keys)==1:
            return self.one_key()
        else:
            return self.many_keys()

    def one_key(self):
        key = self.keys[0]
        if key == '_id':
            value = (self.value)
            if value in self.get_documents():
                if self.id_only:
                    return (self.value,)
                return (self.get_data_file(
                    "%s%s/%s" % (self.collection_dir, value, self.last_version_document(self.value))
                    ),)
            return ()
        documents = []
        quant_result = 0
        for doc in self.last_version_in_documents():
            data = self.get_data_file(doc)
            if key in data:
                if data[key] == self.value:
                    if self.id_only:
                        documents.append(data['_id'])
                    else:
                        documents.append(data)
                    quant_result+=1
                    if self.limit>0:
                        if quant_result == self.limit:
                            return tuple(documents)
        return tuple(documents)
    
    def many_keys(self):
        quant_result = 0
        documents = []
        for document in self.last_version_in_documents():
            data = self.get_data_file(document)

            value = self.keys.pop(0)
            if value in data:
                value = data[value]
            else:
                continue
            
            for key in self.keys:
                if type(value) is int or type(value) is str:
                    continue
                if type(value) is list:
                    if key>(len(value)-1) or key<0:
                        continue
                    value = value[key]
                else:
                    if key in value:
                        value = value[key]
            
            if self.value == value:
                if self.id_only:
                    documents.append(data['_id'])
                else:
                    documents.append(data)
                quant_result+=1
                if self.limit>0:
                    if quant_result == self.limit:
                        return tuple(documents)
        return tuple(documents)

    def get_data_file(self, document_dir):
        document = open(document_dir, 'r')
        data = document.read()
        document.close()
        # Tratar possível erro no JSON
        return json.loads(data)

class UpdateDocument(FindDocuments):
    
    def update_many(self, value, key, data, limit = 1):
        if "_id" in data:
            return {'success':0, 'total':0, 'objectId_success':[]}
        documents = self.value_in_key(value, key, limit)
        results = {'success':0, 'total':len(documents), 'objectId_success':[]}
        if not documents:
            return results
        for doc in documents:
            doc.update(data)
            doc['_version'] += 1
            object_id = doc['_id']
            version = doc['_version']
            self.new_version(object_id, doc, version)
            results['success']+=1
            results['objectId_success'].append((object_id, version))
        return results

    def new_version(self, object_id, data, version):
        version = str(version)+'.json'
        with open(self.collection_dir+object_id+'/'+version, 'w') as document:
            document.write(json.dumps(data))

class RemoveDocument(FindDocuments):

    def remove_many(self, value, key, limit = 1):
        documents = self.value_in_key(value, key, limit, True)
        results = {'success':0, 'total':len(documents), 'objectId_success':[]}
        for object_id in documents:
            rmtree(self.collection_dir+object_id)
            results['success']+=1
            results['objectId_success'].append(object_id)
        return results