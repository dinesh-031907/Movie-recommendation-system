import streamlit as st
import pickle 
import requests
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
movies = pickle.load(open(os.path.join(BASE_DIR, "movies_list.pkl"), 'rb'))
similarity = pickle.load(open(os.path.join(BASE_DIR, "similarity.pkl"), 'rb'))



def fetch_poster(movie_id):
     url = "https://api.themoviedb.org/3/movie/{}?api_key=46941b3d3478f6f196b3371d2b6641cd&language=en-US".format(movie_id)
     try:
         response = requests.get(url, timeout=10)
         response.raise_for_status()
         data = response.json()
         poster_path = data.get('poster_path')
         if poster_path:
             full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
             return full_path
         else:
             return "https://via.placeholder.com/500x750?text=No+Image"
     except Exception as e:
         print(f"Error fetching poster for movie_id {movie_id}: {e}")
         return "https://via.placeholder.com/500x750?text=No+Image"

movies_list=movies['title'].values

st.header("Movie Recommender System")


## Removed custom component code due to missing directory error

selectvalue=st.selectbox("Select movie from dropdown", movies_list)

def recommend(movie):
    index=movies[movies['title']==movie].index[0]
    distance = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda vector:vector[1])
    recommend_movie=[]
    recommend_poster=[]
    for i in distance[1:6]:
        movies_id=movies.iloc[i[0]].id
        recommend_movie.append(movies.iloc[i[0]].title)
        recommend_poster.append(fetch_poster(movies_id))
    return recommend_movie, recommend_poster



if st.button("Show Recommend"):
    movie_name, movie_poster = recommend(selectvalue)
    col1,col2,col3,col4,col5=st.columns(5)
    with col1:
        st.text(movie_name[0])
        st.image(movie_poster[0])
    with col2:
        st.text(movie_name[1])
        st.image(movie_poster[1])
    with col3:
        st.text(movie_name[2])
        st.image(movie_poster[2])
    with col4:
        st.text(movie_name[3])
        st.image(movie_poster[3])
    with col5:
        st.text(movie_name[4])
        st.image(movie_poster[4])
