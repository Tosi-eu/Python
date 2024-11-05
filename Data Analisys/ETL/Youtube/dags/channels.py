from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
import json
from alpha_vantage.timeseries import TimeSeries
from time import sleep
from os import path, makedirs
from constants import API

# Variável para capturar o erro da API
api_error_message = ""

# Função que coleta as cotações e salva em arquivo JSON
def fetch_quotes(**context):
    global api_error_message  # Captura o erro globalmente para o BashOperator
    series = TimeSeries(key=API)

    symbols = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'META', 'NVDA', 'BRK.A', 'V', 'JPM']

    quotes = {}
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    directory = 'datalake/raw_data'
    filename = f'quotes_{timestamp}.json'
    filepath = path.join(directory, filename)

    # Cria o diretório se não existir
    makedirs(directory, exist_ok=True)

    for symbol in symbols:
        try:
            data, _ = series.get_quote_endpoint(symbol=symbol)
            quotes[symbol] = data
            print(f"Obtido {symbol}")
            sleep(12)  
        except Exception as e:
            api_error_message = str(e) 
            context['task_instance'].xcom_push(key='api_error', value=api_error_message) 
            print(f"Erro ao buscar {symbol}: {api_error_message}")
            continue

    with open(filepath, 'w+') as json_file:
        json.dump(quotes, json_file, indent=4, sort_keys=True)

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 10, 25),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    dag_id='fetch_stock_quotes_dag',
    default_args=default_args,
    description='DAG para coletar cotações de ações e salvar em JSON',
    schedule='@hourly', 
)

fetch_quotes_task = PythonOperator(
    task_id='fetch_quotes',
    python_callable=fetch_quotes,
    provide_context=True,
    dag=dag,
)

echo_errors_task = BashOperator(
    task_id='echo_errors',
    bash_command="echo '{{ ti.xcom_pull(task_ids='fetch_quotes', key='api_error') }}'",  
    trigger_rule='one_failed', 
    dag=dag,
)

fetch_quotes_task >> echo_errors_task
