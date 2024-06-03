import joblib
import pandas as pd
from django.conf import settings
from .forms import SongSearchForm
from django.shortcuts import render
from .spotify_client import get_spotify_client

# Load the model and vectorizer
knn_model = joblib.load('knn_model.pkl')
vectorizer = joblib.load('vectorizer.pkl')
artists_df = pd.read_csv('artists_data.csv')

def search_song(request):
    if request.method == 'POST':
        form = SongSearchForm(request.POST)
        if form.is_valid():
            song_name = form.cleaned_data['song_name']
            spotify = get_spotify_client()
            results = spotify.search(q='track:' + song_name, type='track')
            songs = results['tracks']['items']
            return render(request, 'song_search_results.html', {'songs': songs})
    else:
        form = SongSearchForm()
    return render(request, 'song_search.html', {'form': form})


def song_details(request, song_id):
    spotify = get_spotify_client()
    song = spotify.track(song_id)
    artists = [artist['name'] for artist in song['artists']]
    album_cover = song['album']['images'][0]['url'] if song['album']['images'] else None
    genre = ' '.join(song.get('genres', ['Unknown']))  # Use get method to handle missing genre information
    recommendations = []

    if genre:
        X = vectorizer.transform([genre])
        distances, indices = knn_model.kneighbors(X, n_neighbors=10)
        valid_indices = indices[0][indices[0] < len(artists_df)]  # Filter out of bounds indices
        for idx in valid_indices:
            rec_artist = artists_df.iloc[idx]
            rec_artist_id = rec_artist['id']
            rec_artist_albums = spotify.artist_albums(rec_artist_id, album_type='album')['items']
            for album in rec_artist_albums:
                rec_album_id = album['id']
                rec_genre = ' '.join(spotify.track(rec_album_id).get('genres', ['Unknown']))  # Use get method to handle missing genre information
                if rec_genre == genre:
                    recommendations.append({
                        'artist_name': rec_artist['name'],
                        'album_name': album['album_name'],
                        'album_id': rec_album_id,
                        'album_cover': album['images'][0]['url'] if album['images'] else None,
                        'genre': rec_genre
                    })

    return render(request, 'song_details.html', {
        'song': song,
        'artists': artists,
        'album_cover': album_cover,
        'genre': genre,
        'recommendations': recommendations
    })
