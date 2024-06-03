import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from django.conf import settings

def get_spotify_client():
    auth_manager = SpotifyClientCredentials(
        client_id='140259c128a34245b6e8be78e47aadf2',
        client_secret='7ed5430949f24d7ca4fc340e6748630b')
    return spotipy.Spotify(auth_manager=auth_manager)
