CREATE OR REPLACE FUNCTION check_ficha_candidato() RETURNS TRIGGER AS $$
DECLARE ficha VARCHAR(10);
BEGIN
    ficha := (SELECT estado_ficha FROM CANDIDATO WHERE cod_candidato = NEW.cod_candidato);
    IF UPPER(ficha) = 'SUJA' THEN
        RAISE EXCEPTION 'Candidatura inválida, candidato está com o nome sujo';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_valid_ficha
BEFORE INSERT ON Candidatura
FOR EACH ROW EXECUTE FUNCTION check_ficha_candidato();

CREATE OR REPLACE FUNCTION check_juridico_donation()
RETURNS TRIGGER AS $$
DECLARE
    tipo VARCHAR(50);
    ano_candidatura INTEGER;
BEGIN
    SELECT Tipo_Doador INTO tipo
    FROM DoadoresCampanha
    WHERE Cod_Doador = NEW.cod_doador;

    SELECT Ano INTO ano_candidatura
    FROM Candidatura
    WHERE Cod_Candidatura = NEW.cod_candidatura;

    IF UPPER(tipo) = 'JURÍDICO' THEN
        IF EXISTS (
            SELECT 1
            FROM Doa d
            JOIN Candidatura c ON d.cod_candidatura = c.Cod_Candidatura
            WHERE d.cod_doador = NEW.cod_doador
            AND c.Ano = ano_candidatura
        ) THEN
            RAISE EXCEPTION 'Doadores do tipo JURÍDICO só podem doar para uma candidatura por ano';
		ELSIF NEW.quantDoacoes > 1 THEN
			RAISE EXCEPTION 'Doadores do tipo JURÍDICO só podem fazer uma única doação';
        END IF;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER check_juridico_donation_trigger
BEFORE INSERT ON Doa
FOR EACH ROW
EXECUTE FUNCTION check_juridico_donation();

CREATE OR REPLACE FUNCTION update_ficha_processo()
RETURNS TRIGGER AS $$
DECLARE
    ficha VARCHAR(10);
BEGIN
    SELECT estado_ficha INTO ficha
    FROM Candidato
    WHERE cod_candidato = NEW.Cod_Individuo;

    IF UPPER(ficha) = 'LIMPA' THEN
        UPDATE Candidato
        SET estado_ficha = 'SUJA'
        WHERE cod_candidato = NEW.Cod_Individuo;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_ficha_trigger
AFTER INSERT ON ProcessoJudicial
FOR EACH ROW
EXECUTE FUNCTION update_ficha_processo();

CREATE OR REPLACE FUNCTION check_valid_individuo() RETURNS TRIGGER AS $$
BEGIN
    IF UPPER(NEW.Tipo_Individuo) = 'CANDIDATO' THEN
        IF NOT EXISTS (SELECT 1 FROM Candidato WHERE Cod_Candidato = NEW.Cod_Individuo) THEN
            RAISE EXCEPTION 'Candidato de id = % não encontrado', NEW.Cod_Individuo;
        END IF;
    ELSIF UPPER(NEW.Tipo_Individuo) = 'PARTICIPANTE EA' THEN
        IF NOT EXISTS (SELECT 1 FROM ParticipanteEquipeApoio WHERE Cod_Participante = NEW.Cod_Individuo) THEN
            RAISE EXCEPTION 'Participante de equipe de apoio de id = % não encontrado', NEW.Cod_Individuo;
        END IF;
    ELSIF UPPER(NEW.Tipo_Individuo) = 'DOADOR' THEN
        IF NOT EXISTS (SELECT 1 FROM DoadoresCampanha WHERE Cod_Doador = NEW.Cod_Individuo) THEN
            RAISE EXCEPTION 'Doador de campanha de id = % não encontrado', NEW.Cod_Individuo;
        END IF;
    ELSE
        RAISE EXCEPTION 'Tipo de indivíduo inválido: %', NEW.Tipo_Individuo;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER check_valid_individuo_trigger
BEFORE INSERT OR UPDATE ON ProcessoJudicial
FOR EACH ROW
EXECUTE FUNCTION check_valid_individuo();

-- Função para verificar se o cod_doador já existe na tabela oposta
CREATE OR REPLACE FUNCTION check_doador() RETURNS TRIGGER AS $$
BEGIN
    -- Verifica se está tentando inserir em DoadorFisico
    IF TG_TABLE_NAME = 'doadorfisico' THEN
        -- Verifica se o cod_doador já existe em DoadorJuridico
        IF EXISTS (SELECT 1 FROM doadorjuridico WHERE cod_doador = NEW.cod_doador) THEN
            RAISE EXCEPTION 'Cod_doador % já existe em DoadorJuridico', NEW.cod_doador;
        END IF;
    -- Verifica se está tentando inserir em DoadorJuridico
    ELSIF TG_TABLE_NAME = 'doadorjuridico' THEN
        -- Verifica se o cod_doador já existe em DoadorFisico
        IF EXISTS (SELECT 1 FROM doadorfisico WHERE cod_doador = NEW.cod_doador) THEN
            RAISE EXCEPTION 'Cod_doador % já existe em DoadorFisico', NEW.cod_doador;
        END IF;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger para verificar inserções em DoadorFisico
CREATE TRIGGER check_doador_fisico
BEFORE INSERT ON DoadorFisico
FOR EACH ROW
EXECUTE FUNCTION check_doador();

-- Trigger para verificar inserções em DoadorJuridico
CREATE TRIGGER check_doador_juridico
BEFORE INSERT ON DoadorJuridico
FOR EACH ROW
EXECUTE FUNCTION check_doador();

CREATE OR REPLACE FUNCTION check_valid_candidatura() RETURNS TRIGGER AS $$
BEGIN

    IF NEW.Cod_Candidatura_Vice IS NOT NULL AND
       NOT EXISTS (SELECT 1 FROM Candidato WHERE Cod_Candidato = NEW.Cod_Candidatura_Vice) THEN
        RAISE EXCEPTION 'Candidatura de vice é inválida';
    END IF;

    IF NEW.Cod_Candidatura_Vice IS NOT NULL AND
       EXISTS (SELECT 1 FROM Candidatura WHERE Cod_Candidato = NEW.Cod_Candidatura_Vice) THEN
        RAISE EXCEPTION 'Candidato já possui uma candidatura e não pode ser vice de outro candidato';
    END IF;

    IF NEW.Cod_Candidatura = NEW.Cod_Candidatura_Vice THEN
        RAISE EXCEPTION 'Candidato não pode ser seu próprio vice';
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_valid_vice
BEFORE INSERT OR UPDATE ON Candidatura
FOR EACH ROW EXECUTE FUNCTION check_valid_candidatura();
