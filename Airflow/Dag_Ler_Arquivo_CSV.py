
from airflow import DAG
from airflow.operators.python import PythonOperator
import pandas as pd
from datetime import datetime

# Função para ler o arquivo CSV
def read_csv_file():
    # Caminho do arquivo CSV
    file_path = "/opt/airflow/data/cliente_20231019.csv"

    # Incluir nomes de colunas personalizados usando names
    nomes_colunas = ['cd_cliente_legado', 'nm_cliente', 'cd_cpf_cnpj', 'cd_passaporte', 'tp_pessoa',
                'id_pep', 'dt_cadastro']  # Substitua pelos nomes desejados


     # Lendo o arquivo CSV com ';' como delimitador
    df = pd.read_csv(file_path, sep=';', encoding='latin1', engine='python', names=nomes_colunas)

    # Exibindo as primeiras linhas do DataFrame
    print(df.head())


 
# Definindo os argumentos padrão do DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 3, 7),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'tags': ['ETL'],
    
}   

# Definindo o DAG
dag = DAG('read_csv_dag_latin',
          default_args=default_args,
          description='Um exemplo de DAG para ler um arquivo CSV com delimitador ";"',
          schedule_interval='@once',  # Defina o intervalo de agendamento aqui
)

# Definindo a tarefa que irá ler o arquivo CSV
read_csv_task = PythonOperator(
    task_id='read_csv_task',
    python_callable=read_csv_file,
    dag=dag,
)

# Definindo a ordem de execução das tarefas
read_csv_task