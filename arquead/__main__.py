import sys
from arquead.info import Info
from arquead.arquea import Arquea

info = Info()
print(info.get_release() + "\n")

if len(sys.argv) >= 2:
    if sys.argv[1] == 'version':
        print(info.get_release())
    elif sys.argv[1] == 'help':
        info.help()
    elif sys.argv[1] == 'compatible':
        info.show_compatible()
    elif sys.argv[1] == 'create':
        if len(sys.argv) >= 3:
            new = Arquea()
            print(new.create_database(sys.argv[2]))
        else:
            print("\tInforme o caminho do banco. Ex.: /home/user/new-database")
    else:
        print("\tComando não reconhecido.")
else:
    print("\tComando não reconhecido.")
