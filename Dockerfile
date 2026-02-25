FROM apache/airflow:2.8.1
RUN pip install google-cloud-bigquery apache-airflow-providers-google