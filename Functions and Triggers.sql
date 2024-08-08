-- 1.

CREATE OR REPLACE FUNCTION handle_new_artists()
RETURNS TRIGGER AS $$
BEGIN
    -- Insert new or changed records
    INSERT INTO artists (artist_id, artist_name, artist_url, effective_start_date, effective_end_date, active_flag)
    SELECT d.artist_id, d.artist_name, d.artist_url, CURRENT_DATE, NULL, true
    FROM daily_staging_table d
    LEFT JOIN artists a
    ON d.artist_id = a.artist_id AND a.active_flag = true
    WHERE a.artist_id IS NULL;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER trigger_artists_handle_new_artists
AFTER INSERT ON daily_staging_table
FOR EACH STATEMENT
EXECUTE FUNCTION handle_new_artists();


-- 2.
CREATE OR REPLACE FUNCTION handle_new_albums()
RETURNS TRIGGER AS $$
BEGIN

    -- Insert new or changed records
    INSERT INTO albums (album_id, album_name, album_type, album_url, album_release_date, artist_id,effective_start_date, effective_end_date, active_flag)
    SELECT distinct d.album_id, d.album_name,d.album_type ,d.album_url, d.album_release_date, d.artist_id, CURRENT_DATE::date, NULL::date, true
    FROM daily_staging_table d
    LEFT JOIN albums a
    ON d.album_id = a.album_id AND d.artist_id = a.artist_id AND a.active_flag = true
    WHERE a.album_id IS NULL;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER trigger_albums_handle_new_albums
AFTER INSERT ON daily_staging_table
FOR EACH STATEMENT
EXECUTE FUNCTION handle_new_albums();


-- 3.
CREATE OR REPLACE FUNCTION handle_album_tracks_scd_type_2()
RETURNS TRIGGER AS $$
BEGIN

    -- Insert new or changed records
    INSERT INTO album_tracks (track_id, track_name, track_url, track_number, track_duration, track_explicit_flag, album_id, artist_id, effective_start_date, effective_end_date, active_flag)
    SELECT d.track_id, d.track_name, d.track_url, d.track_number, d.track_duration, d.track_explicit_flag, d.album_id, d.artist_id, CURRENT_DATE, NULL, true
    FROM daily_staging_table d
    LEFT JOIN album_tracks a
    ON d.track_id = a.track_id AND d.album_id = a.album_id AND d.artist_id = a.artist_id AND a.active_flag = true
    WHERE a.track_id IS NULL;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

ALTER TABLE album_tracks
ADD CONSTRAINT album_tracks_pkey PRIMARY KEY (track_id, album_id, artist_id, effective_start_date);

truncate table album_tracks;

CREATE OR REPLACE TRIGGER trigger_album_tracks_handle_scd_type_2
AFTER INSERT ON daily_staging_table
FOR EACH STATEMENT
EXECUTE FUNCTION handle_album_tracks_scd_type_2();