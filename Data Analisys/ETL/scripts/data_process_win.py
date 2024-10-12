import os
import gzip
import pandas as pd
import psycopg2
from tqdm import tqdm
from deep_translator import GoogleTranslator
from langdetect import detect
from constants import *
from time import sleep

columns = [
    'hashed_userid', 'masked_username', 'location', 'following', 'followers', 'totaltweets',
    'usercreateddt', 'verified', 'tweetid', 'tweetcreatedts', 'retweetcount', 'text', 'hashtags',
    'language', 'favorite_count', 'in_reply_to_status_id', 'is_quote_status', 'quoted_status_id', 'extractedts'
]

def translate_texts(**kwargs):
    db_config = kwargs['db_config']
    table_name = kwargs['table_name']
    column_name = kwargs['column_name']
    
    try:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()

        print("Selecionando textos para tradução...")
        query_select = f"SELECT hashed_userid, {column_name} FROM {table_name}"
        cursor.execute(query_select)
        rows = cursor.fetchall()

        translated_texts = []
        for row in tqdm(rows, desc="Traduzindo textos"):
            record_id = row[0]
            text = row[1]
            translated_text = text

            if text:
                try:
                    detected_language = detect(text)
                    if detected_language != 'en':         
                        translated_text = GoogleTranslator(source='auto', target='en').translate(text)
                except Exception as e:
                    print(f"Ignorando linha: {e}")

            translated_texts.append((translated_text, record_id))
        
        print("Atualizando textos traduzidos na base de dados...")
        query_update = f"UPDATE {table_name} SET {column_name} = %s WHERE hashed_userid = %s"
        for translated_text, record_id in tqdm(translated_texts, desc="Atualizando base de dados"):
            cursor.execute(query_update, (translated_text, record_id))
            conn.commit()
        
        print(f"Coluna {column_name} traduzida para inglês com sucesso na tabela {table_name}.")

    except Exception as e:
        print(f"Erro ao traduzir textos: {e}")

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def extract_gzip_files(**kwargs):
    input_dir = kwargs['input_dir']
    output_dir = kwargs['output_dir']
    
    files = [f for f in os.listdir(input_dir) if f.endswith('.gzip')]
    
    print("Extraindo arquivos GZIP...")
    for file in tqdm(files, desc="Extraindo arquivos"):
        file_path = os.path.join(input_dir, file)
        output_file_path = os.path.join(output_dir, file.replace('.gzip', '.csv'))
        
        with gzip.open(file_path, 'rb') as f_in:
            df = pd.read_csv(f_in)
            df.to_csv(output_file_path, index=False)

    print("Arquivos GZIP extraídos com sucesso.")

def read_csv_with_merged_columns(**kwargs):
    directory = kwargs['directory']

    files = [f for f in os.listdir(directory) if f.endswith('.csv') and not f.endswith('_processed.csv')]
    
    print("Processando arquivos CSV para mesclar colunas...")
    for file in tqdm(files, desc="Processando CSVs"):
        file_path = os.path.join(directory, file)
        
        df = pd.read_csv(file_path, skiprows=1, header=None, dtype=str)
        df[1] = (df[0] + '.' + df[1]).astype(float)
        df = df.drop(columns=[0])
        df.columns = columns
        
        processed_csv_filename = os.path.basename(file_path).replace('.csv', '_processed.csv')
        processed_csv_file_path = os.path.join(directory, processed_csv_filename)
        df.to_csv(processed_csv_file_path, index=False)

    print("Arquivos CSV processados com sucesso.")

def load_csv_to_postgres(**kwargs):
    csv_file_path = kwargs['csv_file_path']
    table_name = kwargs['table_name']
    db_config = kwargs['db_config']
    
    conn = psycopg2.connect(**db_config)
    cursor = conn.cursor()

    files = [f for f in os.listdir(csv_file_path) if f.endswith('_processed.csv')]
    
    print(f"Carregando dados dos CSVs processados na tabela {table_name}...")
    for file in tqdm(files, desc="Carregando CSVs"):
        full_path = os.path.join(csv_file_path, file)
        df = pd.read_csv(full_path, skiprows=1, header=None)
        df.columns = columns

        columns_str = ', '.join(df.columns)
        placeholders = ', '.join(['%s'] * len(df.columns))
        query = f"INSERT INTO {table_name} ({columns_str}) VALUES ({placeholders})"

        for _, row in df.iterrows():
            cursor.execute(query, tuple(row))

    conn.commit()
    cursor.close()
    conn.close()

    print("Dados carregados com sucesso no banco de dados.")

def execute_sql_queries(**kwargs):
    db_conf = kwargs['db_conf']
    
    try:
        conn = psycopg2.connect(**db_conf)
        cursor = conn.cursor()

        queries = [
            "DELETE FROM TWEETS_DATA WHERE TEXT LIKE '#%';",
            "DELETE FROM TWEETS_DATA WHERE LOCATION = 'NaN';",
            "DELETE FROM TWEETS_DATA WHERE TEXT LIKE '%#News%' OR TEXT LIKE '%#NEWS%' OR TEXT LIKE '%#news%';",
            "DELETE FROM TWEETS_DATA WHERE TEXT LIKE '%http%' OR TEXT LIKE '%https%'"
        ]

        print("Executando queries SQL...")
        for query in tqdm(queries, desc="Executando queries"):
            try:
                cursor.execute(query)
                conn.commit()
            except psycopg2.OperationalError as msg:
                print(f'Comando ignorado: {msg}')

        print("Queries executadas com sucesso.")

    except Exception as e:
        print(f"Erro ao executar as queries SQL: {e}")

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def etl_process():
    print("Iniciando processo ETL...")
    # extract_gzip_files(input_dir=RAW_DATA_DIR, output_dir=PROCESSED_DATA_DIR)
    # sleep(1)
    # read_csv_with_merged_columns(directory=PROCESSED_DATA_DIR)
    # sleep(1)
    load_csv_to_postgres(csv_file_path=PROCESSED_DATA_DIR, table_name=TABLE_NAME, db_config=DATABASE_CONFIG)
    sleep(1)
    execute_sql_queries(db_conf=DATABASE_CONFIG)
    sleep(1)
    translate_texts(db_config=DATABASE_CONFIG, table_name='tweets_data', column_name='text')
    print("Processo ETL concluído com sucesso.")

if __name__ == "__main__":
    etl_process()
