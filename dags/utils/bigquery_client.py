from google.cloud import bigquery


def write_to_bigquery(project_id, dataset, table, rows, schema=None):
    client = bigquery.Client(project=project_id)
    table_ref = f"{project_id}.{dataset}.{table}"

    if schema:
        bq_table = bigquery.Table(table_ref, schema=schema)
        client.create_table(bq_table, exists_ok=True)

    errors = client.insert_rows_json(table_ref, rows)

    if errors:
        raise RuntimeError(f"BigQuery insert errors: {errors}")