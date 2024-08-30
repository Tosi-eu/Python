def analise_vendas(vendas):
    # TODO: Calcule o total de vendas e realize a média mensal:
    total_vendas = 0
    media_vendas = 0
    for count, venda in enumerate(vendas):
        total_vendas += venda
        count+=1
    media_vendas = total_vendas / count

    return f"{total_vendas}, {media_vendas:.2f}"

def obter_entrada_vendas():
    vendas = list(map(int, input().split(', ')))

    return vendas

#vendas = obter_entrada_vendas()
#print(analise_vendas(vendas))

def produto_mais_vendido(produtos):
    contagem = {}
    
    for produto in produtos:
        if produto in contagem:
            contagem[produto] += 1
        else:
            contagem[produto] = 1
    
    max_produto = None
    max_count = 0
    
    for produto, count in contagem.items():
        if count > max_count:
            max_produto, max_count = produto, count
    return max_produto

def obter_entrada_produtos():
    entrada = input().split(',')
    produtos = [e.strip() for e in entrada]
    return produtos

#produtos = obter_entrada_produtos()
#print(produto_mais_vendido(produtos))

class Venda:
    def __init__(self, produto, quantidade, valor):
        self.produto = produto
        self.quantidade = quantidade
        self.valor = valor

class Relatorio:
    def __init__(self):
        self.vendas = []

    def adicionar_venda(self, venda):
        if isinstance(venda, Venda):
            self.vendas.append(venda)
        else:
            print('Classe não permitida ness operação!\n')
        
    def calcular_total_vendas(self):
        total = 0
        for venda in self.vendas:
            total += venda.quantidade * venda.valor
        return total


def main():
    relatorio = Relatorio()
    
    for _ in range(3):
        produto = input()
        quantidade = int(input())
        valor = float(input())
        venda = Venda(produto, quantidade, valor)
        relatorio.adicionar_venda(venda)
        subtotal = relatorio.calcular_total_vendas()
    print(f'Total de Vendas: {subtotal}')
    
# main()

class Venda:
    def __init__(self, produto, quantidade, valor):
        self.produto = produto
        self.quantidade = quantidade
        self.valor = valor

class Categoria:
    def __init__(self, nome):
        self.nome = nome
        self.vendas = []
        self.vendas_totais = 0

    # TODOS: Implementar o método adicionar_venda para adicionar uma venda à lista de vendas:
    def adicionar_venda(self, venda):
      if isinstance(venda, Venda):
        self.vendas.append(venda)
      else:
        print('Classe não permitida para essa operação!\n')

    # TODOS: Implementar o método total_vendas para calcular e retornar o total das vendas
    def total_vendas(self, vendas):
      total = 0
      if isinstance(vendas, Venda):
        self.vendas_totais += vendas.valor
      else:
        print('Classe não permitida para essa operação!\n')

def main():
    categorias = []

    for _ in range(2):
        nome_categoria = input()
        categoria = Categoria(nome_categoria)

        for _ in range(2): 
            entrada_venda = input()
            produto, quantidade, valor = entrada_venda.split(',')
            quantidade = int(quantidade.strip())
            valor = float(valor.strip())

            venda = Venda(produto.strip(), quantidade, valor)
            # TODOS: Adicione a venda à categoria usando o método adicionar_venda:
            categoria.adicionar_venda(venda)
            categoria.total_vendas(venda)

        categorias.append(categoria)
    
    # Exibindo os totais de vendas para cada categoria
    for categoria in categorias:
        # TODOS: Exibir o total de vendas usando o método total_vendas:
        print(f"Vendas em {categoria.nome}: {categoria.vendas_totais}")

if __name__ == "__main__":
    main()