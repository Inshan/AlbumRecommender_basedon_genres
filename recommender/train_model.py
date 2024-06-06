import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
import joblib

# Load the data from CSV
df = pd.read_csv('./data/artists_data.csv')

# Combine genres into a single string for each artist
df['genres_str'] = df['genres']

# Handle NaN values by replacing them with an empty string
df['genres_str'] = df['genres_str'].fillna('')

# Create a TF-IDF vectorizer
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(df['genres_str'])

# Train a k-NN model
knn = NearestNeighbors(n_neighbors=10, algorithm='auto').fit(X)

# Save the model and vectorizer
joblib.dump(knn, 'recommender/knn_model.pkl')
joblib.dump(vectorizer, 'recommender/vectorizer.pkl')
