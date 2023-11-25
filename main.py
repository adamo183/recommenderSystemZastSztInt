import pandas as pd
from Functions.functions import check_missing_data
from Functions.functions import display_all_plots
from Functions.functions import data_preprocessing
from Functions.functions import get_cosine_similarities


file_path = 'imdb_top_1000.csv'
movies_df = pd.read_csv(file_path)
check_missing_data(movies_df)
movies_df = data_preprocessing(movies_df)
display_all_plots(movies_df)

movieToFindRecommendation = 'The Dark Knight'

# Wybór losowego filmu
random_movie = movies_df.loc[movies_df['Series_Title'] == movieToFindRecommendation]
selected_movie = random_movie.iloc[0]

selected_movie_info = {
    "Title": selected_movie['Series_Title'],
    "Director": selected_movie['Director'],
    "Genre": selected_movie['Genre'],
    "IMDB_Rating": selected_movie['IMDB_Rating'],
    "Meta_score": selected_movie['Meta_score']
}

print(selected_movie_info)

cosine_similarities = get_cosine_similarities(movies_df)


# Pobranie indeksu wybranego filmu
selected_movie_index = random_movie.index[0]

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

print(top_5_info)






