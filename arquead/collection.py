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
        
        data['id'] = (object_id, 1)  # id and version
        
        mkdir(join(self.__path, object_id))

        if not object_id in self.get_documents():
            return None, Error("Erro ao criar documento.")
        
        with open(join(self.__path, object_id, "/1.json"), "w") as doc:
            doc.write(dumps(data))
        return object_id, Error()
    
    def find(self, value=None, keys=None, limit=0, return_mode="content"):
        if value is None:
            return ()

        if type(keys) is list or type(keys) is tuple:
            return self.__many_keys(value, keys, limit, return_mode)
        elif type(keys) is str:
            return self.__one_key(value, keys[0], limit, return_mode)
        else:
            return ()

    def __return_content(self, doc_object, return_mode):
        if return_mode == "content":
            return doc_object.get_current_content(),
        elif return_mode == "id":
            return doc_object.get_object_id()[0]
        elif return_mode == "objectId":
            return doc_object.get_object_id(),
        else:
            return doc_object,

    def __find_doc_by_id(self, value, return_mode):
        if value in self.get_documents():
            doc = Document(join(self.__path, value))
            return self.__return_content(doc, return_mode)
        return ()

    def __one_key(self, value, key, limit, return_mode):
        if key == 'id':
            return self.__find_doc_by_id(value, return_mode)

        quant = 0
        docs = []
        for doc in self.get_documents():
            doc_object = Document(join(self.__path, doc))
            data = doc_object.get_current_content()
            if key in data:
                if data[key] == value:
                    docs.append(self.__return_content(doc_object, return_mode))
                    quant += 1
                    if quant == limit:
                        return tuple(docs)
        return tuple(docs)
    
    def __many_keys(self, value, keys, limit, return_mode):
        quant = 0
        docs = []
        for doc in self.get_documents():
            doc_object = Document(join(self.__path, doc))
            data = doc_object.get_current_content()
            kval = keys.pop(0)
            if kval in data:
                kval = data[kval]
            else:
                continue
            
            for key in keys:
                if type(kval) is int or type(kval) is str:
                    continue
                if type(kval) is list:
                    if key > (len(kval)-1) or key < 0:
                        continue
                    kval = kval[key]
                else:
                    if key in kval:
                        kval = kval[key]
            
            if value == kval:
                docs.append(self.__return_content(doc_object, return_mode))
                quant += 1
                if quant == limit:
                    return tuple(docs)
        return tuple(docs)
    
    def remove(self, value=None, key=None, limit=1):
        if value is None:
            return ()
        if type(key) is not list and type(key) is not tuple:
            return ()

        docs = []
        for doc_id in self.find(value, key, limit, "id"):
            rmtree(join(self.__path, doc_id))
            docs.append(doc_id)
        return tuple(docs)
    
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
