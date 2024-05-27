INSERT INTO PARTIDO (cod_partido, nome) VALUES (1, NULL);  -- NULL não permitido para o nome

INSERT INTO programasDePartido (cod_partido, programa) VALUES (1, '');  -- partido 1 não existe

INSERT INTO Candidato (Cod_Candidato, nome, Partido, Estado_Ficha) VALUES (-1, 'Candidato Ilegítimo', 1, 'LIMPA');  -- Cod_Candidato negativo

INSERT INTO Cargo (Cod_Cargo, nome, Localidade, Qtd_Eleitos) VALUES (1, 'Cargo Ilegítimo', 'Localidade Teste', -1);  -- Qtd_Eleitos negativo

INSERT INTO Candidatura (Cod_Candidatura, Cod_Candidato, Cod_Cargo, Ano, Pleito, Cod_Candidatura_Vice, Eleito) VALUES (1, 1, 1, 1800, 1, NULL, FALSE);  -- Ano fora do intervalo permitido

INSERT INTO EquipeApoio (Cod_Equipe, nomeEquipe) VALUES (-1, 'Equipe Ilegítima');  -- Cod_Equipe negativo

INSERT INTO ParticipanteEquipeApoio (Cod_Participante, Cod_Equipe, Estado_Ficha) VALUES (1, 1, '');  -- Equipe 1 não existe

INSERT INTO DoadoresCampanha (Cod_Doador, Estado_Ficha, Tipo_Doador) VALUES (1, 'LIMPA', 'INVALIDO');  -- Tipo_Doador inválido

INSERT INTO ProcessoJudicial (Cod_Processo, Cod_Individuo, Data_Termino, Procedencia) VALUES (1, 1, '2024-12-31', 'INDEFINIDO');  -- Procedencia inválida

INSERT INTO DoadorFisico (Cod_Doador, CPF) VALUES (1, '1234567890');  -- CPF inválido (não possui 11 dígitos)

INSERT INTO DoadorJuridico (Cod_Doador, CNPJ) VALUES (1, '1234567890123');  -- CNPJ inválido (não possui 14 dígitos)

INSERT INTO Doa (cod_doador, cod_candidatura, valor, quantDoacoes) VALUES (1, 1, -100.00, 1);  -- Valor negativo

INSERT INTO Doa (cod_doador, cod_candidatura, valor, quantDoacoes) VALUES (1, 1, 100.00, 2);  -- Valor negativo

