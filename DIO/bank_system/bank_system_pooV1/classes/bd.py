from sqlalchemy.orm import declarative_base, relationship, sessionmaker, Session
from sqlalchemy import String, Float, Integer, ForeignKey, Column, create_engine, inspect

base = declarative_base()

class Cliente(base):
    __tablename__ = "cliente_banco"
    id = Column(Integer, primary_key=True, autoincrement=True)
    endereco = Column(String(100))
    conta = (String)

    def __repr__(self):
        return f"Historico(id={self.id}\tcliente={self.endereco}\tagencia={self.conta})"

class PessoaFisica(base):
    __tablename__ = "pessoa_fisica"
    nome = Column(String(100), nullable=False)
    data_nascimento = Column(String(12), nullable=False)
    cpf = Column(Integer, primary_key=True)

    def __repr__(self):
        return f"Historico(id={self.nome}\tcliente={self.data_nascimento}\tagencia={self.cpf})"

class PessoaJuridica(base):
    __tablename__ = "pessoa_juridica"
    nome = Column(String(100), nullable=False)
    data_nascimento = Column(String(12), nullable=False)
    cnpj = Column(Integer, primary_key=True)

    def __repr__(self):
        return f"Historico(id={self.nome}\tcliente={self.data_nascimento}\tagencia={self.cnpj})"

class Conta(base):
    __tablename__ = "contas_banco"
    id = Column(Integer, primary_key=True, autoincrement=True)
    saldo = Column(Float)
    numero = Column(String(50), primary_key=True)
    agencia = Column(String(8), nullable=False)
    cliente = Column(String(50), ForeignKey("historico.transacao"))
    relation = relationship("historico", back_populates="cliente", cascade="all, delete-orphan")

    def __repr__(self):
        return f"Historico(id={self.id}\tcliente={self.cliente}\tagencia={self.agencia}, saldo={self.saldo})"

class ContaCorrente(base):
    __tablename__ = "contas_corrente"
    numero = Column(String(50), ForeignKey("contas_banco.numero"), primary_key=True)
    cliente = Column(String(100), ForeignKey("contas_banco.cliente"))
    relation = relationship("contas_banco", back_populates="numero", cascade="all, delete-orphan")
    relation2 = relationship("contas_banco", back_populates="cliente", cascade="all, delete-orphan")

    def __repr__(self):
        return f"Historico(agencia={self.agencia}\tnúmero={self.numero})"

class ContaPoupanca(base):
    __tablename__ = "contas_poupanca"
    numero = Column(String(50), ForeignKey("contas_banco.numero"), primary_key=True)
    cliente = Column(String(100), ForeignKey("contas_banco.cliente"))
    relation = relationship("contas_banco", back_populates="numero", cascade="all, delete-orphan")
    relation2 = relationship("contas_banco", back_populates="cliente", cascade="all, delete-orphan")

    def __repr__(self):
        return f"Historico(agencia={self.agencia}\tnúmero={self.numero})"

class Deposito(base):
    __tablename__ = "depositos"
    id = Column(Integer, ForeignKey("cliente_banco.id"), primary_key=True)
    cliente = Column(String(100), ForeignKey("contas_banco.cliente"), nullable=False)
    agencia = Column(String(8), ForeignKey("contas_banco.agencia"), nullable=False)
    numero_fisico = Column(String(12), ForeignKey("contas_corrente.cpf"))
    numero_juridico = Column(String(12), ForeignKey("contas_poupanca.cnpj"))
    relation = relationship("cliente_banco", back_populates="id", cascade="all, delete-orphan")
    relation2 = relationship("contas_banco", back_populates="cliente", cascade="all, delete-orphan")
    relation3 = relationship("contas_corrente", back_populates="cpf", cascade="all, delete-orphan")
    relation4 = relationship("contas_poupanca", back_populates="cnpj", cascade="all, delete-orphan")
    valor = Column(Float, nullable=False)

    def __repr__(self):
        return f"Historico(id={self.id}\tcliente={self.cliente}\tagencia={self.agencia}\tvalor={self.valor})"

class Saque(base):
    __tablename__ = "saques"
    id = Column(Integer, ForeignKey("cliente_banco.id"), primary_key=True)
    cliente = Column(String(100), ForeignKey("contas_banco.cliente"))
    valor = Column(Float, nullable=False)
    limite = Column(Integer)
    limite_saque = Column(Integer, nullable=False)
    relation = relationship("cliente_banco", back_populates="id", cascade="all, delete-orphan")
    relation2 = relationship("cliente_banco", back_populates="cliente", cascade="all, delete-orphan")

    def __repr__(self):
        return f"Historico(id={self.id}\tcliente={self.cliente}\tvalor={self.valor}"

class Historico(base):
    __tablename__ = "historico"
    id = Column(Integer, ForeignKey("cliente_banco.id"), primary_key=True)
    cliente = Column(String(100), ForeignKey("contas_banco.cliente"))
    agencia = Column(String(8), ForeignKey("contas_banco.agencia"), nullable=False)
    numero_fisico = Column(String(12), ForeignKey("contas_corrente.cpf"))
    numero_juridico = Column(String(12), ForeignKey("contas_poupanca.cnpj"))
    transacao = Column(String(50), nullable=False)
    relation = relationship("cliente_banco", back_populates="id", cascade="all, delete-orphan")
    relation2 = relationship("contas_banco", back_populates="cliente", cascade="all, delete-orphan")
    relation3 = relationship("contas_banco", back_populates="agnecia", cascade="all, delete-orphan")
    relation4 = relationship("contas_corrente", back_populates="cpf", cascade="all, delete-orphan")
    relation5 = relationship("contas_poupanca", back_populates="cnpj", cascade="all, delete-orphan")

    def __repr__(self):
        return f"Historico(id={self.id}\tcliente={self.cliente}\tagencia={self.agencia}\ttransação={self.transacao})"

class BancoDeDados():
    def __init__(self) -> None:
        self.engine = create_engine("sqlite://")
        self.Session = sessionmaker(bind=self.engine)
        self.create_tables()

    def create_tables(self):
        base.metadata.create_all(self.engine)

    def conectar(self):
        try:
            self.session: Session = self.Session()
            self.inspector = inspect(self.engine)
        except Exception as error:
            print(f"Erro: {error}")
        else:
            print("Conectado ao banco com sucesso!")

    def desconectar(self):
        self.session.close()
        print("Desconectado do banco com sucesso!")

    def adicionar_registro(self, registro):
        self.session.add(registro)
        self.session.commit()

    def listar_registros(self, tabela):
        return self.session.query(tabela).all()
