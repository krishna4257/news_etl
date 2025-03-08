from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import logging
from extract import extract_news
from transform import transform_news
from load import load_news_to_neon

# ✅ Configure Logging for ETL Monitoring
log_file = "/opt/airflow/logs/news_etl_pipeline.log"
logging.basicConfig(filename=log_file, level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# ✅ Default DAG Arguments
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2024, 1, 1),
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
}

# ✅ Define the DAG
dag = DAG(
    "news_etl_pipeline",
    default_args=default_args,
    description="Automated ETL Pipeline for News Data",
    schedule="0 9 * * *",  # ✅ Runs Daily at 9 AM UTC
    catchup=False,
)

# ✅ Task Functions with Proper Data Flow
def extract():
    """Extract news data from API."""
    logging.info("🔍 [ETL] Starting Extraction Step...")
    news_data = extract_news()  # ✅ Extract news articles
    logging.info(f"✅ [ETL] Extracted {len(news_data)} articles.")
    return news_data  # ✅ Send data to XCom for transform step

def transform(ti):
    """Transform extracted news data."""
    logging.info("🔄 [ETL] Starting Transformation Step...")
    
    # ✅ Retrieve extracted data from XCom
    news_data = ti.xcom_pull(task_ids="extract_task")
    
    if not news_data:
        logging.warning("⚠️ No news data received. Skipping transformation.")
        return []
    
    transformed_data = transform_news(news_data)  # ✅ Transform data
    logging.info(f"✅ [ETL] Transformed {len(transformed_data)} articles.")
    
    return transformed_data  # ✅ Send transformed data to XCom for load step

def load(ti):
    """Load transformed news data into NeonDB."""
    logging.info("💾 [ETL] Starting Load Step...")
    
    # ✅ Retrieve transformed data from XCom
    transformed_data = ti.xcom_pull(task_ids="transform_task")
    
    if not transformed_data:
        logging.warning("⚠️ No transformed data available. Skipping load step.")
        return
    
    load_news_to_neon(transformed_data)  # ✅ Insert data into NeonDB
    
    logging.info("✅ [ETL] Load Complete. Data successfully stored in NeonDB.")

# ✅ Define Airflow Tasks
extract_task = PythonOperator(
    task_id="extract_task",
    python_callable=extract,
    dag=dag,
)

transform_task = PythonOperator(
    task_id="transform_task",
    python_callable=transform,
    dag=dag,
)

load_task = PythonOperator(
    task_id="load_task",
    python_callable=load,
    dag=dag,
)

# ✅ Define Task Execution Order
extract_task >> transform_task >> load_task
