file_generator.py

import pandas as pd
from datetime import date
import boto3

today = date.today().strftime("%Y-%m-%d")

def df_generator(json_data):
    
    gen_df = pd.DataFrame(json_data)
    gen_df = gen_df.transpose()
    return gen_df
    

# def generate_csv_file(new_release_json_data,album_tracks_json_data):

def generate_csv_file(album_tracks_json_data):

    album_tracks_df = df_generator(album_tracks_json_data)
    return album_tracks_df



