import json
import os
import requests
from datetime import datetime, timezone, timedelta

from airflow import DAG # type: ignore
from airflow.operators.python import PythonOperator # pyright: ignore[reportMissingImports]

from utils.bigquery_client import write_to_bigquery
from utils.schemas import INCIDENTS_SF_SCHEMA


PROJECT_ID = os.environ["GCP_PROJECT_ID"]
DATASET = os.environ["BQ_DATASET_RAW"]
TABLE = "incidents_sf"

def fetch_and_store_incidents():
    yesterday = (datetime.now(timezone.utc) - timedelta(days=1)).strftime("%Y-%m-%dT%H:%M:%S")
    params = {
        "$limit": 1000,
        "$order": "requested_datetime DESC",
        "$where": f"requested_datetime > '{yesterday}'",
    }
    headers = {"X-App-Token": os.environ["SF_311_APP_TOKEN"]}
    response = requests.get(
        "https://data.sfgov.org/resource/vw6y-z8j6.json",
        params=params,
        headers=headers,
    )
    response.raise_for_status()

    row = {
        "ingested_at": datetime.now(timezone.utc).isoformat(),
        "source": "sf_311_incidents",
        "raw_data": json.dumps(response.json()),
    }

    write_to_bigquery(PROJECT_ID, DATASET, TABLE, [row], schema=INCIDENTS_SF_SCHEMA)


with DAG(
    dag_id="ingest_incidents_sf",
    schedule_interval="0 2 * * *",
    start_date=datetime(2026, 2, 25),
    catchup=False,
    default_args={
        "retries": 1,
        "retry_delay": timedelta(minutes=5),
    },
) as dag:
    PythonOperator(
        task_id="fetch_and_store_incidents",
        python_callable=fetch_and_store_incidents,
    )