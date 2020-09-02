class Version:
    __version = "0.3.0"
    __release_date = "2020-09-01"
    __compatible_version = ("0.3.0",)

    def __str__(self):
        return self.__version
    
    def get_compatible(self):
        return self.__compatible_version

    def get_release_date(self):
        return self.__release_date

    def get_version(self):
        return self.__version


class Info:
    __version = Version()
    __name = "ArqueaD"
    __repository = "https://github.com/gabriellasaro/arquead-py"
    __website = "https://arquead.lasaro.dev"

    def get_name(self):
        return self.__name

    def get_release(self):
        return f"{self.__name} v{self.__version} 2020-09-01"

    def help(self):
        print(f"Você pode obter ajuda no repositório oficial: {self.__repository}")
        print(f"Ou acessando o nosso website: {self.__website}")

    def cli(self):
        print(f"{self.get_release()}\n")
        print("Lista de comandos:")
        print(" --create")
        print(" --version")
        print(" --release")
        print(" --error-list")
        print("     --error-list number")
        print(" --help")
        print(" --compatible")

    def show_compatible(self):
        print(f"Lista de banco de dados compatíveis com a versão corrente ({self.__version.get_version()}):")
        for version in self.__version.get_compatible():
            print("     {}".format(version))

    def get_repository(self):
        return self.__repository
    
    def get_website(self):
        return self.__website
