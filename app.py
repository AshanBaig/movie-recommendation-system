import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_poster(movie_id):
    response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=619a73a921e5d7a34972b990bb753004&language=en-US')
    data = response.json()
    if "poster_path" in data:
        return "https://image.tmdb.org/t/p/w500/" + data.get('poster_path', '')
    else:
        return "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAQMAAADCCAMAAAB6zFdcAAAANlBMVEXf39+goKDi4uKdnZ2np6e4uLjU1NSamprOzs7KysrExMTj4+PBwcHc3NyoqKiioqKwsLC0tLSjj0KtAAADSklEQVR4nO2b2WKqMBBAA0EjAkL//2fLIMuAigsXeh3OebAVQiWnM9kkrihcITih0HRvhzPqZ/Nb+6IuHA6P3riW27/XnR7KTI/oGxofvHfLo3PdBcM9uQnXgzeHYZcQBzgAAAAAAACAeZg34kDAAQAAaOgXcCDgAAcCDgCgg/YABwIOcCDgAAcCDnAg4AAHAg5wIOAABwIOAABAQ7+AAwEHOBBwgAMBBzgAAIAx9As4EFZ3EC9n7VtcnfywmG+P1TgJfiHh+NeVWEic+GghNhwsCILagTfhoPq8LdjCwdrtjTjwp+zTLiHzVhykH3dvMQ6sOIiuDorj2zhrDs7hXUpnzsHb44QkxsHFsIMy8sFH4akTiQO3hYO1uePA+0Ndq+Jc+nkNjYPIqINj21X+7MaBnzjoFbjsMiuhywUTc6aRA3/I+pNFeOYgtulA1Si77MpB3DtQ4+b4MJcMdh1E2kG+TwdejUj+kzjYfIzkU3WyVFUukwcODI4Tkz4Z4lSFgf85edMOnB4fdJ1jfNSVDmk2WX417CDyVZHVDYREgY6DOizCXhzUUyZf5edDOfqv+yqbrsNvNmf6gzhoqjyZL/mQumkgbDZf+CMHE8prlxmPuoadOWhSYRoIF+O5MCVcl55HgWBsHck9jYO2tB48b+ZgbV5cT6zaMcNRJYOh+cIrDvoBdKaSwZyDeMaB96EvrpJhPw588FU6tEpqaWknDuqhUi1AfxtZTxr81g42+871jgMfqtRNHrlSyWBovvDAQSMgu71gSAZjDtyNA58UdwQ43TMYcnB/zpQ8vCCftgdGHTxWoJJhMwdrczcX6kR4fEWfDKYdzEWBmjxadjCvoA6EVoK5dSQ1RnqioJdgbg0lzrvnlp8qaNJBClpz4E55yyufmEnps61ckNpcNyK8uBtBijXFbTn47HIbDhY9p2rneeX89DFWHNRzRMV4j0q43eaijwUb/cLifSw4sLCWVpXJQspvd8D+xu/g2/dP/gtwgAMBBzgQcIADAQc4EHCAAwEHOBBwgAMAABhDv4ADAQc4EHCAAwEHOACAAdoDHAg4wIGAAxwIOMCBgAMcAMAA7QEOBBzgQMABDgQcAAAAAADAI5gv4AAAen4BZVMuzK5mga8AAAAASUVORK5CYII="


movie_list=pd.DataFrame(pickle.load(open("movies.pkl","rb")))
similarity=pickle.load(open("similarity.pkl","rb"))
movie_name=movie_list.title.values
st.title("Movie Reccomendation System")
option = st.selectbox(
    "How would you like to be contacted?",
    (movie_name),
)


def recommended(movie):
    movie_index = movie_list[movie_list["title"] == movie].index[0]
    indexes = sorted(list(enumerate(similarity[movie_index])), reverse=True, key=lambda x: x[1])[1:6]
    l = []
    movie_poster=[]
    for i in indexes:
        movie_id=movie_list.iloc[i[0]]["movie_id"]

        movie_poster.append(fetch_poster(movie_id))
        l.append(movie_list.iloc[i[0]].title)
    return l,movie_poster


if st.button("Recommend"):
        recommended_movies,movie_poster=recommended(option)
        columns  = st.columns(5)
        for i in range(len(columns)):
            with columns[i]:
                st.text(recommended_movies[i])
                st.image(movie_poster[i])
