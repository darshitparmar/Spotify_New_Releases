api_handler.py

import requests
import json
import config
import base64
from file_generator import generate_csv_file
from datetime import date
import boto3
import pandas

today = date.today().strftime("%Y-%m-%d")


def generate_bearer_token():
    
    client_id = config.client_id
    client_secret = config.client_secret

    credentials = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()

    auth_token_url = 'https://accounts.spotify.com/api/token'

    data = {
        "grant_type": "client_credentials",
    }

    headers = {
        "Authorization": f"Basic {credentials}",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    response = requests.post(auth_token_url, data=data, headers=headers)
    if response.status_code == 200:
        return response.json().get("access_token")
    raise ConnectionError

def album_chunk_size(lst, chunk_size):
    for i in range(0, len(lst), chunk_size):
        yield lst[i: i+chunk_size]


def get_spotify_album_tracks(album_ids,auth_bearer_token):
    base_url = 'https://api.spotify.com/v1/albums'
    chunk_size = 20

    final_response_dict = {}
    chunk_counter = 1000
    for chunk in album_chunk_size(album_ids, chunk_size):
        id_params = ','.join(chunk)

        album_tracks_api_url = f"{base_url}?ids={id_params}"

        headers = {"Authorization": f"Bearer {auth_bearer_token}"}
        album_tracks_response = requests.get(album_tracks_api_url, headers=headers)

        if album_tracks_response.status_code == 200:
            final_response_dict.update(album_tracks_response_handler(album_tracks_response, chunk_counter))
            chunk_counter += 1000
        else:
            raise Exception

    return final_response_dict


def album_tracks_response_handler(album_tracks_response, counter):
    response = album_tracks_response.json()
    response_dict = {}

    for data in response['albums']:
        album_id = data['id']
        album_name = data['name']
        album_url = data['external_urls']['spotify']
        album_type = data['album_type']
        album_release_date = data['release_date']
        for tracks in data['tracks']['items']:
            track_id = tracks['id']
            track_name = tracks['name']
            track_url = tracks['external_urls']['spotify']
            track_number = tracks['track_number']
            track_duration = tracks['duration_ms']
            track_is_explicit = tracks['explicit']
            for artist in tracks['artists']:
                artist_id = artist['id']
                artist_name = artist['name']
                artist_type = artist['type']
                artist_url = artist['external_urls']['spotify']

                response_dict[counter] = {}
                response_dict[counter]['album_id'] = album_id
                response_dict[counter]['album_name'] = album_name
                response_dict[counter]['album_url'] = album_url
                response_dict[counter]['album_type'] = album_type
                response_dict[counter]['album_release_date'] = album_release_date
                response_dict[counter]['artist_id'] = artist_id
                response_dict[counter]['artist_name'] = artist_name
                response_dict[counter]['artist_type'] = artist_type
                response_dict[counter]['artist_url'] = artist_url
                response_dict[counter]['track_id'] = track_id
                response_dict[counter]['track_name'] = track_name
                response_dict[counter]['track_url'] = track_url
                response_dict[counter]['track_number'] = track_number
                response_dict[counter]['track_duration'] = track_duration
                response_dict[counter]['track_explicit'] = track_is_explicit
                response_dict[counter]['pull_date'] = today
                counter += 1

    return response_dict


def new_release_url_generator(offset, limit, available_markets):
    base_url = 'https://api.spotify.com/v1/browse/new-releases'
    new_release_url = f'{base_url}?offset={offset}&limit={limit}&available_markets={available_markets}'

    auth_bearer_token = generate_bearer_token()
    
    headers = {"Authorization": f"Bearer {auth_bearer_token}"}
    new_release_response = requests.get(new_release_url, headers=headers)

    if new_release_response.status_code == 200:
        return new_release_response_handler(new_release_response,auth_bearer_token)
    else:
        raise Exception


def new_release_response_handler(new_release_response, auth_bearer_token):
    new_release_dict = {}
    response = new_release_response.json()
    response_text = new_release_response.text

    all_album_ids = [item['id'] for item in response['albums']['items']]
    all_unique_album_ids = list(set(all_album_ids))

    album_tracks_dict = get_spotify_album_tracks(all_unique_album_ids, auth_bearer_token)    
    
    return generate_csv_file(album_tracks_dict)

