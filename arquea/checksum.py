from arquea.documents import VersionDocuments
from hashlib import sha256
class CheckSum(VersionDocuments):

    def get_sha256(self, object_id = None):
        if not object_id:
            return {'success':0, 'total':0}
        if object_id in self.get_documents():
            last_version = self.last_version_document(object_id)
            with open(self.collection_dir+last_version, 'r') as pdata:
                data = sha256(bytes(pdata.read(), 'utf-8')).hexdigest()
            return {'success':1, 'total':1, 'chechsum':data}
        return {'success':0, 'total':0}