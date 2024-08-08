-- Table: public.daily_staging_table

CREATE TABLE IF NOT EXISTS daily_staging_table
(
    album_id varchar(255)  NOT NULL,
    album_name varchar(255) ,
    album_type varchar(255) ,
    album_url varchar(255) ,
    album_release_date date,
    artist_id varchar(255)  NOT NULL,
    artist_name varchar(255) ,
    artist_url varchar(255) ,
    track_id varchar(255)  NOT NULL,
    track_url varchar(255) ,
    track_number smallint,
    track_duration numeric,
    track_name varchar(255) ,
    track_explicit_flag boolean,
    pull_date date,
    artist_type varchar  NOT NULL
)


-- Table: public.artists

CREATE TABLE IF NOT EXISTS artists
(
    artist_id varchar(255)  NOT NULL,
    artist_name varchar(255)  NOT NULL,
    artist_url varchar(255) ,
    effective_start_date date NOT NULL,
    effective_end_date date,
    active_flag boolean NOT NULL,
    CONSTRAINT artists_pkey PRIMARY KEY (artist_id)
	
	
-- Table: public.albums

CREATE TABLE IF NOT EXISTS albums
(
    album_id varchar(255)  NOT NULL,
    album_name varchar(255) ,
    album_type varchar(255) ,
    album_url varchar(255)  NOT NULL,
    album_release_date date,
    artist_id varchar(255)  NOT NULL,
    effective_start_date date NOT NULL,
    effective_end_date date,
    active_flag boolean NOT NULL,
    CONSTRAINT album_pkey PRIMARY KEY (album_id, artist_id),
    CONSTRAINT fk_artist FOREIGN KEY (artist_id)
        REFERENCES public.artists (artist_id)
)


-- Table: public.album_tracks

CREATE TABLE IF NOT EXISTS album_tracks
(
    track_id varchar(255)  NOT NULL,
    track_name varchar(255) ,
    track_url varchar(255) ,
    track_number smallint,
    track_duration numeric,
    track_explicit_flag boolean,
    album_id varchar(255)  NOT NULL,
    artist_id varchar(255)  NOT NULL,
    effective_start_date date NOT NULL,
    effective_end_date date,
    active_flag boolean NOT NULL,
    CONSTRAINT album_tracks_pkey PRIMARY KEY (track_id, album_id, artist_id, effective_start_date),
    CONSTRAINT fk_album FOREIGN KEY (album_id, artist_id)
        REFERENCES public.albums (album_id, artist_id) 
    CONSTRAINT fk_artist FOREIGN KEY (artist_id)
        REFERENCES public.artists (artist_id) 
)

