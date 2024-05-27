-- VERIFICADAS
CREATE TABLE PARTIDO(
    cod_partido INTEGER PRIMARY KEY,
    nome VARCHAR(60) UNIQUE NOT NULL
);

CREATE TABLE programasDePartido(
    cod_partido INTEGER PRIMARY KEY,
    programa VARCHAR(255) NOT NULL,

    CONSTRAINT cod_partido FOREIGN KEY(cod_partido) REFERENCES partido(cod_partido) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE Candidato (
    Cod_Candidato INTEGER,
    nome VARCHAR(60) UNIQUE NOT NULL,
    Partido INTEGER NOT NULL,
    Estado_Ficha VARCHAR(50) NOT NULL,

    CONSTRAINT ck_candidato CHECK(Cod_Candidato > 0),
    CONSTRAINT candidato_pk PRIMARY KEY(Cod_Candidato),
    CONSTRAINT candidato_fk FOREIGN KEY(Partido) REFERENCES Partido(cod_partido) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE Cargo (
    Cod_Cargo INTEGER PRIMARY KEY,
    nome VARCHAR(60) NOT NULL,
    Localidade VARCHAR(50),
    Qtd_Eleitos INTEGER NOT NULL DEFAULT 0

    CONSTRAINT ck_cargo_eleitos CHECK(Qtd_Eleitos >= 0),
    CONSTRAINT ck_cargo CHECK(Cod_Cargo > 0)
);

CREATE TABLE Pleito (
    Cod_Pleito INTEGER PRIMARY KEY,
    Qtd_Votos INTEGER NOT NULL DEFAULT 0,

    CONSTRAINT ck_votos CHECK(Qtd_Votos >= 0)
);

CREATE TABLE Candidatura (
    Cod_Candidatura INTEGER PRIMARY KEY,
    Cod_Candidato INTEGER NOT NULL,
    Cod_Cargo INTEGER NOT NULL,
    Ano INTEGER NOT NULL,
    Pleito INTEGER NOT NULL,
    Cod_Candidatura_Vice INTEGER,
    Eleito BOOLEAN DEFAULT FALSE,

    CONSTRAINT ck_ano CHECK(Ano <= EXTRACT(YEAR FROM CURRENT_DATE) AND Ano >= 1894),
    CONSTRAINT candidato_fk FOREIGN KEY (Cod_Candidato) REFERENCES Candidato(Cod_Candidato) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT cargo_fk FOREIGN KEY (Cod_Cargo) REFERENCES Cargo(Cod_Cargo) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT pleito_fk FOREIGN KEY (Pleito) REFERENCES Pleito(Cod_Pleito) ON DELETE SET NULL ON UPDATE CASCADE,
    CONSTRAINT vice_fk FOREIGN KEY (Cod_Candidatura_Vice) REFERENCES Candidatura(Cod_Candidatura) ON DELETE SET NULL ON UPDATE CASCADE
);

CREATE TABLE EquipeApoio (
    Cod_Equipe INTEGER PRIMARY KEY,
    nomeEquipe VARCHAR(60) UNIQUE NOT NULL,

    CONSTRAINT ck_equipe CHECK(Cod_Equipe > 0)
);

CREATE TABLE ParticipanteEquipeApoio (
    Cod_Participante INTEGER PRIMARY KEY,
    Cod_Equipe INTEGER NOT NULL,
    Estado_Ficha VARCHAR(50) NOT NULL,

    CONSTRAINT ck_participante CHECK(Cod_Participante > 0),
    CONSTRAINT equipe_fk FOREIGN KEY (Cod_Equipe) REFERENCES EquipeApoio(Cod_Equipe) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE DoadoresCampanha (
    Cod_Doador INTEGER PRIMARY KEY,
    Estado_Ficha VARCHAR(50) NOT NULL,
    Tipo_Doador VARCHAR(50) NOT NULL CHECK (UPPER(Tipo_Doador) IN ('FÍSICO', 'JURÍDICO')),

    CONSTRAINT ck_doador CHECK(Cod_Doador > 0)
);

CREATE TABLE ProcessoJudicial (
    Cod_Processo INTEGER PRIMARY KEY,
    Cod_Individuo INTEGER NOT NULL,
    Tipo_Individuo VARCHAR(20) NOT NULL CHECK(UPPER(Tipo_Individuo) IN ('CANDIDATO', 'PARTICIPANTE EA', 'DOADOR')),
    Data_Termino DATE,
    Procedencia VARCHAR(50),
    CONSTRAINT ck_processo CHECK(Cod_Processo > 0),
    CONSTRAINT Procedencia_ck CHECK(UPPER(Procedencia) IN('PROCEDENTE', 'IMPROCEDENTE'))
);

CREATE TABLE DoadorFisico (
    Cod_Doador INTEGER PRIMARY KEY,
    CPF VARCHAR(11) UNIQUE NOT NULL,
    FOREIGN KEY (Cod_Doador) REFERENCES DoadoresCampanha(Cod_Doador) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE DoadorJuridico (
    Cod_Doador INTEGER PRIMARY KEY,
    CNPJ VARCHAR(14) UNIQUE NOT NULL,
    FOREIGN KEY (Cod_Doador) REFERENCES DoadoresCampanha(Cod_Doador) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE Doa(
    cod_doador INTEGER,
    cod_candidatura INTEGER,
    valor NUMERIC(11, 2) DEFAULT 0,
    quantDoacoes INTEGER DEFAULT 1,

    CONSTRAINT doa_pk PRIMARY KEY(cod_doador, cod_candidatura),
    CONSTRAINT doa_fk FOREIGN KEY(cod_candidatura) REFERENCES CANDIDATURA(cod_candidatura) ON DELETE CASCADE ON UPDATE CASCADE
);