#!/usr/bin/python3
from arquea.arquea import Arquea
db = Arquea()
con = db.connect("/home/user/arqueadb/aq-db/")
if con['status']!=200:
    print(con)
    print('Erro ao conectar-se ao banco de dados!')
else:
    print(db.create_collection('user_profile'))
    print(db.get_collections())
    print("-------------------------------------------")
    db.set_collection('user_profile')
    print(db.get_documents())