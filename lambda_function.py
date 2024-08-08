lambda_function.py

import requests
import json
import config
import base64
import api_handler
import pandas
import push_to_s3_bucket


def lambda_handler(event, context):
  
    album_track_df = api_handler.new_release_url_generator(0, 50, "CA")
    push_to_s3_bucket.push_csv_to_s3(album_track_df)

    return {
      'statusCode': 200,
      'body': 'CSV and JSON uploaded successfully to S3!'
    }
