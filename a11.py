import pickle
import streamlit as st
import requests

def fetch_poster(movie_id):
    api_key = "c5353608"  # Replace with your actual OMDB API key
    url = f"http://img.omdbapi.com/?i={movie_id}&apikey={api_key}"
    
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        poster_url = data.get('Poster')
        if poster_url and poster_url != 'N/A':
            return poster_url
        else:
            return "https://example.com/default_poster.jpg"  # Valid default poster URL
    else:
        return "https://example.com/default_poster.jpg"  # Valid default poster URL









def recommend(movie):
    if movie not in movies['title'].values:
        return [], []
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)
    return recommended_movie_names, recommended_movie_posters





st.header('Movie Recommender System')
movies = pickle.load(open('movie_list.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

movie_list = movies['title'].values
selected_movie = st.selectbox("Type or select a movie from the dropdown", movie_list)

if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
    cols = st.columns(5)
    for i, col in enumerate(cols):
        if i < len(recommended_movie_names):
            with col:
                st.text(recommended_movie_names[i])
                st.image(recommended_movie_posters[i])
