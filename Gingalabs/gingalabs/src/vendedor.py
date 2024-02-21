from sistema import Sistema

class Vendedor:
    def __init__(self):
        self.sistema = Sistema()

    def fazer_login(self):
        self.sistema.sign_in()

    def consultar_informacoes(self):
        self.sistema.consult_informations()

    def ranking_produtos_mais_vendidos(self):
        self.sistema.top_products_best_seller()

    def cadastrar_novo_produto(self):
        self.sistema.signup_new_product()

    def obter_sugestao_reposicao_estoque(self):
        return self.sistema.get_replenish_suggestion()

    def obter_sugestao_novos_produtos(self):
        return self.sistema.get_suggestion_to_buy_new_products()