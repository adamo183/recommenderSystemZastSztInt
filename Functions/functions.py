import matplotlib.pyplot as plt
import seaborn as sns

def display_plot(movies_df, ):
    # Ustawienie stylu wykresów
    sns.set(style="whitegrid")
    # Rozkład ocen IMDb
    plt.figure(figsize=(10, 6))
    sns.histplot(movies_df['IMDB_Rating'], bins=20, kde=True)
    plt.title('Rozkład ocen IMDb')
    plt.xlabel('Ocena IMDb')
    plt.ylabel('Liczba filmów')
    plt.show()
    # Rozkład Meta_score
    plt.figure(figsize=(10, 6))
    sns.histplot(movies_df['Meta_score'], bins=20, kde=True)
    plt.title('Rozkład Meta_score')
    plt.xlabel('Meta_score')
    plt.ylabel('Liczba filmów')
    plt.show()
    # Przygotowanie danych gatunków
    genre_list = movies_df['Genre'].str.split(', ').sum()
    genre_counts = Counter(genre_list)
    # Tworzenie DataFrame dla gatunków
    genre_df = pd.DataFrame(genre_counts.items(), columns=['Genre', 'Count']).sort_values(by='Count', ascending=False)
    # Wykres rozkładu gatunków
    plt.figure(figsize=(12, 8))
    sns.barplot(x='Count', y='Genre', data=genre_df, palette='viridis', legend=False, hue='Genre')
    plt.title('Rozkład gatunków filmowych')
    plt.xlabel('Liczba filmów')
    plt.ylabel('Gatunek')
    plt.show()
    # Przygotowanie danych reżyserów
    director_counts = movies_df['Director'].value_counts().head(20)  # Top 20 reżyserów
    # Wykres dla reżyserów
    plt.figure(figsize=(12, 8))
    sns.barplot(x=director_counts.values, y=director_counts.index, palette='mako', hue=director_counts.index)
    plt.title('Top 20 reżyserów z największą liczbą filmów')
    plt.xlabel('Liczba filmów')
    plt.ylabel('Reżyser')
    plt.show()
