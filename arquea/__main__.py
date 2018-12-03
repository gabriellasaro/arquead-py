import sys
from arquea.info import InfoArquea
from arquea.arquea import Arquea
info = InfoArquea()

def other():
    print(info.get_release(), '\n')
    print("Lista de comandos:")
    print(" --create")
    print(" --version")
    print(" --release")
    print(" --help")
    print(" --compatible")

if len(sys.argv)>=2:
    if sys.argv[1] == '--version':
        print(info.get_version())
    elif sys.argv[1] == '--release':
        print(info.get_release())
    elif sys.argv[1] == '--help':
        print("Você pode obter ajuda no repositório oficial - {}".format(info.get_repository()))
    elif sys.argv[1] == '--compatible':
        print("Lista de banco de dados compatíveis com a versão corrente ({}):".format(info.get_version()))
        for version in info.get_compatible():
            print(" {}".format(version))
    elif sys.argv[1] == '--create':
        if len(sys.argv)==3:
            new = Arquea()
            print(new.create_database(sys.argv[2]))
        else:
            print("Faltando parâmetro para criar banco de dados.")
    else:
        other()
else:
    other()
