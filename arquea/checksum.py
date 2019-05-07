from arquea.documents import VersionDocuments
from hashlib import sha256, md5
class CheckSum(VersionDocuments):

    def __init__(self, collection_dir, object_id):
        super().__init__(collection_dir)
        self.object_id = object_id
    
    def check(self, func):
        def wrapper(*args, **kargs):
            if not self.object_id:
                return {'success':0, 'total':0}
            if self.object_id in self.get_documents():
                last_version = self.last_version_document(self.object_id)
                with open(self.collection_dir+last_version, 'r') as pdata:
                    data = func(pdata)
                return {'success':1, 'total':1, 'chechsum':data}
            return {'success':0, 'total':0}
        return wrapper
    
    @check
    def sha256(self, data):
        return sha256(bytes(data, 'utf-8')).hexdigest()
    
    @check
    def md5(self, data):
        return md5(bytes(data, 'utf-8')).hexdigest()