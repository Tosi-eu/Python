extrato = 0
LIMITE_SAQUE = 3

def menu():
    print("==========================")
    print("    Operações do banco    ")
    print("        1 - Saque         ")
    print("        2 - Depósito      ")
    print("        3 - Extrato       ")
    print("==========================")

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
        case _:
            exit(1)
