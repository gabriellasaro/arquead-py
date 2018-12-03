class InfoArquea:

    def __init__(self):
        self.version = "0.2.0"
        self.name = "ArqueaDB"
        self.release_date = "ArqueaDB v{} 2018-12-02 LinuxMint-19-tara/Linux".format(self.version)
        self.repository = "https://github.com/gabriellasaro/arqueadb/"
        self.compatible_version = ("0.1.0",)
    
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

    def get_compatible(self):
        return self.compatible_version
