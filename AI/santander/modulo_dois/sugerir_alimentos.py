# Entrada do usuário
cogumelo_desejado = input()

# Função para sugerir cogumelos com preços mais baixos com base em um cogumelo desejado.
def sugerir_cogumelos(cogumelo_desejado):
    # Dicionário onde as chaves são os tipos de cogumelos e os valores são os preços correspondentes
    catalogo = {
        "Shitake": 10,
        "Portobello": 8,
        "Shimeji": 6,
        "Champignon": 12,
        "Funghi": 16,
        "Porcini": 16
    }

    # Verifica se o cogumelo desejado está no catálogo
    if cogumelo_desejado in catalogo:
        valor_desejado = catalogo[cogumelo_desejado] #acessa o index 'nome_cogumelo', cujo valor é o preço dele
        sugestoes = [] #necessário iterar sobre o dicionário

        # Procura por cogumelos mais baratos no catálogo
        for cogumelo, valor in catalogo.items():
            if valor <= valor_desejado and cogumelo != cogumelo_desejado:
                sugestoes.append((cogumelo, valor))  # Adiciona uma tupla (cogumelo, valor) à lista
                if len(sugestoes) == 2:
                    break #critério de parada
        
        if not sugestoes:
            # Se não houver sugestões, exibe a mensagem indicada no enunciado
            print("Desculpe, não há sugestões disponíveis.")
        else:
            for sugestao, valor_sugestao in sugestoes:
                print(f"{sugestao} - Valor: {valor_sugestao}")
    else:
        # Se o cogumelo desejado não estiver no catálogo, exibe uma mensagem de erro indicada no enunciado
        print("Cogumelo não encontrado no catálogo.")

# Chamada da função para sugerir cogumelos
sugerir_cogumelos(cogumelo_desejado)
