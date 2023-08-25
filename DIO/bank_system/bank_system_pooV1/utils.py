import textwrap
from classes.cliente import Cliente
from classes.conta import Conta
from classes.conta_corrente import ContaCorrente
from classes.conta_poupanca import ContaPoupanca
from classes.deposito import Deposito
from classes.historico import Historico
from classes.pessoa_fisica import PessoaFisica
from classes.pessoa_juridica import PessoaJuridica
from classes.saque import Saque
from classes.transacao import Transacao

def menu():
    menu = """\n
    ================ AGIOBANK ================
    [1]\tDepositar
    [2]\tSacar
    [3]\tExtrato
    [4]\tCadastro cliente
    [5]\tCriar conta PF
    [6]\tCriar conta PJ
    [7]\tListar contas PF
    [8]\tListar contas PJ
    [9]\tSair
    Opção escolhida:  """
    return input(textwrap.dedent(menu))

def filtrar_cliente_pf(documento_verificador, clientes):

    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == documento_verificador]
    return clientes_filtrados[0] if clientes_filtrados else None

def filtrar_cliente_pj(documento_verificador, clientes):

    clientes_filtrados = [cliente for cliente in clientes if cliente.cnpj == documento_verificador]
    return clientes_filtrados[0] if clientes_filtrados else None

def depositar(clientes_pf, clientes_pj):
        pf_pj = input("Pessoa física ou jurídica? [PF/PJ]: ")

        if pf_pj == "PF":
            cpf = input("Informe o CPF do cliente: ")
            cliente = filtrar_cliente_pf(cpf, clientes_pf)
            if not cliente:
                print("\n@@@ Cliente não encontrado! @@@")
                return

            valor = float(input("Informe o valor do depósito: "))
            transacao = Deposito(valor)

            conta = recuperar_conta_cliente(cliente)
            if not conta:
                return
            
            cliente.realizar_transacao(conta, transacao)
        elif pf_pj == "PJ":
            cnpj = input("Informe o CNPJ do cliente: ")
            cliente = filtrar_cliente_pj(cnpj, clientes_pj)
            if not cliente:
                print("\n@@@ Cliente não encontrado! @@@")
                return

            valor = float(input("Informe o valor do depósito: "))
            transacao = Deposito(valor)

            conta = recuperar_conta_cliente(cliente)
            if not conta:
                return

            cliente.realizar_transacao(conta, transacao)
        else:
            print("@@@ Operação inválida! Tente novamente @@@")
            pass

def sacar(clientes_pf, clientes_pj):

    pf_pj = input("Pessoa física ou jurídica? [PF/PJ]: ")

    if pf_pj == "PF":
        cpf = input("Informe o CPF do cliente: ")
        cliente = filtrar_cliente_pf(cpf, clientes_pf)

        if not cliente:
            print("\n@@@ Cliente não encontrado! @@@")
            return

        valor = float(input("Informe o valor do saque: "))
        transacao = Saque(valor)

        conta = recuperar_conta_cliente(cliente)
        if not conta:
            return

        cliente.realizar_transacao(conta, transacao)
    elif pf_pj == "PJ":
        cnpj = input("Informe o CNPJ do cliente: ")
        cliente = filtrar_cliente_pj(cnpj, clientes_pj)

        if not cliente:
            print("\n@@@ Cliente não encontrado! @@@")
            return

        valor = float(input("Informe o valor do saque: "))
        transacao = Saque(valor)

        conta = recuperar_conta_cliente(cliente)
        if not conta:
            return

        cliente.realizar_transacao(conta, transacao)
    else:
        print("@@@ Opção inválida! Tente novamente @@@")
        pass

def exibir_extrato(clientes_pf, clientes_pj):

    pf_pj = input("Pessoa física ou jurídica? [PF/PJ]: ")

    if pf_pj == "PF":
        cpf = input("Informe o CPF do cliente: ")
        cliente = filtrar_cliente_pf(cpf, clientes_pf)

        if not cliente:
            print("\n@@@ Cliente não encontrado! @@@")
            return

        conta = recuperar_conta_cliente(cliente)
        if not conta:
            return

        print("\n================ EXTRATO ================")
        transacoes = conta.historico.transacoes

        extrato = ""
        if not transacoes:
            extrato = "Não foram realizadas movimentações no período."
        else:
            for transacao in transacoes:
                extrato += f"\n{transacao['tipo']}:\n\tR$ {transacao['valor']:.2f}"

        print(extrato)
        print(f"\nSaldo:\n\tR$ {conta.saldo:.2f}")
        print("==========================================")
    elif pf_pj == "PJ":
        cnpj = input("Informe o CNPJ do cliente: ")
        cliente = filtrar_cliente_pj(cnpj, clientes_pj)

        if not cliente:
            print("\n@@@ Cliente não encontrado! @@@")
            return

        conta = recuperar_conta_cliente(cliente)
        if not conta:
            return

        print("\n================ EXTRATO ================")
        transacoes = conta.historico.transacoes

        extrato = ""
        if not transacoes:
            extrato = "Não foram realizadas movimentações no período."
        else:
            for transacao in transacoes:
                extrato += f"\n{transacao['tipo']}:\n\tR$ {transacao['valor']:.2f}"

        print(extrato)
        print(f"\nSaldo:\n\tR$ {conta.saldo:.2f}")
        print("==========================================")
    else:
        print("@@@ Operação inválida! Tente novamente @@@")
        return

def criar_cliente(clientes_pf, clientes_pj):
    pf_pj = input("Pessoa Física ou Jurídica?[PF/PJ]: ")

    if pf_pj == 'PF':
        cpf = input("Informe o CPF (somente número): ")
        cliente = filtrar_cliente_pf(cpf, clientes_pf)

        if cliente:
            print("\n@@@ Já existe cliente com esse CPF! @@@")
            return

        nome = input("Informe o nome completo: ")
        data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
        endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

        cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)
        clientes_pf.append(cliente)
        print("\n=== Cliente criado com sucesso! ===")
    
    elif pf_pj == 'PJ':
        cnpj = input("Informe o CNPJ (somente número): ")
        cliente = filtrar_cliente_pj(cnpj, clientes_pj)

        if cliente:
            print("\n@@@ Já existe cliente com esse CNPJ! @@@")
            return

        nome = input("Informe o nome completo: ")
        data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
        endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

        cliente = PessoaJuridica(nome=nome, data_nascimento=data_nascimento, cnpj=cnpj, endereco=endereco)
        clientes_pj.append(cliente)
        print("\n=== Cliente criado com sucesso! ===")
    else:
        print("@@@ Operação inválida @@@")

def criar_conta_pf(numero_conta, clientes_pf, contas_pf):

        cpf = input("Informe o CPF do cliente: ")
        cliente = filtrar_cliente_pf(cpf, clientes_pf)

        if not cliente:
            print("\n@@@ Cliente não encontrado, fluxo de criação de conta encerrado! @@@")
            return

        cc_cp = input("Conta corrente ou Conta poupança? [CC/CP]: ")
        if cc_cp == "CC":
            conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
            contas_pf.append(conta)
            cliente.contas.append(conta)
            print("\n=== Conta criada com sucesso! ===")
        elif cc_cp == "CP":
            conta = ContaPoupanca.nova_conta(cliente=cliente, numero=numero_conta)
            contas_pf.append(conta)
            cliente.contas.append(conta)
            print("\n=== Conta criada com sucesso! ===")
        else:
            print("@@@ Operação inválida! Tente novamente")
            pass

def criar_conta_pj(numero_conta, clientes_pj, contas_pj):

        cnpj = input("Informe o CNPJ do cliente: ")
        cliente = filtrar_cliente_pj(cnpj, clientes_pj)

        if not cliente:
            print("\n@@@ Cliente não encontrado, fluxo de criação de conta encerrado! @@@")
            return

        cc_cp = input("Conta corrente ou Conta poupança? [CC/CP]: ")
        if cc_cp == "CC":
            conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
            contas_pj.append(conta)
            cliente.contas.append(conta)
            print("\n@@@ Conta criada com sucesso! @@@")
        elif cc_cp == "CP":
            conta = ContaPoupanca.nova_conta(cliente=cliente, numero=numero_conta)
            contas_pj.append(conta)
            cliente.contas.append(conta)
            print("\n@@@ Conta criada com sucesso! @@@")
        else:
            print("@@@ Operação inválida! Tente novamente")
            pass

def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("\n@@@ Cliente não possui conta! @@@")
        return

    # FIXME: não permite cliente escolher a conta
    return cliente.contas[0]

def listar_contas_pf(contas):
    for conta in contas:
        print("=" * 100)
        print(textwrap.dedent(str(conta)))

def listar_contas_pj(contas):
    for conta in contas:
        print("=" * 100)
        print(textwrap.dedent(str(conta)))

def main():
    clientes_pf = []
    clientes_pj = []
    contas_pf = []
    contas_pj = []

    while True:
        opcao = menu()

        match opcao:

            case "1":
                depositar(clientes_pf, clientes_pj)

            case "2":
                sacar(clientes_pf, clientes_pj)

            case "3":
                exibir_extrato(clientes_pf, clientes_pj)

            case "4":
                criar_cliente(clientes_pf, clientes_pj)

            case "5":
                numero_conta = len(contas_pf) + 1
                criar_conta_pf(numero_conta, clientes_pf, contas_pf)
            
            case "6":
                numero_conta = len(contas_pj) + 1
                criar_conta_pj(numero_conta, clientes_pj, contas_pj)

            case "7":
                listar_contas_pf(contas_pf)

            case "8":
                listar_contas_pj(contas_pj)

            case "9":
                exit(1)

            case _:
                print("Operação inválida! Tente novamente")