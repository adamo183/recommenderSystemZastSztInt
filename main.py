import pandas as pd
from Functions.functions import check_missing_data
from Functions.functions import display_all_plots
from Functions.functions import data_preprocessing
from Functions.functions import get_cosine_similarities

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


file_path = 'imdb_top_1000.csv'
movies_df = pd.read_csv(file_path)
check_missing_data(movies_df)
movies_df = data_preprocessing(movies_df)
display_all_plots(movies_df)


cosine_similarities = get_cosine_similarities(movies_df)



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






