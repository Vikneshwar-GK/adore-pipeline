import json
import os
import requests
from datetime import datetime, timezone, timedelta

from airflow import DAG # type: ignore
from airflow.operators.python import PythonOperator # pyright: ignore[reportMissingImports]

from utils.bigquery_client import write_to_bigquery
from utils.schemas import TRANSIT_SF_SCHEMA


PROJECT_ID = os.environ["GCP_PROJECT_ID"]
DATASET = os.environ["BQ_DATASET_RAW"]
TABLE = "transit_sf"

def fetch_and_store_transit():
    params = {
        "api_key": os.environ["API_511_TOKEN"],
        "agency": "SF",
        "format": "json",
    }
    response = requests.get("http://api.511.org/transit/TripUpdates", params=params)
    response.raise_for_status()

    row = {
        "ingested_at": datetime.now(timezone.utc).isoformat(),
        "source": "511_transit_sf",
        "raw_data": response.content.decode("utf-8-sig"),
    }

    write_to_bigquery(PROJECT_ID, DATASET, TABLE, [row], schema=TRANSIT_SF_SCHEMA)


with DAG(
    dag_id="ingest_transit_sf",
    schedule_interval="*/15 * * * *",
    start_date=datetime(2026, 2, 25),
    catchup=False,
    default_args={
        "retries": 1,
        "retry_delay": timedelta(minutes=5),
    },
) as dag:
    PythonOperator(
        task_id="fetch_and_store_transit",
        python_callable=fetch_and_store_transit,
    )