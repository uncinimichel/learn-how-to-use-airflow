import csv
import time

import requests
from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults


class DataToPostgresOperator(BaseOperator):
    copy_csv_sql = """
        COPY {}
        FROM '{}'
        DELIMITER '{}'
        NULL ''
        CSV HEADER
    """

    @apply_defaults
    def __init__(self,
                 postgres_conn_id="",
                 table="",
                 data_url="",
                 delimiter=",",
                 source_type="csv",
                 ignore_headers=1,
                 *args, **kwargs):
        super(DataToPostgresOperator, self).__init__(*args, **kwargs)
        self.table = table
        self.postgres_conn_id = postgres_conn_id
        self.data_url = data_url
        self.delimiter = delimiter
        self.source_type = source_type
        self.ignore_headers = ignore_headers

    def execute(self, context):
        postgres = PostgresHook(postgres_conn_id=self.postgres_conn_id)

        self.log.info("Clearing data from destination Redshift table")
        postgres.run("DELETE FROM {}".format(self.table), autocommit=True)

        if self.source_type == "csv":
            file_name = self.table.split(".")
            with open(f"/data/{file_name[1]}.csv", "w+") as f:
                data = requests.get(self.data_url)
                writer = csv.writer(f)
                reader = csv.reader(data.text.splitlines())

                for row in reader:
                    writer.writerow(row)

            # Feeling really bad about this...
            # But I need to wait for the file to complete
            # Better is to use a airflow sensor or don't use temp file..
            # or maybe XCOM to move data?
            # ....
            time.sleep(5)

            formatted_sql = DataToPostgresOperator.copy_csv_sql.format(
                self.table,
                f"/data/{file_name[1]}.csv",
                self.delimiter
            )
            postgres.run(formatted_sql, autocommit=True)
