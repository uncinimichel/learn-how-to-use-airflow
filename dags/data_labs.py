from datetime import datetime

from airflow import DAG
from airflow.operators import DataToPostgresOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.postgres_operator import PostgresOperator
from airflow.operators.python_operator import PythonOperator
from helpers import SqlQueries

SONG_DATA_SET_CSV_URL = "https://s3.eu-west-2.amazonaws.com/com.datalab/song_data/song.csv"
EVENTS_CSV_URL = "https://s3.eu-west-2.amazonaws.com/com.datalab/log-data/2018-11-01-events.csv"

# Those args will be present to every tasks that you define
default_args = {
    'owner': 'data_labs',
    'start_date': datetime(2019, 1, 12),
}

dag = DAG('data_labs',
          default_args=default_args,
          description='Load and transform some data in POSTGRES with Airflow',
          schedule_interval="@once")

start = DummyOperator(
    task_id="start",
    dag=dag)

stop = DummyOperator(
    task_id="stop",
    dag=dag
)

create_data_songs_to_postgres = DataToPostgresOperator(
    task_id="create_data_songs_to_postgres",
    data_url=SONG_DATA_SET_CSV_URL,
    dag=dag,
    table="dwh.raw_songs",
    postgres_conn_id="stage_postgres",
    source_type="csv"
)

create_log_events_to_postgres = DataToPostgresOperator(
    task_id="create_log_events_to_postgres",
    data_url=EVENTS_CSV_URL,
    dag=dag,
    table="dwh.raw_events",
    postgres_conn_id="stage_postgres",
    source_type="csv"
)

create_fact_table_songplay = PostgresOperator(
    task_id="create_fact_table_songplay",
    dag=dag,
    postgres_conn_id="stage_postgres",
    sql=SqlQueries.songplay_table_insert
)

create_data_dimension_songs = PostgresOperator(
    task_id="create_data_dimension_songs",
    dag=dag,
    postgres_conn_id="stage_postgres",
    sql=SqlQueries.song_table_insert
)

create_data_dimension_artists = PostgresOperator(
    task_id="create_data_dimension_artists",
    dag=dag,
    postgres_conn_id="stage_postgres",
    sql=SqlQueries.artist_table_insert
)
create_data_dimension_time = PostgresOperator(
    task_id="create_data_dimension_time",
    dag=dag,
    postgres_conn_id="stage_postgres",
    sql=SqlQueries.time_table_insert
)
create_data_dimension_users = PostgresOperator(
    task_id="create_data_dimension_users",
    dag=dag,
    postgres_conn_id="stage_postgres",
    sql=SqlQueries.user_table_insert
)


# Do some cleaning!
def clean_year_zero_with_minus_1(*args, **kwargs):
    pass


def change_user_level_from_free_to_poor(*args, **kwargs):
    pass


# Now do some validation!!!
def check_greater_than_zero(*args, **kwargs):
    pass


def check_is_not_null(*args, **kwargs):
    pass


def check_is_all_song_id_in_songplays_are_in_songs(*args, **kwargs):
    pass


# Can you run a panda model?
def run_panda_model_against_users(*args, **kwargs):
    pass


check_there_is_some_artists_data = PythonOperator(
    task_id='check_there_is_some_artists_data',
    dag=dag,
    python_callable=check_greater_than_zero,
    provide_context=True
)

run_panda_model_against_users_task = PythonOperator(
    task_id='run_panda_model_against_users_task',
    dag=dag,
    python_callable=run_panda_model_against_users,
    provide_context=True
)

start >> create_data_songs_to_postgres
start >> create_log_events_to_postgres

create_data_songs_to_postgres >> create_fact_table_songplay
create_log_events_to_postgres >> create_fact_table_songplay

create_fact_table_songplay >> create_data_dimension_songs
create_fact_table_songplay >> create_data_dimension_artists
create_fact_table_songplay >> create_data_dimension_time
create_fact_table_songplay >> create_data_dimension_users

create_data_dimension_songs >> stop
create_data_dimension_time >> stop
create_data_dimension_users >> stop
create_data_dimension_users >> run_panda_model_against_users_task

create_data_dimension_artists >> check_there_is_some_artists_data
check_there_is_some_artists_data >> stop
run_panda_model_against_users_task >> stop
