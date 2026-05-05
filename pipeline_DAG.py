import datetime as dt
from datetime import timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from sqlalchemy import create_engine
import pandas as pd
import psycopg2

"""
the pipeline step:
Retrieve data from the PostgreSQL database (final_project_rmt53), 
then merge all tables into a single table with the required columns, 
followed by data cleaning, 
and finally save it as a CSV file (data_clean.csv) in a separate database (data_ready)
"""

def fetchData():
    # Replace these parameters with your actual database credentials
    db_user = "airflow"
    db_password = "airflow" #Use your own password
    db_host = "postgres"  # Usually "localhost" if running locally
    db_port = "5432"  # Default is 5432

    connection = psycopg2.connect(
        user=db_user,
        password=db_password,
        host=db_host,
        port=db_port,
        database = "final_project_rmt53"
    )

    query = """
            SELECT
            u.user_id, u.age, u.employment_type, u.monthly_income, u.location, u.debt_to_income_ratio, u.app_usage_frequency,
        t.transaction_date, t.purchase_amount, t.product_category, t.bnpl_installments,
        p.repayment_delay_days, p.missed_payments, p.default_flag,
        r.credit_score, r.risk_score, r.customer_segment

        FROM transactions t

        JOIN users u ON t.user_id = u.user_id
    	JOIN payments p ON t.transaction_id = p.transaction_id
    	JOIN risk_assesment r ON u.user_id = r.user_id;
        """


    df = pd.read_sql (query, connection)
    df.to_csv('/opt/airflow/dags/table_final.csv', index = False)
    connection.close()

def cleanData():
    df=pd.read_csv('/opt/airflow/dags/table_final.csv')
    
    """
    During the data cleaning process, duplicate records are removed to prevent redundant information. 
    Column names are then standardized to ensure consistency, which will simplify the analysis process later on.
    
    Missing values in the ‘customer_segment’ column will be filled with ‘unknown’,
    and missing values in the ‘repayment_delay’ column will be filled with 0 to facilitate analysis and decision-making.
    
    """

    #convert 'date' data to the 'date' type
    df['transaction_date'] = pd.to_datetime(df['transaction_date'])
    df['transaction_date'] = df['transaction_date'].dt.date 

    #drop duplicate
    df.drop_duplicates(inplace=True)


    #manipulate the column name
    df.columns = (
        df.columns
        .str.lower()
        .str.strip()
        .str.replace(" ", "_")
        .str.replace(r"[^\w]", "", regex=True)
    )

    #handle missing value
    
    df['repayment_delay_days'] = df['repayment_delay_days'].fillna(0)

    df['customer_segment'] = df['customer_segment'].fillna("unknown")


    #saving data clean
    df.to_csv('/opt/airflow/dags/clean_data.csv', index=False)


def loadToReady():
    # the Credentials for database target
    db_params = {
        "user": "airflow",
        "password": "airflow",
        "host": "postgres", 
        "port": "5432",
        "database": "data_ready"
    }
    
    # Reading the cleaned data
    df = pd.read_csv('/opt/airflow/dags/clean_data.csv')
    
    
    engine = create_engine(f'postgresql://{db_params["user"]}:{db_params["password"]}@{db_params["host"]}:{db_params["port"]}/{db_params["database"]}')
    
    # Saving to the new/different database
    # Use 'append' so when the new data is added, the old data will be not be deleted or overwritten
    df.to_sql('bnpl_ready_table', engine, if_exists='append', index=False)
     



    """
    Pipeline schedulling will be begin in 4 May 2026
    """
default_args = {
    'owner': 'ali',
    'start_date': dt.datetime(2026, 5, 4) , #jadwal mulai
    'retries': 1,
    'retry_delay': dt.timedelta(minutes=1),
}


"""
The pipeline schedule will be carried out on the 1st of every month
"""
with DAG('pipeline_final_project',
         default_args=default_args,
         schedule_interval= '0 2 1 * *',     
         catchup=False
         ) as dag:
    


    fetch_data = PythonOperator(task_id='fetch_postgre',
                                    python_callable=fetchData)

    clean_data = PythonOperator(task_id='clean_data',
                                    python_callable=cleanData)
    
    task_load = PythonOperator(task_id='load_to_database_ready',
                                    python_callable=loadToReady)
    

   

fetch_data >> clean_data >> task_load