# Airflow at the Data Labs

## Why use airflow?
Because I want programmatically schedule and monitor workflows.
The rich user interface makes it easy to visualize pipelines running in production, monitor progress, and troubleshoot issues when needed. When workflows are defined as code, they become more maintainable, versionable, testable, and collaborative.

## How it works?
Define workflow as directed acyclic graphs (DAGs) of tasks written in Python.
Example of DAG workflows :



## Keywords

### Operators

Describe a single task in a workflow. There are many operators already in Airflow but it is very easy to create your own one.
- BashOperator - executes a bash command
- PythonOperator - calls an arbitrary Python function
- EmailOperator - sends an email
- SimpleHttpOperator - sends an HTTP request
- MySqlOperator, SqliteOperator, PostgresOperator, MsSqlOperator, OracleOperator,JdbcOperator, etc. - executes a SQL command
- Sensor - waits for a certain time, file, database row, S3 key, etc…


### Connection 

Store connections details with resources. For example I can have two connections for my postgres. One that point to the stage env and the other that point to prod. 

### XComs 

Move data from tasks

### Hooks
Interfaces to external platforms and Database like Hive, S3, Postgres, HDFS… 
Hooks are also very useful on their own to use in a PythonOperator. 
For example I can use the AwsHook to get my was credentials and then the PostgresOperator to run some SQL  

### Secrets
You can store secrets in airflow and it will encrypt that.

### Variable, SubDAGs, Branching, Sla
...

## What this Lab is about?

Our client did a website where you can listen to music. This website use a song dataset and it generate lots of log events.
Our tasks is to define a pipeline of tasks where we grab the dataset and the log events and we move it to the Data Warehouse, so they can be analysed.  

Some examples of tasks to :
- Download the logs and the data set
- Create the tables in the Data warehouse to store the dataset and the logs (sql is already provided)
- Run Data quality check
- Clean the data
- Run some data model (why not :)
- Publish the results somewhere

This is an example of how the pipeline will look like:

![Pipeline](/pipeline.png)


## A bit about the type of Data/Logs:

1. [SONG_DATA_SET](https://s3.eu-west-2.amazonaws.com/com.datalab/song_data/song.csv): Is a subset of real data from the Million Song Dataset.

```json
{
  "num_songs": 1,
  "artist_id": "ARD7TVE1187B99BFB1",
  "artist_latitude": null,
  "artist_longitude": null,
  "artist_location": "California - LA",
  "artist_name": "Casual",
  "song_id": "SOMZWCG12A8C13C480",
  "title": "I Didn't Mean To",
  "duration": 218.93179,
  "year": 0
}
```
2. [EVENTS_CSV_URL](https://s3.eu-west-2.amazonaws.com/com.datalab/log-data/2018-11-01-events.csv): JSON format logs generated by an event simulator that generate fake user interactions with a hypothetical song streaming website

```json
{
  "artist": null,
  "auth": "Logged In",
  "firstName": "Theodore",
  "gender": "M",
  "itemInSession": 0,
  "lastName": "Smith",
  "length": null,
  "level": "free",
  "location": "Houston-The Woodlands-Sugar Land, TX",
  "method": "GET",
  "page": "Home",
  "registration": 1540306145796.0,
  "sessionId": 154,
  "song": null,
  "status": 200,
  "ts": 1541290555796,
  "userAgent": "Mozilla\/5.0 (Windows NT 6.1; WOW64; rv:31.0) Gecko\/20100101 Firefox\/31.0",
  "userId": "52"
}
```

The data in the DWS is modelled as a start schema:
- `songplays` is the big fact table records in log data associated with song plays i.e. records with page NextSong
    - songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location, user_agent

Some other tables

- `users` - users in the app
    - user_id, first_name, last_name, gender, level
- `songs` - songs in music database
    - song_id, title, artist_id, year, duration
- `artists` - artists in music database
    - artist_id, name, location, lattitude, longitude
- `time` - timestamps of records in songplays broken down into specific units
    - start_time, hour, day, week, month, year, weekday

### Some folder/files in this repo

- `init_db.sql`
init the postgres database with our star schema.  

- `docker-compose.yml`
start postgres and airflow

- `dags`
contains our DAG

- `plugins/helpers`
some helpers function that airflow pass to the dags 

- `plugins/operators`
Custom operators that you can define. I create `data_to_postgres.py` which download the data from a s3 bucket and pass it to postgres.
- `data`
Contains some data. It is not used because the data is coming from a s3 bucket but feel free to use it instead!!!

### Getting Started

To get started with this Lab demonstration follow the steps outlined below:

1. Clone the repository

- `git clone https://github.com/uncinimichel/learn-how-to-use-airflow.git`

2. Modify the docker-componse.yml file. Remove the last line under services > webserver > environment:

- `AIRFLOW_CONN_STAGE_POSTGRES=postgres://airflow:airflow@localhost:5432/airflow`

3. Start the docker instance:

- `docker-compose up`

4. Navigate to:

- `http://localhost:8080`

5. From the navigation bar at the top of the web interface, select `admin` then `connections`

6. From the tabs under connections select `Create`

7. Using the information below populate the create connection form:

   - Conn Id: `stage_postgres`
   - Conn Type: `Postgres`
   - Host: `postgres`
   - Schema: `airflow`
   - Login: `airflow`
   - Password: `airflow`
   - Port: `5432`
   - Extra: leave this blank

8. Click save  

### TODO

- Change the tasks scheduler
- Run only failed tasks
- Automatically re-run tasks
- Better Data Partition. For example can append a delta to the big table instead of build it every time from scratch?
- Get a email notification when a task fail
- Can you implement some SLA
- Can you add some trigger rules for some tasks?
- Can you download the dataset and the logs with a unix script instead of using python?
- For example run a task only when all the upstream fail
- Publish the results of panda somewhere else!!
- Run a ML model as part of the pipeline
- Can you trigger a Spark job and waiting for result?
- Implement a sensor
- Can you use s3 and redshift instead?
- Use XComs to exchange data between tasks

## LINKS

- Airflow list of operators
https://github.com/apache/airflow/tree/master/airflow/operators
- Airflow Concepts:
http://airflow.apache.org/concepts.html
- Docker image 
https://github.com/puckel/docker-airflow