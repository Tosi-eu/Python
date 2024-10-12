import os
from deep_translator import GoogleTranslator
import pandas as pd
import gzip
import psycopg2
from tqdm import tqdm
from constants import *
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from langdetect import detect
import subprocess as sub

columns = ['hashed_userid',	'masked_username',	'location',	'following',	'followers',	'totaltweets',
          	'usercreateddt',	'verified',	'tweetid',	'tweetcreatedts',	'retweetcount',	'text',	'hashtags',
            'language',	'favorite_count',	'in_reply_to_status_id',	'is_quote_status',	'quoted_status_id',	'extractedts']

def translate_texts(db_config, table_name, column_name):
    try:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()

        query_select = f"SELECT hashed_userid, {column_name} FROM {table_name}"
        cursor.execute(query_select)
        rows = cursor.fetchall()

        print(f"Selecionando e traduzindo textos da coluna {column_name}...\n")

        translated_texts = []
        for row in tqdm(rows, desc="Traduzindo textos"):
            record_id = row[0]
            text = row[1]
            if text:
                try:
                    detected_language = detect(text)
                    if detected_language not in ('en', 'fr', 'es'):         
                        translated_text = GoogleTranslator(source='auto', target='en').translate(text)
                except Exception as e:
                    print(f"Ignorirando linha: {e}")
                    translated_text = text

            translated_texts.append((translated_text, record_id))
        
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

# Funções ETL
def extract_gzip_files(**kwargs):
    input_dir = kwargs['input_dir']
    output_dir = kwargs['output_dir']
    files = [f for f in os.listdir(input_dir) if f.endswith('.gzip')]

    for file in files:
        file_path = os.path.join(input_dir, file)
        output_file_path = os.path.join(output_dir, file.replace('.gzip', '.csv'))
        
        with gzip.open(file_path, 'rb') as f_in:
            df = pd.read_csv(f_in)    
            df.to_csv(output_file_path, index=False)

def read_csv_with_merged_columns(**kwargs):
    directory = kwargs['directory']
    for file in os.listdir(directory):
        if file.endswith('.csv') and not file.endswith('_processed.csv'):
            file_path = os.path.join(directory, file)
            
            df = pd.read_csv(file_path, skiprows=1, header=None, dtype=str)
            df[1] = (df[0] + '.' + df[1]).astype(float)
            df = df.drop(columns=[0])
            df.columns = columns
            
            processed_csv_filename = os.path.basename(file_path).replace('.csv', '_processed.csv')
            processed_csv_file_path = os.path.join(directory, processed_csv_filename)
            df.to_csv(processed_csv_file_path, index=False)

def load_csv_to_postgres(**kwargs):
    csv_file_path = kwargs['csv_file_path']
    table_name = kwargs['table_name']
    db_config = kwargs['db_config']
    
    conn = psycopg2.connect(**db_config)
    cursor = conn.cursor()

    for file in os.listdir(csv_file_path):
        if file.endswith('_processed.csv'):
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

def execute_sql_script(script_path, db_config):
    try:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()

        with open(SQL_PATH, 'r') as script_file:
            sql_script = script_file.read()
        
        cursor.execute(sql_script)
        conn.commit()

        print(f"Script SQL {script_path} executado com sucesso.")

    except Exception as e:
        print(f"Erro ao executar o script SQL: {e}")

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 8, 29),
    'retries': 1,
}

dag = DAG(
    'etl_process',
    default_args=default_args,
    schedule=None,  
)

extract_task = PythonOperator(
    task_id='extract_gzip_files',
    python_callable=extract_gzip_files,
    op_kwargs={'input_dir': RAW_DATA_DIR, 'output_dir': PROCESSED_DATA_DIR},
    dag=dag,
)

pre_process_task = PythonOperator(
    task_id='process_csv_files',
    python_callable=read_csv_with_merged_columns,
    op_kwargs={'directory': PROCESSED_DATA_DIR},
    dag=dag,
)

load_task = PythonOperator(
    task_id='load_csv_to_postgres',
    python_callable=load_csv_to_postgres,
    op_kwargs={
        'csv_file_path': PROCESSED_DATA_DIR,
        'table_name': TABLE_NAME,
        'db_config': DATABASE_CONFIG
    },
    dag=dag,
)

process2_task = PythonOperator(
    task_id='treat_database',
    python_callable=execute_sql_script,
    op_kwargs={
        'script_path': SQL_PATH,  
        'db_config': DATABASE_CONFIG
    },
    dag=dag,
)

extract_task >> pre_process_task >> load_task >> process2_task
