import pandas as pd
from collections import Counter
import random
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from Functions.functions import display_plot
from fastapi import FastAPI

app = FastAPI()

file_path = 'imdb_top_1000.csv'
movies_df = pd.read_csv(file_path)

# Sprawdzenie brakujących danych
missing_data = movies_df.isnull().sum()

# Procent brakujących danych w każdej kolumnie
percent_missing = (missing_data / len(movies_df)) * 100

missing_data_df = pd.DataFrame({'Kolumna': missing_data.index, 'Brakujące wartości': missing_data.values, 'Procent brakujących': percent_missing.values})
print(missing_data_df)

# Ustawienie brakujących wartości w 'Certificate' na 'Nieznany'
movies_df['Certificate'].fillna('Nieznany', inplace=True)

# Uzupełnienie brakujących wartości w 'Meta_score' przez średnią
meta_score_mean = movies_df['Meta_score'].mean()
movies_df['Meta_score'].fillna(meta_score_mean, inplace=True)

# Usunięcie kolumny 'Gross'
movies_df.drop('Gross', axis=1, inplace=True)

# Sprawdzenie, czy operacje zostały wykonane poprawnie
print(movies_df.isnull().sum()) # Powinno nie wykazywać brakujących danych

#display_plot(movies_df)


# Przygotowanie danych
feature_columns = ['Genre', 'Director', 'IMDB_Rating', 'Meta_score']

# Tworzenie DataFrame z wybranymi kolumnami
features_df = movies_df[feature_columns]

# Kodowanie "one-hot" dla kategorialnych danych ('Genre' i 'Director')
one_hot_encoder = ColumnTransformer(transformers=[('cat', OneHotEncoder(sparse_output=False), ['Genre', 'Director'])], remainder='passthrough')

# Transformacja danych
transformed_features = one_hot_encoder.fit_transform(features_df)

# Normalizacja ocen numerycznych ('IMDB_Rating' i 'Meta_score')
scaler = MinMaxScaler()
transformed_features = scaler.fit_transform(transformed_features)

# Sprawdzenie przekształconych danych
transformed_features.shape
# Obliczenie podobieństwa kosinusowego
cosine_similarities = cosine_similarity(transformed_features)


@app.get("/recommend/movie/name/{movie_name}")
def read_item(movie_name: str):
    choosen_movie = movies_df.loc[movies_df['Series_Title'] == movie_name]
    selected_movie = choosen_movie.iloc[0]
    selected_movie_index = choosen_movie.index[0]
    # Pobranie podobieństw dla wybranego filmu
    similarities = cosine_similarities[selected_movie_index]
    # Przekształcenie podobieństw w DataFrame
    similarity_df = pd.DataFrame({'index': range(len(similarities)), 'similarity': similarities})

    # Sortowanie filmów według podobieństwa (pomijając wybrany film)
    recommended_movies = similarity_df.sort_values(by='similarity', ascending=False)
    recommended_movies = recommended_movies[recommended_movies['index'] != selected_movie_index]

    # Wybór top 5 podobnych filmów
    top_5 = recommended_movies.head(5)

    # Wyszukanie tytułów i informacji o top 5 filmach
    top_5_info = movies_df.loc[top_5['index'], ['Series_Title', 'Director', 'Genre', 'IMDB_Rating', 'Meta_score']]
    top_5_info.reset_index(drop=True, inplace=True)
    return {"recomendation": top_5_info}

@app.get("/films")
def read_item():
    return movies_df['Series_Title'].to_json()






