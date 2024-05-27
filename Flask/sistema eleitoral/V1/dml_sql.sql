INSERT INTO Pleito (Cod_Pleito, Qtd_Votos) VALUES
(1, 200934), (2, 354200), (3, 100000), (4, 587410), (5, 245000),
(6, 985254), (7, 114254), (8, 421589), (9, 102325), (10, 104254);

INSERT INTO EquipeApoio (Nome) VALUES
('Equipe Alfa'), ('Equipe Beta'), ('Equipe Gama'), ('Equipe Delta'), ('Equipe Epsilon'),
('Equipe Zeta'), ('Equipe Eta'), ('Equipe Theta'), ('Equipe Iota'), ('Equipe Kappa');

INSERT INTO Individuo (CPF, Nome, Cod_Equipe) VALUES
(10000000026, 'Amanda Silva', 26), (10000000027, 'Bruno Carvalho', 27),
(10000000028, 'Cecilia Azevedo', 28), (10000000029, 'Diego Machado', 29), (10000000030, 'Elisa Barbosa', 30),
(10000000031, 'Felipe Sousa', 21), (10000000032, 'Gustavo Ferreira', 22), (10000000033, 'Heloisa Melo', 23),
(10000000034, 'Isabela Andrade', 24), (10000000035, 'João Moraes', 25), (10000000036, 'Karina Mendes', 26),
(10000000037, 'Leonardo Cardoso', 27), (10000000038, 'Marcelo Santos', 28), (10000000039, 'Natalia Lima', 29),
(10000000040, 'Oscar Freitas', 30), (10000000041, 'Patricia Mota', 21), (10000000042, 'Rafael Teixeira', 22),
(10000000043, 'Samuel Mendes', 23), (10000000044, 'Thiago Ribeiro', 24), (10000000045, 'Vera Alves', 25),
(10000000046, 'William Barros', 26), (10000000047, 'Ana Claudia Silva', 27), (10000000048, 'Bruno Lima', 28),
(10000000049, 'Catarina Souza', 29), (10000000050, 'Daniel Gomes', 30), (10000000051, 'Eduardo Martins', 21),
(10000000052, 'Fabiana Santos',22), (10000000053, 'Gilberto Lima', 23), (10000000054, 'Hugo Gonçalves', 24),
(10000000055, 'Isabel Torres', 25), (10000000056, 'Joana Castro', 26), (10000000057, 'Kevin Dias', 27),
(10000000058, 'Lara Azevedo', 28), (10000000059, 'Marcos Ferreira', 29), (10000000060, 'Nadia Souza', 30),
(10000000061, 'Otavio Lima', 21), (10000000062, 'Priscila Mendes', 22), (10000000063, 'Renato Freitas', 23),
(10000000064, 'Sara Andrade', 24), (10000000065, 'Tatiana Costa', 25), (10000000066, 'Ulisses Pereira', 26),
(10000000067, 'Victor Barbosa', 27), (10000000068, 'Walter Nunes', 28), (10000000069, 'Xuxa Oliveira', 29),
(10000000070, 'Yuri Ribeiro', 30), (10000000071, 'Zilda Silva', 21), (10000000072, 'Alberto Mendes', 22),
(10000000073, 'Beatriz Carvalho', 23), (10000000074, 'Caio Oliveira', 24), (10000000075, 'Diana Souza', 25),
(10000000076, 'Emilio Lima', 26), (10000000077, 'Fernanda Ribeiro', 27), (10000000078, 'Gustavo Silva', 28),
(10000000079, 'Helena Mendes', 29), (10000000080, 'Isabela Sousa', 30), (10000000081, 'José Oliveira', 21),
(10000000082, 'Karla Silva', 22), (10000000083, 'Leonardo Pereira', 23), (10000000084, 'Marta Costa', 24),
(10000000085, 'Nicolas Nunes', 25), (10000000086, 'Olivia Martins', 26), (10000000087, 'Paulo Andrade', 27),
(10000000088, 'Quintino Lima', 28), (10000000089, 'Rita Souza', 29), (10000000090, 'Samuel Ferreira', 30),
(10000000091, 'Tereza Araujo', 21), (10000000092, 'Ursula Mendes', 22), (10000000093, 'Vicente Oliveira', 23),
(10000000094, 'Wesley Nunes', 24), (10000000095, 'Xander Lima', 25), (10000000096, 'Yara Souza', 26),
(10000000097, 'Zuleica Silva', 27), (10000000098, 'Anderson Araujo', 28), (10000000099, 'Beto Costa', 29),
(10100000000, 'Carla Lima', 30);

INSERT INTO Individuo (CPF, Nome, Cod_Equipe) VALUES
(10000000002, 'Bruno Souza', NULL),(10000000003, 'Carla Oliveira', NULL),(10000000004, 'Daniel Pereira', NULL),
(10000000005, 'Eduardo Costa', NULL),(10000000006, 'Fernanda Lima', NULL),(10000000007, 'Gabriel Alves', NULL),
(10000000008, 'Helena Rocha', NULL),(10000000009, 'Igor Ribeiro', NULL),(10000000010, 'Julia Santos', NULL),
(10000000011, 'Luis Martins', NULL),(10000000012, 'Mariana Fernandes', NULL),(10000000013, 'Nicolas Ferreira', NULL),
(10000000014, 'Olivia Gonçalves', NULL),(10000000015, 'Paulo Almeida', NULL),(10000000016, 'Quintino Barbosa', NULL),
(10000000017, 'Renata Araujo', NULL),(10000000018, 'Sergio Castro', NULL),(10000000019, 'Tatiana Cunha', NULL),
(10000000020, 'Ulisses Dias', NULL),(10000000021, 'Vanessa Nunes', NULL),(10000000022, 'Wagner Monteiro', NULL),
(10000000023, 'Xavier Pinto', NULL),(10000000024, 'Yasmin Oliveira', NULL),(10000000025, 'Zeca Rodrigues', NULL);



INSERT INTO ProgramaPartido (Descricao) VALUES
('Programa de Desenvolvimento Econômico'), ('Programa de Saúde e Educação'),
('Programa de Infraestrutura'), ('Programa de Meio Ambiente');

INSERT INTO Partido (Nome, Cod_Programa) VALUES
('Partido Progressista', 1), ('Partido Social', 2), ('Partido Liberal', 3), ('Partido Verde', 4);

INSERT INTO Cargo (Descricao, Localidade, Qtd_Eleitos, Pais, Estado, Cidade) VALUES
('Presidente', 'FEDERAL', 1, 'BRASIL', NULL, NULL),
('Prefeito', 'MUNICIPAL', 1, 'BRASIL', 'São Paulo', 'São Paulo'),
('Prefeito', 'MUNICIPAL', 1, 'BRASIL', 'Rio de Janeiro', 'Rio de Janeiro'),
('Governador', 'ESTADUAL', 1, 'BRASIL', 'Rio de Janeiro', NULL),
('Deputado Federal', 'FEDERAL', 10, 'BRASIL', NULL, NULL),
('Deputado Estadual', 'ESTADUAL', 10, 'BRASIL', 'Minas Gerais', NULL),
('Senador', 'FEDERAL', 3, 'BRASIL', NULL, NULL),
('Prefeito', 'MUNICIPAL', 1, 'BRASIL', 'Minas Gerais', 'Belo Horizonte'),
('Prefeito', 'MUNICIPAL', 1, 'BRASIL', 'Minas Gerais', 'Uberlândia'),
('Prefeito', 'MUNICIPAL', 1, 'BRASIL', 'São Paulo', 'Campinas');

INSERT INTO Candidatura (Cod_Candidato, Cod_Cargo, Cod_Partido, Ano, Cod_Pleito, Cod_Candidatura_Vice) VALUES
(10000000001, 1, 1, 2024, 1, NULL), (10000000002, 2, 2, 2024, 2, NULL), 
(10000000003, 3, 3, 2024, 3, NULL), (10000000004, 4, 4, 2024, 4, NULL),
(10000000005, 5, 1, 2024, 5, NULL), (10000000006, 6, 2, 2024, 6, NULL),
(10000000007, 7, 3, 2024, 7, NULL), (10000000008, 8, 4, 2024, 8, NULL),
(10000000009, 9, 1, 2024, 9, NULL), (10000000010, 10, 2, 2024, 10, NULL),
(10000000011, 1, 1, 2024, 1, NULL), (10000000012, 2, 2, 2024, 2, NULL),
(10000000013, 3, 3, 2024, 3, NULL), (10000000014, 4, 4, 2024, 4, NULL),
(10000000015, 5, 1, 2024, 5, NULL), (10000000016, 6, 2, 2024, 6, NULL),
(10000000017, 7, 3, 2024, 7, NULL), (10000000018, 8, 4, 2024, 8, NULL),
(10000000019, 9, 1, 2024, 9, NULL), (10000000020, 10, 2, 2024, 10, NULL),
(10000000021, 1, 1, 2024, 1, NULL), (10000000022, 2, 2, 2024, 2, NULL),
(10000000023, 3, 3, 2024, 3, NULL), (10000000024, 4, 4, 2024, 4, NULL),
(10000000025, 5, 1, 2024, 5, NULL);

INSERT INTO ProcessoJudicial (Cod_Individuo, Data_Inicio, Julgado, Data_Termino, Procedente) VALUES
(10000000001, '2022-01-01', TRUE, '2023-01-01', TRUE), (10000000002, '2022-01-01', TRUE, '2023-01-01', FALSE),
(10000000003, '2022-01-01', FALSE, NULL, NULL), (10000000004, '2022-01-01', TRUE, '2023-01-01', TRUE),
(10000000005, '2022-01-01', TRUE, '2023-01-01', FALSE), (10000000006, '2022-01-01', FALSE, NULL, NULL),
(10000000007, '2022-01-01', TRUE, '2023-01-01', TRUE), (10000000008, '2022-01-01', TRUE, '2023-01-01', FALSE),
(10000000009, '2022-01-01', FALSE, NULL, NULL), (10000000010, '2022-01-01', TRUE, '2023-01-01', TRUE),
(10000000011, '2022-01-01', TRUE, '2023-01-01', TRUE), (10000000012, '2022-01-01', TRUE, '2023-01-01', FALSE),
(10000000013, '2022-01-01', FALSE, NULL, NULL), (10000000014, '2022-01-01', TRUE, '2023-01-01', TRUE),
(10000000015, '2022-01-01', TRUE, '2023-01-01', FALSE), (10000000016, '2022-01-01', FALSE, NULL, NULL),
(10000000017, '2022-01-01', TRUE, '2023-01-01', TRUE), (10000000018, '2022-01-01', TRUE, '2023-01-01', FALSE),
(10000000019, '2022-01-01', FALSE, NULL, NULL), (10000000020, '2022-01-01', TRUE, '2023-01-01', TRUE),
(10000000021, '2022-01-01', TRUE, '2023-01-01', TRUE), (10000000022, '2022-01-01', TRUE, '2023-01-01', FALSE),
(10000000023, '2022-01-01', FALSE, NULL, NULL), (10000000024, '2022-01-01', TRUE, '2023-01-01', TRUE),
(10000000025, '2022-01-01', TRUE, '2023-01-01', FALSE);

INSERT INTO Empresa (CNPJ, Nome) VALUES
(12345678000100, 'Tech Innovations'), (23456789000111, 'Global Enterprises'), 
(34567890000122, 'Green Solutions'), (45678901000133, 'Health First'),
(56789012000144, 'EduTech Corp'), (67890123000155, 'AgroFuture'),
(78901234000166, 'FinTech Leaders'), (89012345000177, 'Retail Giants'),
(90123456000188, 'Construction Masters'), (11234567000199, 'Auto World');


INSERT INTO DoacaoPF (Cod_Individuo, Valor, data_doacao, Cod_Candidatura) VALUES
(10000000027, 600.00, '2024-05-02', 2),
(10000000028, 700.00, '2024-05-03', 3),(10000000029, 800.00, '2024-05-04', 4),(10000000030, 900.00, '2024-05-05', 5),
(10000000031, 1000.00, '2024-05-06', 6),(10000000032, 1100.00, '2024-05-07', 7),(10000000033, 1200.00, '2024-05-08', 8),
(10000000034, 1300.00, '2024-05-09', 9),(10000000035, 1400.00, '2024-05-10', 10),(10000000036, 1500.00, '2024-05-11', 11),
(10000000037, 1600.00, '2024-05-12', 12),(10000000038, 1700.00, '2024-05-13', 13),(10000000039, 1800.00, '2024-05-14', 14),
(10000000040, 1900.00, '2024-05-15', 15),(10000000041, 2000.00, '2024-05-16', 16),(10000000042, 2100.00, '2024-05-17', 17),
(10000000043, 2200.00, '2024-05-18', 18),(10000000044, 2300.00, '2024-05-19', 19),(10000000045, 2400.00, '2024-05-20', 20);

INSERT INTO DoadorPJ (Cod_Candidatura, Cod_Empresa, Valor, data_doacao) VALUES
(2, 23456789000111, 6000.00, '2024-05-02'),
(3, 34567890000122, 7000.00, '2024-05-03'), (4, 45678901000133, 8000.00, '2024-05-04'),
(5, 56789012000144, 9000.00, '2024-05-05'), (6, 67890123000155, 10000.00, '2024-05-06'),
(7, 78901234000166, 11000.00, '2024-05-07'), (8, 89012345000177, 12000.00, '2024-05-08'),
(9, 90123456000188, 13000.00, '2024-05-09'), (10, 11234567000199, 14000.00, '2024-05-10'),
(11, 12345678000100, 5000.00, '2024-05-11'), (12, 23456789000111, 6000.00, '2024-05-12'),
(13, 34567890000122, 7000.00, '2024-05-13'), (14, 45678901000133, 8000.00, '2024-05-14'),
(15, 56789012000144, 9000.00, '2024-05-15'), (16, 67890123000155, 10000.00, '2024-05-16'),
(17, 78901234000166, 11000.00, '2024-05-17'), (18, 89012345000177, 12000.00, '2024-05-18'),
(19, 90123456000188, 13000.00, '2024-05-19'), (20, 11234567000199, 14000.00, '2024-05-20');




