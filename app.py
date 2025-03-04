import streamlit as st
import pickle
import pandas as pd
import requests

# OMDB api key for fetching posters....
OMDB_API_KEY = '28a23645'

# Custom CSS styling
st.markdown("""
    <style>
        .main {
            background: linear-gradient(45deg, #1a1a1a, #2a2a2a);
            color: #ffffff;
        }
        .stSelectbox div div div input {
            color: #4a4a4a !important;
        }
        .stButton button {
            background-color: #e50914;
            color: white;
            border-radius: 5px;
            padding: 10px 24px;
            border: none;
            font-weight: bold;
            transition: all 0.3s ease;
        }
        .stButton button:hover {
            background-color: #ff0000;
            transform: scale(1.05);
        }
        .movie-card {
            background: #2a2a2a;
            border-radius: 10px;
            padding: 20px;
            margin: 15px auto;
            width: 95%;
            transition: transform 0.3s ease;
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        }
        .movie-card img {
            width: 100%;
            height: 400px;
            object-fit: cover;
            border-radius: 8px;
            margin-bottom: 15px;
        }
        .movie-card h4 {
            font-size: 1.2rem;
            margin: 15px 0;
            min-height: 3em;
        }
        .movie-card p {
            margin: 8px 0;
            font-size: 1rem;
            color: #cccccc;
        }
        .stSelectbox > div > div {
            width: 90% !important;
            max-width: 800px !important;
            margin: 0 auto;
        }
        .stSelectbox input {
            font-size: 1.1rem !important;
            padding: 12px !important;
        }
        /* Responsive adjustments */
        @media (max-width: 1200px) {
            .movie-card img {
                height: 350px;
            }
        }
        @media (max-width: 992px) {
            .movie-card img {
                height: 300px;
            }
        }
    </style>
""", unsafe_allow_html=True)

def fetch_movie_details(movie_title):
    url = f"http://www.omdbapi.com/?t={movie_title}&apikey={OMDB_API_KEY}"
    data = requests.get(url).json()
    return {
        'poster': data.get('Poster'),
        'year': data.get('Year'),
        'rating': data.get('imdbRating'),
        'genre': data.get('Genre'),
        'runtime': data.get('Runtime')
    }

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_details = []

    for i in movies_list:
        movie_title = movies.iloc[i[0]].title
        details = fetch_movie_details(movie_title)
        recommended_movies.append(movie_title)
        recommended_details.append(details)

    return recommended_movies, recommended_details

movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))

# App layout
st.markdown('<h1 class="title">🎬 CineMatch Pro</h1>', unsafe_allow_html=True)
st.markdown("---")

selected_movie_name = st.selectbox(
    '**Discover Your Next Favorite Movie**\n\nStart typing or select from the dropdown below:',
    movies['title'].values,
    index=0,
    help="Select a movie you enjoy to get personalized recommendations"
)

st.markdown("---")

if st.button('🎯 Get Recommendations'):
    with st.spinner('🔍 Searching the cinematic universe...'):
        names, details = recommend(selected_movie_name)
        
        st.markdown(f'### 🍿 Top Recommendations for "{selected_movie_name}"')
        cols = st.columns(3)  # Changed from 5 to 3 columns for wider cards
        
        for col, name, detail in zip(cols, names, details):
            with col:
                card = f"""
                <div class="movie-card">
                    <div style="text-align: center;">
                        {f'<img src="{detail["poster"]}" style="margin-bottom: 15px;">' 
                         if detail['poster'] != 'N/A' else 
                         '<div style="height: 400px; background: #3a3a3a; border-radius: 10px; display: flex; align-items: center; justify-content: center; margin-bottom: 15px;">📽️ Poster Unavailable</div>'}
                        <h4 style="margin: 15px 0; color: #e50914; line-height: 1.3;">{name}</h4>
                        <p>⭐ {detail['rating'] or 'N/A'}</p>
                        <p>📅 {detail['year'] or 'N/A'}</p>
                        <p>⌛ {detail['runtime'] or 'N/A'}</p>
                        <p>🎭 {detail['genre'] or 'N/A'}</p>
                    </div>
                </div>
                """
                st.markdown(card, unsafe_allow_html=True)

        st.balloons()