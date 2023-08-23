from os import system
import random
from data import *
from time import sleep
from datetime import date

def menu():
    print("==============================================")
    print("             Operações - Agiobank             ")
    print("                 1 - Saque                    ")
    print("                 2 - Depósito                 ")
    print("                 3 - Cadastro                 ")
    print("                 4 - Criar CC                 ")
    print("                 5 - Extrato                  ")
    print("                 6 - Listar                   ")
    print("                 7 - Histórico                ")
    print("==============================================")
    print("               Escolha de 1 a 7:              ")
    print("==============================================")

def fazer_saque():
    global extrato
    global usuarios
    print("==============================================")
    print("          Área de realização de saque       \n")
    nome = input("- Nome do Usuário: ")
    if nome in usuarios:
        conta = input("- Conta corrente do usuário: ")
        if usuarios[nome]["Conta corrente"] != 0: 
            if conta == usuarios[nome]["Conta corrente"]:
                if(usuarios[nome]["Saques diarios"] != 3):
                    valor = float(input("\n- Valor a ser sacado: "))
                    if valor <= usuarios[nome]["Valor em conta"] and valor > 0 and valor <= 500:
                        usuarios[nome]["Valor em conta"] -= valor
                        print("- Saque realizado com sucesso! -")
                        usuarios[nome]["Historico"].append(f"{date.today()}, {OPERACOES[0]}")
                        usuarios[nome]["Saques diarios"] += 1
                    else:
                        print("\n- Extrato inferior ao valor resquisitado para saque!")
                        sleep(1)
                        system('clear')
                else:
                    print("\n- Limite de saques diário atingido!")
                    sleep(1)
                    system('clear')
            else:
                print("- Conta corrente não encontrada, operação cancelada!")
                sleep(1)
                system('clear')
        else:
            print("- Usuário não possui conta corrente, operação cancelada!")
            sleep(1)
            system('clear')
    else:
        print("- Nome não encontrado, operação cancelada!")
        sleep(1)
        system('clear')
        
def fazer_deposito():
    global extrato
    global usuarios
    print("==============================================")
    print("         Área de realização de depósito     \n")
    nome = input("- Pessoa que receberá o depósito: ")
    if nome in usuarios:
        conta = input("- Conta corrente: ")
        if conta == usuarios[nome]['Conta corrente']:      
            deposito = float(input("- Valor a ser depositado: "))
            if deposito <= 0:
                print("- Valor inválido, tente novamente!\n")
                pass
            else:
                usuarios[nome]['Valor em conta'] += deposito
                print("==============================================")
                print("- Quantia de R$ ",round(deposito, 2),  " depositado na conta de", usuarios[nome]["Nome"], "!\n")
                usuarios[nome]["Historico"].append(f"{date.today()}, {OPERACOES[1]}")
        else:
            print("- Conta corrente não encontrada!\n")
            sleep(1)
            system('clear')
    else:
        print("- Usuário não encontrado!\n")
        sleep(1)
        system('clear')

def mostrar_extrato_usuario():
    global usuarios
    print("==============================================")
    print("            Verificação de extrato          \n")
    nome = input("- Nome do usuário: ")
    print("- Extrato : R$  ", round(usuarios[nome]["Valor em conta"], 2),  "\n")
    usuarios[nome]["Historico"].append(f"{date.today()}, {OPERACOES[4]}")
    sair = input("- Aperte ENTER para sair")
    sleep(1)
    system('clear')

def cria_usuario():
    global usuarios
    print("==============================================")
    print("           Área de Criação de usuário       \n")
    nome = input("- Nome do usuário: ")
    if nome not in usuarios:
        usuarios[nome] = {
            'Nome': nome,
            'Valor em conta': 0.0,
            'Conta corrente': 0,
            'Agencia': 0,
            'Saques diarios': 0,
            'Historico': []
        }
        print(f"\n- Usuário {nome} criado com sucesso!\n")
        usuarios[nome]["Historico"].append(f"{date.today()}, {OPERACOES[2]}")
    else:
        print("==============================================")
        print("              Usuário já existe!              ")

def cria_conta_corrente():
    global usuarios
    print("==============================================")
    print("     Área de Criação de conta corrente (CC) \n")
    nome = input("- Usuário que deseja criar CC: ")
    for chave in usuarios.keys():
        if nome == chave:
            print("===========================================")
            print("          Criando conta, aguarde!        \n")
            sleep(1)
            usuarios[nome]['Conta corrente'] = gerar_numero_conta()
            usuarios[nome]['Agencia'] = gerar_numero_agencia()

        print("==============================================")
        print("- Conta criada, segue os dados da conta abaixo: ")
        print("- Conta corrente: ", usuarios[nome]['Conta corrente'], "\n- Agência: ", usuarios[nome]["Agencia"])
        usuarios[nome]["Historico"].append(f"{date.today()}, {OPERACOES[3]}")


def gerar_numero_agencia():
    numero_agencia = f"{random.randint(100, 999)}-{random.randint(0, 9)}"
    return numero_agencia

def gerar_numero_conta():
    numero_conta = f"{random.randint(10000, 99999)}-{random.randint(0, 9)}"
    return str(numero_conta)

def lista_usuarios():
    global usuarios
    print("==============================================")
    print("Lista de usuários cadastrados - Agiobank\n")
    for chave, valor in usuarios.items():
        print(f"- Nome: {chave}\n- Valor em conta: R$ {round(valor['Valor em conta'], 2)}\n- Agência: {valor['Agencia']}\n- Conta Corrente: {valor['Conta corrente']}\n\n")
        usuarios[chave]["Historico"].append(f"{date.today()}, {OPERACOES[5]}")

def historico_do_usuario():
    print("==============================================")
    print("        Histórico de usário - Agiobank      \n")
    nome = input("- Nome do usuário: ")
    if nome in usuarios and usuarios[nome]["Conta corrente"] != 0:
        conta = input("- Conta corrente: ")
        if usuarios[nome]["Conta corrente"] == conta:
            print(usuarios[nome]["Historico"], "\n")
            usuarios[nome]["Historico"].append(f"{date.today()}, {OPERACOES[6]}")
        else:
            print("- Conta corrente não encontrada!")
    else:
        print("Usuário não encontrado!")

while True:
    menu()    
    op = int(input(("              - Escolha uma operação: ")))
    print("Operação ", OPERACOES[op - 1], " selecionada, redirecionando...")
    sleep(1)
    system('clear')
    print()

    match op:

        case 1:
            fazer_saque()
        case 2:
            fazer_deposito()
        case 3:
            cria_usuario()
        case 4:
            cria_conta_corrente()
        case 5:
            mostrar_extrato_usuario()
        case 6:
            lista_usuarios()
        case 7:
            historico_do_usuario()
        case _:
            print("- Encerrando transação, comando não encontrado!")
            exit(1)
