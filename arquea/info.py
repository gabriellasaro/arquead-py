class VersionArquea:

    def __init__(self):
        self.version = "0.3.0"
        self.compatible_version = ("0.3.0",)
    
    def __str__(self):
        return self.version
    
    def get_compatible(self):
        return self.compatible_version

class InfoArquea(VersionArquea):

    def __init__(self):
        super()
        self.name = "ArqueaDB"
        self.release_date = "ArqueaDB v{} 2019-05-06 LinuxMint-19.1-tessa/Linux".format(self.version)
        self.repository = "https://github.com/gabriellasaro/arqueadb/"
        self.website = "https://arqueadb.lasaro.tech"
    
    def get_info(self):
        return (self.version, self.name, self.release_date, self.repository)
    
    def get_name(self):
        return self.name
    
    def get_version(self):
        return self.version
    
    def get_release(self):
        return self.release_date
    
    def get_repository(self):
        return self.repository
    
    def get_website(self):
        return self.website
