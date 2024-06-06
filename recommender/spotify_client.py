import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from django.conf import settings

def get_spotify_client():
    auth_manager = SpotifyClientCredentials(
<<<<<<< HEAD
        client_id='2da61999a9624632b6efcc370ea3ce46',
        client_secret='6649cb64a9af48d19e343f21b5534c12')
=======
        client_id='',
        client_secret='')
>>>>>>> d369fc8ec3d5f390df6c08c6595d52c2a28aa697
    return spotipy.Spotify(auth_manager=auth_manager)
