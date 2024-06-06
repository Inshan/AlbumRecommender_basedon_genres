import logging
from spotipy.oauth2 import SpotifyClientCredentials
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
from .forms import BandSearchForm
from sklearn.neighbors import NearestNeighbors
import joblib
import pandas as pd
from .spotify_client import get_spotify_client
from spotipy.exceptions import SpotifyException

# Initialize logging
logger = logging.getLogger(__name__)

# Load the model and vectorizer
knn_model = joblib.load("./recommender/knn_model.pkl")
vectorizer = joblib.load("./recommender/vectorizer.pkl")
artists_df = pd.read_csv("./data/artists_data.csv")

get_spotify_client()

def search_band(request):
    if request.method == "POST":
        form = BandSearchForm(request.POST)
        if form.is_valid():
            band_name = form.cleaned_data["band_name"]
            spotify = get_spotify_client()
            results = spotify.search(q="artist:" + band_name, type="artist")
            artists = results["artists"]["items"]
            if artists:
                artist_id = artists[0]["id"]
                return HttpResponseRedirect(reverse("band_albums", args=[artist_id]))
    else:
        form = BandSearchForm()
    return render(request, "search_band.html", {"form": form})

def band_albums(request, artist_id):
    form = BandSearchForm()
    spotify = get_spotify_client()
    artist = spotify.artist(artist_id)
    albums = spotify.artist_albums(artist_id, album_type="album")["items"]

    album_data = []
    for album in albums:
        album_data.append(
            {
                "id": album["id"],
                "name": album["name"],
                "cover": album["images"][0]["url"] if album["images"] else None,
                "genres": ", ".join(artist["genres"]),
            }
        )

    return render(
        request,
        "band_albums.html",
        {"band_name": artist["name"], "albums": album_data, "artist_id": artist_id, "form": form}
    )



def recommendations(request, artist_id):
    spotify = get_spotify_client()

    try:
        rec_artist_spotify = spotify.artist(artist_id)
    except SpotifyException as e:
        # Handle Spotify API errors
        if e.http_status == 400 and "invalid id" in str(e):
            # Invalid artist ID
            return HttpResponse("Invalid artist ID", status=400)
        else:
            # Other Spotify API errors
            return HttpResponse("An error occurred with the Spotify API", status=500)
    except Exception as e:
        # Handle other unexpected errors
        return HttpResponse("An unexpected error occurred", status=500)

    # Fetch artist information
    artist = spotify.artist(artist_id)
    genre = " ".join(artist.get("genres", []))
    artist_name = artist["name"]

    # Initialize recommendations list
    recommendations = []

    # Generate recommendations based on artist's genre
    if genre:
        X = vectorizer.transform([genre])
        distances, indices = knn_model.kneighbors(X, n_neighbors=30)
        valid_indices = indices[0][indices[0] < len(artists_df)]  # Filter out of bounds indices

        for idx in valid_indices:
            rec_artist = artists_df.iloc[idx]
            rec_artist_id = str(rec_artist["id"])  # Ensure rec_artist_id is a string
            try:
                rec_artist_spotify = spotify.artist(rec_artist_id)
                rec_genres = rec_artist_spotify.get("genres", [])
                if not rec_genres:  # Skip if no genres
                    continue

                rec_albums = spotify.artist_albums(rec_artist_id, album_type="album")["items"]
            except SpotifyException as e:
                print(f"Spotify API error for artist ID {rec_artist_id}: {e}")  # Debug print
                continue  # Skip this artist if there's an error
            except Exception as e:
                print(f"Unexpected error for artist ID {rec_artist_id}: {e}")  # Debug print
                continue  # Skip this artist if there's an error

            for album in rec_albums:
                recommendations.append(
                    {
                        "id": album["id"],
                        "name": album["name"],
                        "cover": album["images"][0]["url"] if album["images"] else None,
                        "artist_name": rec_artist_spotify["name"],  # Use artist's name instead of band_name
                        "genres": ", ".join(rec_genres),
                    }
                )
    
    # Limit to 15 recommendations
    recommendations = recommendations[:15]

    # Render recommendations template with artist and recommendations data
    return render(
        request,
        "recommendations.html",
        {"artist_name": artist_name, "recommendations": recommendations}
    )