from classes.cliente import Cliente

class PessoaJuridica(Cliente):
    def __init__(self, nome, data_nascimento, cnpj, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cnpj = cnpj