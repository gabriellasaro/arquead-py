import sys
from arquea.info import Info
from arquea.arquea import Arquea
from arquea.error import ReturnMessage

info = Info()

if len(sys.argv) >= 2:
    if sys.argv[1] == '--version':
        print(info.get_version())
    elif sys.argv[1] == '--release':
        print(info.get_release())
    elif sys.argv[1] == '--help':
        info.help()
    elif sys.argv[1] == '--compatible':
        info.show_compatible()
    elif sys.argv[1] == '--error-list':
        error_list = ReturnMessage().error_list
        if len(sys.argv)==3:
            if int(sys.argv[2]) in error_list:
                print("Código de erro: {} - {}".format(sys.argv[2], error_list[int(sys.argv[2])]))
            else:
                print("Código de erro não encontrado.")
        else:
            print("Lista de erros:")
            for key, value in error_list.items():
                print("     {} - {}".format(key, value))
    elif sys.argv[1] == '--create':
        if len(sys.argv)==3:
            new = Arquea()
            print(new.create_database(sys.argv[2]))
        else:
            print("Faltando parâmetro para criar banco de dados.")
    else:
        info.cli()
else:
    info.cli()
