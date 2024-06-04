import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from django.conf import settings

def get_spotify_client():
    auth_manager = SpotifyClientCredentials(
        client_id='',
        client_secret='')
    return spotipy.Spotify(auth_manager=auth_manager)
