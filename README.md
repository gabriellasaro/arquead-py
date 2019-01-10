# ArqueaDB
Um pequeno banco de dados NoSQL feito em Python.

A small NoSQL database made in Python.

### Correções v0.2.2
- Resolvido um pequeno problema encontrado no tratamento de parâmetros de algumas funções;
- Novo recurso: "python3 -m arquea --error-list" para obter a lista de erros.

### Alterações v0.2.0
- Resolvido o problema de formatação dos diretórios no Windows;
- Remoção de alguns códigos redundantes;
- Retornos em tuple no lugar de list em algumas funções;
- Alteração na função insert_one();
- Nova função de inserção: insert_many() para inserir listas de dicionários;
- Nova função get_current_collection() retorno a coleção definida;
- Nova função get_current_directory() retorna o diretório de operação atual;
- Agumas correções nas funções create_database(), find_document(), updade() e remove();
- Nova funcionalidade na função connect(directory, collection), é permitido passar a coleção diretamente nela;
- Nova função checksum_sha256(objectId) retorna uma hash (sha256) do documento solicitado (aceita somente objectId como parâmetro de busca);
- Tabela de código de erros atualizada e pequena alteração na função de retorno de erro.

## Documentação

### Instalação
Você pode instalar o ArqueaDB atravez do pip:

    pip install arquea

### Criar um banco de dados
Para criar um banco de dados execute o seguinte comando no diretório desejado:

    python3 -m arquea --create name_database

Ou:

    from arquea import Arquea
    db = Arquea()
    db.create_database("name_database")

### Conexão:
Para se conecatar com o banco de dados arquea é somente necessário passar o diretório em que se encontra o banco.

    from arquea import Arquea
    db = Arquea()
    con = db.connec("/home/user/arqueadb/aq-db/")
    if con['status']!=200:
        print(con)
        print('Erro ao conectar-se ao banco de dados!')

### Coleções:
#### Para criar uma coleção use o comando:

    db.create_collection('user_profile')

#### Para obter todas as coleções

    print(db.get_collections())

#### Definir coleção
Para pesquisar, atualizar, inserir e remover qualquer arquivo, é necessário definir um coleção.

    db.set_collection('user_profile')

#### Lista de documentos
A função get_documents() retorna a lista de documente de uma coleção.

    print(db.get_documents())

#### Pesquisar
A função find_document() aceita 3 (três) parâmetros, sendo: um valor de busca, uma lista com o caminho até o valor, e, o limite de retorno, sendo (0) ilimitado.

    {'items':{
        'name':'Pedro',
        'phone':'999999999'
    }}

    print(db.find_document('Pedro', ['items', 'name'], 1))

#### Inserir
A função insert_one() aceita um parâmetro, sendo um dicionário Python.

    db.insert_one({'_id':123456, 'name':'Pedro'})

A função insert_many() aceita um parâmetro, sendo do tipo lista ou tupla Python.

    list_items = [
        {'name':'Pedro', 'age':38},
        {'name':'Maria', 'age':37}
    ]

    db.insert_many(list_items)

Se não for definido a chave-valor "_id" será gerado um automaticamente. Lembrando que o (objectId) não pode ser atualizado.

#### Atualizar
A função update() aceita 4 (quatro) parâmetros, sendo: um valor de busca, uma lista com o caminho até o valor, informação atualizada, e, o limite.

    db.update('Pedro', ['items', 'name'], {'items':{'name':'Sr. Pedro'}}, 1)

#### Remover
A função remove() aceita 3 (parâmetros), sendo: um valor de busca, uma lista com o caminho até o valor, e, o limite.

    db.remove('value', ['key'], 0)

#### Observação
A função get_last_err() funciona somente com as funções: checksum_sha256(), get_documents(), find_document(), update(), remove().

Cuidado com o uso desta função.

    print(db.get_last_err())

### Outras funções:

#### Versão do banco de bados
A função get_db_info() retorna a versão do banco de dados conectado. Estando esses dados armanzenados no arquivo "conf.arquea" de cada banco.

    print(db.get_db_info())

### Lista de erros:

    200:'OK',
    300:'Versão do banco de dados não é compatível',
    301:'Não foi possível determinar a versão do banco de dados',
    302:'Erro de sintaxe no arquivo "conf.arquea"',
    404:'Diretório do banco de dados não encontrado.',
    406:'Coleção solicitada não encontrada',
    408:'Não é possível provar ser um banco de dados ArqueaDB. Faltando arquivo "conf.arquea".',
    500:'Erro desconhecido',
    501:'Parâmetro inválido ou nulo',
    502:'Erro ao criar coleção',
    503:'Já existe uma coleção/objeto com está identificação',
    504:'Erro ao criar banco de dados',
    505:'Já existe um diretório/documento com este nome',
    506:'Nenhum documento encontrado',
    508:'Ação não permitida',
    509:'Faltando dados para validar operação'

Exemplo de retorno:

    {'status': 404, 'message': 'Diretório do banco de dados não encontrado.'}
