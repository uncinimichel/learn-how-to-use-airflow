DROP DATABASE IF EXISTS dwh;

CREATE SCHEMA dwh AUTHORIZATION "airflow";
GRANT ALL PRIVILEGES ON SCHEMA dwh TO "airflow";
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA dwh TO "airflow";

DROP TABLE IF EXISTS dwh.raw_events;
DROP TABLE IF EXISTS dwh.raw_songs;

DROP TABLE IF EXISTS dwh.songplays;
DROP TABLE IF EXISTS dwh.songs;
DROP TABLE IF EXISTS dwh."time";

CREATE TABLE dwh.raw_events
(
  artist        varchar(256),
  auth          varchar(256),
  firstname     varchar(256),
  gender        varchar(256),
  iteminsession int4,
  lastname      varchar(256),
  length        numeric(18,0),
  "level"       varchar(256),
  location      varchar(256),
  "method"      varchar(256),
  page          varchar(256),
  registration  numeric(18,0),
  sessionid     int4,
  song          varchar(256),
  status        int4,
  ts            int8,
  useragent     varchar(256),
  userid        int4
);

CREATE TABLE dwh.raw_songs
(
  num_songs        int4,
  artist_id        varchar(256),
  artist_latitude  numeric(18,0),
  artist_longitude numeric(18,0),
  artist_location  varchar(256),
  artist_name      varchar(256),
  song_id          varchar(256),
  title            varchar(256),
  duration         numeric(18,0),
  "year"           int4
);

CREATE TABLE dwh.artists
(
  artistid  varchar(256) NOT NULL,
  name      varchar(256),
  location  varchar(256),
  lattitude numeric(18,0),
  longitude numeric(18,0),
  CONSTRAINT artistid_pkey PRIMARY KEY (artistid)
);

CREATE TABLE dwh.songplays
(
  playid     varchar(32) NOT NULL,
  start_time timestamp   NOT NULL,
  userid     int4        NOT NULL,
  "level"    varchar(256),
  songid     varchar(256),
  artistid   varchar(256),
  sessionid  int4,
  location   varchar(256),
  user_agent varchar(256),
  CONSTRAINT songplays_pkey PRIMARY KEY (playid)
);

CREATE TABLE dwh.songs
(
  songid   varchar(256) NOT NULL,
  title    varchar(256),
  artistid varchar(256),
  "year"   int4,
  duration numeric(18,0),
  CONSTRAINT songs_pkey PRIMARY KEY (songid)
);

CREATE TABLE dwh."time"
(
  start_time timestamp NOT NULL,
  "hour"     int4,
  "day"      int4,
  week       int4,
  "month"    varchar(256),
  "year"     int4,
  weekday    varchar(256),
  CONSTRAINT time_pkey PRIMARY KEY (start_time)
);

CREATE TABLE dwh.users
(
  userid     int4 NOT NULL,
  first_name varchar(256),
  last_name  varchar(256),
  gender     varchar(256),
  "level"    varchar(256),
  CONSTRAINT users_pkey PRIMARY KEY (userid)
);