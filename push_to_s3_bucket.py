push_to_s3_bucket.py

import requests
import json
import boto3
import io
import pandas
from datetime import date

today = date.today().strftime("%Y-%m-%d")

def push_csv_to_s3(album_track_df):

    s3_client = boto3.client('s3')
    s3_bucket = "<bucket_name>"
    album_track_csv_key = f'spotify_new_releases_tracks_{today}.csv' #new_release
    
    # In-memory CSV buffer
    album_track_csv_buffer = io.StringIO()

    album_track_df.to_csv(album_track_csv_buffer, index=False)  # Don't include index row

    # Upload CSV to S3
    try:
        print("Pushing to S3")
        s3_client.put_object(Body=album_track_csv_buffer.getvalue(), Bucket=s3_bucket, Key=album_track_csv_key)    
        return True
        
    except Exception as e:
        return e