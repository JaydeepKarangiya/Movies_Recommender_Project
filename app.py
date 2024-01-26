import streamlit as st
import requests

import pickle

movies_df = pickle.load(open('movies.pkl', 'rb'))
movies_list = movies_df['title'].values

similarity = pickle.load(open('similarity.pkl', 'rb'))


def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommend(movie):
    movie_index = movies_df[movies_df['title'] == movie].index[0]
    distance = similarity[movie_index]
    movies = sorted(list(enumerate(distance)), reverse=True, key=lambda x: x[1])[1:6]

    recommend_movies = []
    recommended_movie_posters = []
    for i in movies:
        movie_id = movies_df.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommend_movies.append(movies_df.iloc[i[0]].title)

    return recommend_movies,recommended_movie_posters

# ui
st.title('Movies Recommender System')

selected_movie_name = st.selectbox('Select Movie', movies_list)

num_recommendations = 5

if st.button('Show Recommendation'):
    try:
        recommended_movie_names, recommended_movie_posters = recommend(selected_movie_name)

        cols = st.columns(num_recommendations)

        for i in range(num_recommendations):
            with cols[i]:
                
                st.image(recommended_movie_posters[i])
                st.markdown(f"<p style='font-weight: bold;'>{recommended_movie_names[i]}</p>", unsafe_allow_html=True)

    except Exception as e:
        st.error(f"An error occurred: {e}")

