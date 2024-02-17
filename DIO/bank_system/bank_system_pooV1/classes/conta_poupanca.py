from classes.conta import Conta
from classes.saque import Saque

class ContaPoupanca(Conta):
    def __init__(self, numero, cliente, limite=10000):
        super().__init__(numero, cliente)
        self._limite = limite

    def sacar(self, valor):
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__]
        )

        excedeu_limite = valor > self._limite

        if excedeu_limite:
            print("\n@@@ Operação falhou! O valor do saque excede o limite. @@@")

        else:
            return super().sacar(valor)

        return False

    def __str__(self):
        return f"""\
            Agência:\t{self.agencia}
            C/P:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
        """