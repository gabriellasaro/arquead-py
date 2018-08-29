class ReturnMessage():

    def __init__(self, directory, code_error = 500):
        self.directory = directory
        self.code_error = code_error
        self.error_list = {
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
            506:'Nada encontrado para atualizar',
            508:'Ação não permitida'
        }
    
    def show(self):
        if self.code_error in self.error_list.keys():
            return {'status':self.code_error, 'directory':self.directory, 'message':self.error_list[self.code_error]}
        return {'status':500, 'directory':self.directory, 'message':self.error_list[500]}

class Error:
    
    status_error = [False, 200]
    
    def set_status_error(self, status = False, code = 500):
        self.status_error = [status, code]
    
    def error_status(self):
        return self.status_error[0]
    
    def error_code(self):
        return self.status_error[1]