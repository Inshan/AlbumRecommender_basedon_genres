import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import json

SPOTIPY_CLIENT_ID = '140259c128a34245b6e8be78e47aadf2'
SPOTIPY_CLIENT_SECRET = '6d5414ddba994e6191bdf59e48fab5ea'

auth_manager = SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET)
sp = spotipy.Spotify(auth_manager=auth_manager)

def get_artists_data():
    artists = []
    for i in range(0, 1000, 50):
        results = sp.search(q='year:2020', type='artist', limit=50, offset=i)
        for artist in results['artists']['items']:
            artists.append({
                'id': artist['id'],
                'name': artist['name'],
                'genres': artist['genres']
            })
    return artists

artists_data = get_artists_data()

with open('artists_data.csv', 'w') as f:
    json.dump(artists_data, f)
