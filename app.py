import streamlit as st
import pickle
import pandas as pd
import requests


def fetch_poster(movies_id):
    response = requests.get(
        'https://api.themoviedb.org/3/movie/{}?api_key=cda879d2e9040bcac488c971e930f653&language=en-US'.format(
            movies_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']


def recommend(movie):
    movie_index = movies_dataframe[movies_dataframe['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:5]

    recommended_movies = []
    recommended_movies_posters = []
    for j in movies_list:
        movies_id = movies_dataframe.iloc[j[0]].movie_id
        recommended_movies.append(movies_dataframe.iloc[j[0]].title)
        recommended_movies_posters.append(fetch_poster(movies_id))
    return recommended_movies, recommended_movies_posters


similarity = pickle.load(open('similarity.pkl', 'rb'))
movies_dictionary = pickle.load(open('movies_dictionary.pkl', 'rb'))
movies_dataframe = pd.DataFrame(movies_dictionary)

st.title('Movie Recommender System')
selected_movie = st.selectbox(
    'Select/Search a movie to know similar movies',
    movies_dataframe['title'].values)
if st.button('Find Similar Movies'):
    names, posters = recommend(selected_movie)
    col1, clo2, clo3, col4 = st.columns(4)
    with col1:
        st.text(names[0])
        st.image(posters[0])
    with clo2:
        st.text(names[1])
        st.image(posters[1])
    with clo3:
        st.text(names[2])
        st.image(posters[2])
    with col4:
        st.text(names[3])
        st.image(posters[3])
