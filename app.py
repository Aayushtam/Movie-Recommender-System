import pickle
import streamlit as st
import requests
import pymongo
def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8d52c778658975f70fd05d9b0bb72aa6&language=en-US".format(movie_id)
    data = requests.get(url, headers = {
    "Authorization": "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI4ZDUyYzc3ODY1ODk3NWY3MGZkMDVkOWIwYmI3MmFhNiIsIm5iZiI6MTczMjM0MzI0MS4wMjQ1MTI1LCJzdWIiOiI2NzQxNzIwOTFiY2IyYzA5MzgwNTlhZWMiLCJzY29wZXMiOlsiYXBpX3JlYWQiXSwidmVyc2lvbiI6MX0.ySujWWO9tETmlXKXq3b7XZoo9__ZmVYU1iP1nx9ew6I"
})
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500" + poster_path
    return full_path

def recommend(movie):
    """Recommends movies based on similarity."""
    movie = movie.strip().lower()  # Normalize title for case-insensitive matching
    
    # Find the index of the selected movie
    index = next((i for i, m in enumerate(movies) if m['title'].strip().lower() == movie), None)
    if index is None:
        st.error("Selected movie not found in the database!")
        return [], []

    # Sort distances and get recommendations
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:  # Top 5 recommendations (excluding the selected movie)
        movie_id = movies[i[0]]['id']  # Fetch `id` for poster
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies[i[0]]['title'])

    return recommended_movie_names, recommended_movie_posters



st.header('Movie Recommender System')
client = pymongo.MongoClient("mongodb://localhost:27017/")
# Database Name
db = client["movie_cleaned_data"]
 
# Collection Name
col = db["Movie-recommender-system"]
movies = list(col.find({}, {"id": 1, "title": 1, "_id": 0}))

similarity = pickle.load(open(r'C:\Users\acer\Desktop\movies-recommender-system\similarity.pkl','rb'))

movie_list = [movie['title'] for movie in movies]
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

if st.button('Show Recommendation'):
    recommended_movie_names,recommended_movie_posters = recommend(selected_movie)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommended_movie_names[0])
        st.image(recommended_movie_posters[0])
    with col2:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1])

    with col3:
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2])
    with col4:
        st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters[3])
    with col5:
        st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[4])




