import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from collections import Counter
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity


def check_missing_data(movies_df):
    missing_data = movies_df.isnull().sum()
    percent_missing = (missing_data / len(movies_df)) * 100
    missing_data_df = pd.DataFrame({'Kolumna': missing_data.index, 'Brakujące wartości': missing_data.values,
                                    'Procent brakujących': percent_missing.values})
    print(missing_data_df)


def display_IMDb_ratings_plot(movies_df):
    sns.set(style="whitegrid")
    plt.figure(figsize=(10, 6))
    sns.histplot(movies_df['IMDB_Rating'], bins=20, kde=True)
    plt.title('Rozkład ocen IMDb')
    plt.xlabel('Ocena IMDb')
    plt.ylabel('Liczba filmów')
    plt.show()


def display_meta_score_plot(movies_df):
    plt.figure(figsize=(10, 6))
    sns.histplot(movies_df['Meta_score'], bins=20, kde=True)
    plt.title('Rozkład Meta_score')
    plt.xlabel('Meta_score')
    plt.ylabel('Liczba filmów')
    plt.show()


def display_genres_plot(movies_df):
    genre_list = movies_df['Genre'].str.split(', ').sum()
    genre_counts = Counter(genre_list)
    genre_df = pd.DataFrame(genre_counts.items(), columns=['Genre', 'Count']).sort_values(by='Count', ascending=False)
    plt.figure(figsize=(12, 8))
    sns.barplot(x='Count', y='Genre', data=genre_df, palette='viridis', legend=False, hue='Genre')
    plt.title('Rozkład gatunków filmowych')
    plt.xlabel('Liczba filmów')
    plt.ylabel('Gatunek')
    plt.show()


def display_directors_plot(movies_df):
    director_counts = movies_df['Director'].value_counts().head(20)
    plt.figure(figsize=(12, 8))
    sns.barplot(x=director_counts.values, y=director_counts.index, palette='mako', hue=director_counts.index)
    plt.title('Top 20 reżyserów z największą liczbą filmów')
    plt.xlabel('Liczba filmów')
    plt.ylabel('Reżyser')
    plt.show()


def display_all_plots(movies_df, ):
    display_IMDb_ratings_plot(movies_df)
    display_meta_score_plot(movies_df)
    display_genres_plot(movies_df)
    display_directors_plot(movies_df)


def data_preprocessing(movies_df):
    movies_df['Certificate'].fillna('Nieznany', inplace=True)
    meta_score_mean = movies_df['Meta_score'].mean()
    movies_df['Meta_score'].fillna(meta_score_mean, inplace=True)
    movies_df.drop('Gross', axis=1, inplace=True)

    print(movies_df.isnull().sum())

    return movies_df


def get_cosine_similarities(movies_df):
    feature_columns = ['Genre', 'Director', 'IMDB_Rating', 'Meta_score']
    features_df = movies_df[feature_columns]
    one_hot_encoder = ColumnTransformer(
        transformers=[('cat', OneHotEncoder(sparse_output=False), ['Genre', 'Director'])], remainder='passthrough')
    transformed_features = one_hot_encoder.fit_transform(features_df)
    scaler = MinMaxScaler()
    transformed_features = scaler.fit_transform(transformed_features)
    transformed_features.shape
    cosine_similarities = cosine_similarity(transformed_features)

    return cosine_similarities
