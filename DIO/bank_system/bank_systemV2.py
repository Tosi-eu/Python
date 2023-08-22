import random
from data import *

def menu():
    print("==========================")
    print("    Operações do banco    ")
    print("        1 - Saque         ")
    print("        2 - Depósito      ")
    print("        3 - Extrato       ")
    print("        4 - Cadastro      ")
    print("        5 - Criar CC      ")
    print("        6 - Listar        ")
    print("==========================")
    print("OBS: Se não existir o comando, a operação é cancelada\n")

def fazer_saque():
    global extrato
    global LIMITE_SAQUE
    valor = float(input("\nValor a ser sacado: "))
    if(LIMITE_SAQUE != 0):
        if valor <= extrato and valor > 0 and valor <= 500:
            extrato -= valor
            print("Saque realizado com sucesso!")
            LIMITE_SAQUE -= 1
        else:
            print("\nExtrato inferior ao valor resquisitado para saque!\n")
    else:
        print("\nLimite de saques diário atingido!\n")
        
def fazer_deposito():
    global extrato
    deposito = float(input("\nValor a ser depositado: "))
    if deposito <= 0:
        print("\nValor inválido, tente novamente!\n")
        pass
    else:
        extrato += deposito
        print(f"\nQuantia de R$ {round(deposito, 2)} depositado em sua conta!\n")

def mostrar_extrato():
    global extrato
    print(f"\nExtrato : R$ {round(extrato, 2)}\n")

def cria_usuario():
    global usuarios
    nome = input("Digite o nome do usuário: ")
    if nome not in usuarios:
        usuarios[nome] = {
            'valor_em_conta': 0.0,
            'conta_corrente': 0,
            'agencia': 0
        }
    else:
        print("Usuário já existe!!\n")

def cria_conta_corrente():
    global usuarios
    nome = input("Usuário que deseja criar CC: ")
    for chave in usuarios.keys():
        if nome == chave:
            print("\nChave encontrada, criando conta: \n")
            usuarios[nome]['conta_corrente'] = gerar_numero_conta()
            usuarios[nome]['agencia'] = gerar_numero_agencia()

def gerar_numero_agencia():
    numero_agencia = f"{random.randint(100, 999)}-{random.randint(0, 9)}"
    return numero_agencia

def gerar_numero_conta():
    numero_conta = f"{random.randint(10000, 99999)}-{random.randint(0, 9)}"
    return numero_conta

def lista_usuarios():
    global usuarios
    print("\nUsuários cadastrados:\n")
    for chave, valor in usuarios.items():
        print(f"Nome: {chave}\nValor em conta: R$ {round(valor['valor_em_conta'], 2)}\nAgência: {valor['agencia']}\nConta Corrente: {valor['conta_corrente']}\n\n")

def historico_do_usuario():
    pass

while True:
    menu()    
    op = int(input(("Escolha uma operação: ")))

    match op:

        case 1:
            fazer_saque()
        case 2:
            fazer_deposito()
        case 3:
            mostrar_extrato()
        case 4:
            cria_usuario()
        case 5:
            cria_conta_corrente()
        case 6:
            lista_usuarios()
        case _:
            print("\nEncerrando transação, comando não encontrado!")
            exit(1)
