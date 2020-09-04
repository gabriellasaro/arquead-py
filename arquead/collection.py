from os import listdir, mkdir
from os.path import join, basename
from uuid import uuid4
from json import dumps
from shutil import rmtree
from arquead.document import Document
from arquead.error import Error

class Collection:

    def __init__(self, path):
        self.__path = path
    
    def get_name(self):
        return basename(self.__path)

    def get_documents(self):
        return tuple(listdir(self.__path))

    def get_path(self):
        return self.__path
    
    def insert(self, data):
        if not 'id' in data:
            object_id = str(uuid4())
        else:
            object_id = str(data['id']).replace(' ', '_')
        
        if object_id in self.get_documents():
                return (None, Error("Já existe um documento com este object ID."))
        
        data['id'] = (object_id, 1) # id and version
        
        mkdir(join(self.__path, object_id))

        if not object_id in self.get_documents():
            return (None, Error("Erro ao criar documento."))
        
        with open(join(self.__path, object_id, "/1.json"), "w") as doc:
            doc.write(dumps(data))
        return (object_id, Error())
    
    def value_in_key(self, value, keys, limit = 0, id_only = False):
        if len(keys)==1:
            return self.one_key(value, keys[0], limit, id_only)
        else:
            return self.many_keys(value, keys, limit, id_only)
    
    def find_doc_by_id(self, value, id_only):
        if value in self.get_documents():
            if id_only:
                return (value, Error())
            doc = Document(join(self.__path, value))
            return (doc.get_current_content(),)
        return ()
    
    def one_key(self, value, key, limit, id_only):
        if key == 'id':
            return self.find_doc_by_id(value, id_only)
        
        docs = []
        quant = 0
        for doc in self.get_documents():
            data = Document(join(self.__path, doc)).get_current_content()
            if key in data:
                if data[key] == value:
                    if id_only:
                        docs.append(doc)
                    else:
                        docs.append(data)
                    quant += 1
                    if quant == limit:
                        return tuple(docs)
        return tuple(docs)
    
    def many_keys(self, value, keys, limit, id_only):
        quant = 0
        docs = []
        for doc in self.get_documents():
            data = Document(join(self.__path, doc)).get_current_content()
            kval = keys.pop(0)
            if kval in data:
                kval = data[kval]
            else:
                continue
            
            for key in keys:
                if type(kval) is int or type(kval) is str:
                    continue
                if type(kval) is list:
                    if key>(len(kval)-1) or key<0:
                        continue
                    kval = kval[key]
                else:
                    if key in kval:
                        kval = kval[key]
            
            if value == kval:
                if id_only:
                    docs.append(data['id'])
                else:
                    docs.append(data)
                quant += 1
                if quant > limit:
                    return tuple(docs)
        return tuple(docs)
    
    # def remove(self, value = None, key = None, limit = 1):
    #     if value is None:
    #         return {'success':0, 'total':0, 'objectId_success':[]}
    #     if type(key) is not list and type(key) is not tuple:
    #         return {'success':0, 'total':0, 'objectId_success':[]}
    #     documents = self.value_in_key(value, key, limit, True)
    #     results = {'success':0, 'total':len(documents), 'objectId_success':[]}
    #     for object_id in documents:
    #         rmtree(join(self.__path, object_id))
    #         results['success']+=1
    #         results['objectId_success'].append(object_id)
    #     return results
    
    # def update_many(self, value, key, data, limit = 1):
    #     if "_id" in data:
    #         return {'success':0, 'total':0, 'objectId_success':[]}
    #     documents = self.value_in_key(value, key, limit)
    #     results = {'success':0, 'total':len(documents), 'objectId_success':[]}
    #     if not documents:
    #         return results
    #     for doc in documents:
    #         doc.update(data)
    #         doc['_version'] += 1
    #         object_id = doc['_id']
    #         version = doc['_version']
    #         self.new_version(object_id, doc, version)
    #         results['success']+=1
    #         results['objectId_success'].append((object_id, version))
    #     return results

    # def new_version(self, object_id, data, version):
    #     version = str(version)+'.json'
    #     with open(join(self.__path, object_id, version), 'w') as document:
    #         document.write(dumps(data))
