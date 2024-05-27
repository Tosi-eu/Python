import psycopg2
from psycopg2 import sql, Error
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
from os import getenv

app = Flask(__name__)
load_dotenv()


### VERIFICADAS ###
def get_db_connection():
    try:
        conn = psycopg2.connect(
            dbname=getenv("DB_NAME"),
            user=getenv("USER"),
            password=getenv("PSSWD"),
            host=getenv("HOST"),
            port=getenv("PORT")
        )
        return conn
    except Error as e:
        print(f"Error connecting to the database: {e}")
        return None

@app.route('/')
def index():
    return render_template('index.html')

# Relatório de candidatos eleitos
@app.route('/candidaturas/eleitos', methods=['GET'])
def get_eleitos():
    query = """
    SELECT Candidatura.*, Candidato.Partido, Cargo.Localidade, Vice.Cod_Candidato AS Vice_Candidato
    FROM Candidatura
        JOIN Candidato ON Candidatura.Cod_Candidato = Candidato.Cod_Candidato
        JOIN Cargo ON Candidatura.Cod_Cargo = Cargo.Cod_Cargo
        LEFT JOIN Candidatura AS Vice ON Candidatura.Cod_Candidatura_Vice = Vice.Cod_Candidatura
    WHERE Candidatura.Eleito = TRUE
    """

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(query)
    candidaturas = cursor.fetchall()
    cursor.close()
    conn.close()

    result = []
    for candidatura in candidaturas:
        result.append({
            'Cod_Candidatura': candidatura[0],
            'Cod_Candidato': candidatura[1],
            'Cod_Cargo': candidatura[2],
            'Ano': candidatura[3],
            'Pleito': candidatura[4],
            'Cod_Candidatura_Vice': candidatura[5],
            'Eleito': candidatura[6],
            'Partido': candidatura[7],
            'Localidade': candidatura[8],
            'Vice_Candidato': candidatura[9]
        })
    return render_template('eleitos.html', candidaturas=result)

#############################################################

@app.route('/candidaturas', methods=['GET'])
def get_candidaturas():
    ano = request.args.get('ano')
    nome_candidato = request.args.get('nome_candidato')
    cargo = request.args.get('cargo')
    order_by = request.args.get('order_by', 'Ano')
    order_dir = request.args.get('order_dir', 'ASC')

    query = """
    SELECT Candidatura.*, Candidato.Partido, Cargo.Localidade 
    FROM Candidatura 
    JOIN Candidato ON Candidatura.Cod_Candidato = Candidato.Cod_Candidato 
    JOIN Cargo ON Candidatura.Cod_Cargo = Cargo.Cod_Cargo
    """
    filters = []
    params = []

    if ano:
        filters.append("Candidatura.Ano = %s")
        params.append(ano)
    if nome_candidato:
        filters.append("Candidato.Partido ILIKE %s")
        params.append(f"%{nome_candidato}%")
    if cargo:
        filters.append("Cargo.Localidade ILIKE %s")
        params.append(f"%{cargo}%")

    if filters:
        query += " WHERE " + " AND ".join(filters)

    query += f" ORDER BY {order_by} {order_dir}"

    conn = get_db_connection()
    if conn is None:
        return jsonify({'error': 'Database connection failed'}), 500

    try:
        cursor = conn.cursor()
        cursor.execute(query, tuple(params))
        candidaturas = cursor.fetchall()
        cursor.close()
        conn.close()
    except Error as e:
        if conn:
            conn.close()
        return jsonify({'error': str(e)}), 500

    result = []
    for candidatura in candidaturas:
        result.append({
            'Cod_Candidatura': candidatura[0],
            'Cod_Candidato': candidatura[1],
            'Cod_Cargo': candidatura[2],
            'Ano': candidatura[3],
            'Pleito': candidatura[4],
            'Cod_Candidatura_Vice': candidatura[5],
            'Eleito': candidatura[6],
            'Partido': candidatura[7],
            'Localidade': candidatura[8]
        })
    return render_template('candidaturas.html', candidaturas=result)

@app.route('/candidatos/ficha-limpa', methods=['GET'])
def get_ficha_limpa():
    query = "SELECT * FROM Candidato WHERE UPPER(Estado_Ficha) = 'LIMPA'"
    
    conn = get_db_connection()
    if conn is None:
        return jsonify({'error': 'Database connection failed'}), 500

    try:
        cursor = conn.cursor()
        cursor.execute(query)
        candidatos = cursor.fetchall()
        cursor.close()
        conn.close()
    except Error as e:
        if conn:
            conn.close()
        return jsonify({'error': str(e)}), 500

    result = []
    for candidato in candidatos:
        result.append({
            'Cod_Candidato': candidato[0],
            'Partido': candidato[1],
            'Estado_Ficha': candidato[2]
        })
    return render_template('ficha_limpa.html', candidatos=result)

# Remover entidade específica
@app.route('/delete', methods=['GET', 'POST'])
def delete_entity():
    if request.method == 'POST':
        entity = request.form['entity']
        id = request.form['id']

        table_mapping = {
            'pleito': 'pleito',
            'candidatura': 'candidatura',
            'candidato': 'candidato',
            'cargo': 'cargo',
            'equipeapoio': 'equipeapoio',
            'participanteequipeapoio': 'participanteequipeapoio',
            'doadorescampanha': 'doadorescampanha',
            'processojudicial': 'processojudicial'
        }

        id_column_mapping = {
            'pleito': 'cod_pleito',
            'candidatura': 'cod_candidatura',
            'candidato': 'cod_candidato',
            'cargo': 'cod_cargo',
            'equipeapoio': 'cod_equipe',
            'participanteequipeapoio': 'cod_participante',
            'doadorescampanha': 'cod_doador',
            'processojudicial': 'cod_processo'
        }

        id_column = id_column_mapping.get(entity.lower())
        table = table_mapping.get(entity.lower())
        query = sql.SQL("DELETE FROM {table} WHERE {id_column} = %s").format(
            table=sql.Identifier(table),
            id_column=sql.Identifier(id_column)
        )
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(query, (id,))
        conn.commit()
        cursor.close()
        conn.close()

    return render_template('delete.html', message="Entity deleted successfully")

@app.route('/inserir', methods=['GET', 'POST'])
def inserir():
    if request.method == 'POST':
        entity = request.form['entity']
        conn = get_db_connection()

        cursor = conn.cursor()
        
        if entity == 'pleito':
            cod_pleito = request.form['Cod_Pleito']
            qtd_votos = request.form['qtdVotos']
            query = "INSERT INTO pleito (cod_pleito, qtd_votos) VALUES (%s, %s)"
            cursor.execute(query, (cod_pleito, qtd_votos))

        elif entity == 'partido':
            cod_partido = request.form['cod_partido']
            nome = request.form['nome']
            query = "INSERT INTO partido (cod_partido, nome) VALUES (%s, %s)"
            cursor.execute(query, (cod_partido, nome))
        
        elif entity == 'programaPartido':
            cod_partido = request.form['cod_programaPartido']
            programa = request.form['programa']
            query = "INSERT INTO programasDePartido (cod_partido, programa) VALUES (%s, %s)"
            cursor.execute(query, (cod_partido, programa))
        
        elif entity == 'candidatura':
            codigo_candidatura = request.form['cod_candidatura']
            codigo_candidato = request.form['cod_candidato']
            codigo_cargo = request.form['cod_cargo']
            ano = request.form['ano']
            pleito = request.form['pleito']
            query = "INSERT INTO candidatura (cod_candidatura, cod_candidato, cod_cargo, ano, pleito) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(query, (codigo_candidatura, codigo_candidato, codigo_cargo, ano, pleito))
        
        elif entity == 'candidato':
            cod_candidato = request.form['codigo_candidato']
            nome = request.form['nomeCandidato']
            partido = request.form['partido']
            estado_ficha = request.form['estado_ficha']
            query = "INSERT INTO candidato (cod_candidato, nome, partido, estado_ficha) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (cod_candidato, nome, partido, estado_ficha))
        
        elif entity == 'cargo':
            codigo_cargo = request.form['cod_Cargo']
            nome = request.form['nome']
            localizacao = request.form['localidade']
            qtd_eleitos = request.form['qtd_Eleitos']
            query = "INSERT INTO cargo (cod_cargo, nome, localidade, qtd_eleitos) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (codigo_cargo, nome, localizacao, qtd_eleitos))
        
        elif entity == 'equipeapoio':
            codigo_equipe = request.form['cod_equipe']
            nome_equipe = request.form['nomeEquipe']
            query = "INSERT INTO equipeapoio (cod_equipe, nomeEquipe) VALUES (%s, %s)"
            cursor.execute(query, (codigo_equipe, nome_equipe))
        
        elif entity == 'participanteequipeapoio':
            codigo_participante = request.form['cod_participante']
            codigo_equipe = request.form['cod_Equipe']
            ficha = request.form['estado_Ficha']
            query = "INSERT INTO participanteequipeapoio (cod_participante, cod_equipe, estado_ficha) VALUES (%s, %s, %s)"
            cursor.execute(query, (codigo_participante, codigo_equipe, ficha))
        
        elif entity == 'doadorescampanha':
            codigo_doador = request.form['cod_doador']
            tipo_doador = request.form['tipo_doador']
            ficha = request.form['estado_ficha']
            cpf = request.form['cpf']
            cnpj = request.form['cnpj']

            query = "INSERT INTO doadorescampanha (cod_doador, estado_ficha, tipo_doador) VALUES (%s, %s, %s)"
            cursor.execute(query, (codigo_doador, ficha, tipo_doador))

            cursor.execute("SELECT 1 FROM doadorfisico WHERE cod_doador = %s", (codigo_doador,))
            doador_existente_f = cursor.fetchone()

            cursor.execute("SELECT 1 FROM doadorjuridico WHERE cod_doador = %s", (codigo_doador,))
            doador_existente_j = cursor.fetchone()

            if not doador_existente_f and tipo_doador == 'Físico':
                query = "INSERT INTO doadorfisico (cod_doador, cpf) VALUES (%s, %s)"
                cursor.execute(query, (codigo_doador, cpf))
            elif not doador_existente_j and tipo_doador == 'Jurídico':
                query = "INSERT INTO doadorjuridico (cod_doador, cnpj) VALUES (%s, %s)"
                cursor.execute(query, (codigo_doador, cnpj))

        elif entity == 'processojudicial':
            codigo_processo = request.form['codigo_processo']
            codigo_individuo = request.form['codigo_individuo']
            tipo_individuo = request.form['individuo_t']
            data_fim = request.form['data_termino']
            procedencia = request.form['procedencia']
            query = "INSERT INTO processojudicial (cod_processo, cod_individuo, tipo_individuo, data_termino, procedencia) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(query, (codigo_processo, codigo_individuo, tipo_individuo, data_fim, procedencia))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        message = "Dados inseridos com sucesso!"
        return render_template('inserir.html', message=message)
    
    return render_template('inserir.html')

@app.route('/doacoes', methods=['GET', 'POST'])
def doacoes():
    if request.method == 'POST':
        conn = get_db_connection()
        cursor = conn.cursor()
        cod_doador = request.form['cod_doador']
        cod_candidatura = request.form['cod_candidatura']
        valor = request.form['valor']
        quantDoacoes = request.form['quantDoacoes']
        
        try:
            cursor.execute("INSERT INTO Doa (cod_doador, cod_candidatura, valor, quantDoacoes) VALUES (%s, %s, %s, %s)", (cod_doador, cod_candidatura, valor, quantDoacoes))
            conn.commit()
        except Exception as e:
            conn.rollback()
            return f"Erro ao registrar doação: {e}"

    message = "Dados inseridos com sucesso!"
    return render_template('doacoes.html', message=message)

if __name__ == '__main__':
    app.run(debug=True)
