import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import os

<<<<<<< HEAD
SPOTIPY_CLIENT_ID = "2da61999a9624632b6efcc370ea3ce46"
SPOTIPY_CLIENT_SECRET = "6649cb64a9af48d19e343f21b5534c12"
=======
SPOTIPY_CLIENT_ID = ''
SPOTIPY_CLIENT_SECRET = ''
>>>>>>> d369fc8ec3d5f390df6c08c6595d52c2a28aa697

auth_manager = SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET)
sp = spotipy.Spotify(auth_manager=auth_manager)

def get_artists_data():
    artists = []
    unique_artist_ids = set()
    queries = ["year:2020", "year:2019", "year:2018", "year:2017", "year:2016", "year:2015", "pop", "rock", "jazz", "hip-hop", "classical"]

    for query in queries:
        # Get the total number of results for the query
        initial_results = sp.search(q=query, type="artist", limit=1)
        total_results = initial_results['artists']['total']
        
        # Retrieve results in batches of 50
        for i in range(0, total_results, 50):
            results = sp.search(q=query, type="artist", limit=50, offset=i)
            for artist in results["artists"]["items"]:
                if artist["id"] not in unique_artist_ids:
                    unique_artist_ids.add(artist["id"])
                    artists.append({
                        "id": artist["id"],
                        "name": artist["name"],
                        "genres": ", ".join(artist["genres"])  # Convert genres list to a comma-separated string
                    })
            
            # Stop if we've collected enough artists
            if len(artists) >= 5000:
                break
        if len(artists) >= 5000:
            break
    return artists

artists_data = get_artists_data()

# Convert list of dictionaries to a DataFrame
df = pd.DataFrame(artists_data)

# Ensure the directory exists
output_dir = 'data'
os.makedirs(output_dir, exist_ok=True)

# Save DataFrame to a CSV file in the 'data' directory
output_file_path = os.path.join(output_dir, 'artists_data.csv')
df.to_csv(output_file_path, index=False)

print("Data has been saved to", output_file_path)
