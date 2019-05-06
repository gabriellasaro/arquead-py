class ErrorLine:

    error_line = []

    def add_err(self, number, action):
        self.error_line.append((number, action))
    
    def valid_action(self):
        if not self.error_line:
            return True
        return False
    
    def clean_errors(self):
        self.error_line.clear()

class RErrorLine(ErrorLine):

    def __init__(self, error = 500):
        self.code_error = error
        self.error_list = {
            200:'OK',
            202:'Versão do banco de dados não é compatível',
            204:'Diretório do banco de dados não encontrado.',
            206:'Erro de sintaxe no arquivo de configuração',
            208:'Faltando arquivo de configuração',
            300:'Erro ao criar banco de dados',


            404:'Nenhum documento/coleção encontrado',

            500:'Erro desconhecido',
            501:'Parâmetro inválido ou nulo',
            502:'Erro ao criar coleção',
            503:'Já existe uma coleção/objeto com está identificação',
            505:'Já existe um diretório/documento com este nome',
            508:'Ação não permitida',
            509:'Faltando dados para validar operação'
        }
    
    # def show(self):
    #     if self.code_error in self.error_list.keys():
    #         return {'status':self.code_error, 'message':self.error_list[self.code_error]}
    #     return {'status':500, 'message':self.error_list[500]}
    
    def formatted_list_error(self):
        for err in self.error_line:
            print("Nº Error: {} | Action: {}".format(err[0], err[1]))
    
class ReturnMessage():

    def __init__(self, error = 500):
        self.code_error = error
        self.error_list = {
            200:'OK',
            202:'Versão do banco de dados não é compatível',
            204:'Diretório do banco de dados não encontrado.',
            206:'Erro de sintaxe no arquivo de configuração',
            208:'Faltando arquivo de configuração',
            300:'Erro ao criar banco de dados',


            404:'Nenhum documento/coleção encontrado',

            500:'Erro desconhecido',
            501:'Parâmetro inválido ou nulo',
            502:'Erro ao criar coleção',
            503:'Já existe uma coleção/objeto com está identificação',
            505:'Já existe um diretório/documento com este nome',
            508:'Ação não permitida',
            509:'Faltando dados para validar operação'
        }
    
    def show(self):
        if self.code_error in self.error_list.keys():
            return {'status':self.code_error, 'message':self.error_list[self.code_error]}
        return {'status':500, 'message':self.error_list[500]}

class Error:
    
    status_error = [False, 200]
    
    def set_status_error(self, status = False, code = 500):
        self.status_error = [status, code]
    
    def error_status(self):
        return self.status_error[0]
    
    def error_code(self):
        return self.status_error[1]