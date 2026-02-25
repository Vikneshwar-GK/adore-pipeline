from google.cloud import bigquery

WEATHER_SF_SCHEMA = [
    bigquery.SchemaField("ingested_at", "TIMESTAMP"),
    bigquery.SchemaField("source", "STRING"),
    bigquery.SchemaField("raw_data", "STRING"),
]