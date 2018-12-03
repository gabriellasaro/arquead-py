from arquea.data import Collection
from arquea.error import Error
from hashlib import sha256
class CheckSum(Collection, Error):

    def get_sha256(self, objectId = None):
        if not objectId:
            self.set_status_error(True, 506)
            return {'total':0}
        file_dir = str(objectId)+'.json'
        if file_dir in self.get_documents():
            with open(self.collection_directory+file_dir, 'r') as pdata:
                data = sha256(bytes(pdata.read(), 'utf-8')).hexdigest()
            return {'total':1, 'chechsum':data}
        self.set_status_error(True, 506)
        return {'total':0}