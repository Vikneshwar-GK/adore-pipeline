import json
import os
import requests
from datetime import datetime, timezone, timedelta

from airflow import DAG # type: ignore
from airflow.operators.python import PythonOperator # pyright: ignore[reportMissingImports]

from utils.bigquery_client import write_to_bigquery
from utils.schemas import WEATHER_SF_SCHEMA


PROJECT_ID = os.environ["GCP_PROJECT_ID"]
DATASET = os.environ["BQ_DATASET_RAW"]
TABLE = "weather_sf"

def fetch_and_store_weather():
    url = os.environ["OPEN_METEO_BASE_URL"]
    params = {
        "latitude": 37.7749,
        "longitude": -122.4194,
        "hourly": "temperature_2m,precipitation,windspeed_10m,relativehumidity_2m",
    }
    response = requests.get(url, params=params)
    response.raise_for_status()

    row = {
        "ingested_at": datetime.now(timezone.utc).isoformat(),
        "source": "open_meteo_sf",
        "raw_data": json.dumps(response.json()),
    }

    write_to_bigquery(PROJECT_ID, DATASET, TABLE, [row], schema=WEATHER_SF_SCHEMA)


with DAG(
    dag_id="ingest_weather_sf",
    schedule_interval="*/15 * * * *",
    start_date=datetime(2026, 2, 25),
    catchup=False,
    default_args={
        "retries": 1,
        "retry_delay": timedelta(minutes=5),
    },
) as dag:
    PythonOperator(
        task_id="fetch_and_store_weather",
        python_callable=fetch_and_store_weather,
    )