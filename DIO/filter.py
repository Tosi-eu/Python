def filtrar_visuais(lista_visuais):
     # Converter a string de entrada em uma lista
     visuais = lista_visuais.split(", ")

     visuais_cap = [visual.title() for visual in visuais]

     # TODO: Normalize e remova duplicatas usando um conjunto
     visual_un = set(visuais_cap)
    
    # TODO: Converta o conjunto de volta para uma lista ordenada:
     lista_final = sorted(visual_un)
    
     # Unir a lista em uma string, separada por vírgulas
     return ", ".join(lista_final)

 # Capturar a entrada do usuário
entrada_usuario = input()

 # Processar a entrada e obter a saída
saida = filtrar_visuais(entrada_usuario)
print(saida)    

from datetime import datetime

def extrair_anos(datas):
    # Divide a string de datas em uma lista
    lista_str = datas.split(", ")
    lista_datas = [datetime.strptime(data, '%Y-%m-%d') for data in lista_str]
    
    anos = [str(data.year) for data in lista_datas]
    # Junta os anos em uma string separada por vírgula e retorna
    return ", ".join(anos)


entrada = input()

# TODO: Chame a função para imprimir o resultado:
saida = extrair_anos(entrada)
print(saida)