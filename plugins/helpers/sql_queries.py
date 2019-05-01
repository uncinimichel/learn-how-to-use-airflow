class SqlQueries:
    songplay_table_insert = ("""
        INSERT INTO dwh.songplays
            SELECT
              md5(concat(events.sessionid, events.start_time)) playid,
              events.start_time,
              events.userid,
              events.level,
              songs.song_id,
              songs.artist_id,
              events.sessionid,
              events.location,
              events.useragent
            FROM (SELECT TIMESTAMP 'epoch' + ts / 1000 * interval '1 second' AS start_time, *
                  FROM dwh.raw_events
                  WHERE page = 'NextSong') events
                   LEFT JOIN dwh.raw_songs songs
                             ON events.song = songs.title
                               AND events.artist = songs.artist_name
                               AND events.length = songs.duration
            ON CONFLICT ON CONSTRAINT
            songplays_pkey DO NOTHING
            """)

    user_table_insert = ("""
        INSERT INTO dwh.users
        SELECT distinct userid, firstname, lastname, gender, level
        FROM dwh.raw_events
        WHERE page='NextSong'
        ON CONFLICT ON CONSTRAINT
        users_pkey DO NOTHING
    """)
    # I think you should delete it! but I guess depend on how big is the table... eiter I delete it or I create a delta everytime!
    song_table_insert = ("""
        INSERT INTO dwh.songs
        SELECT distinct song_id, title, artist_id, year, duration
        FROM dwh.raw_songs
        ON CONFLICT ON CONSTRAINT
        songs_pkey DO NOTHING
    """)

    artist_table_insert = ("""
        INSERT INTO dwh.artists
        SELECT distinct artist_id, artist_name, artist_location, artist_latitude, artist_longitude
        FROM dwh.raw_songs
        ON CONFLICT ON CONSTRAINT
        artistid_pkey DO NOTHING
    """)

    time_table_insert = ("""
        INSERT INTO dwh.time
        SELECT start_time, extract(hour from start_time), extract(day from start_time), extract(week from start_time), 
               extract(month from start_time), extract(year from start_time), extract(dow from start_time)
        FROM dwh.songplays        
        ON CONFLICT ON CONSTRAINT
        time_pkey DO NOTHING
    """)
