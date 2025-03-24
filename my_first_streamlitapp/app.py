import streamlit as st
import pandas as pd
import plotly.express as px
import os
import requests
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page Configuration
st.set_page_config(
    page_title="IMDB Movies Analysis",
    page_icon="🎬",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .stTitle { color: #1E3D59; font-weight: 800; }
    .stHeader { color: #2c3e50; font-weight: 600; }
    .stSubheader { color: #34495e; font-weight: 500; }
    .stButton>button { background-color: #1E3D59; color: white; border-radius: 5px; }
    .stButton>button:hover { background-color: #2c5282; transform: translateY(-2px); }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False

# Load and process data
@st.cache_data
def load_data():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, "IMDB_Movie_Data.csv")
    df = pd.read_csv(file_path)
    df['Revenue (Millions)'] = pd.to_numeric(df['Revenue (Millions)'], errors='coerce')
    return df

# Sidebar Navigation
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/movie-projector.png")
    st.title("Navigation")
    
    page = st.radio("📋 Go to", ["📊 Dataset Overview", "🔍 Movie Analysis", 
                                "📝 Genre Statistics", "🎬 Movie Recommendations", 
                                "🤖 AI Movie Chat"])
    
    # API key input for AI Chat
    if page == "🤖 AI Movie Chat":
        api_key = st.text_input("Enter API Key:", type="password")
        if api_key:
            st.session_state['api_key'] = api_key
            st.success("✅ API Key set successfully!")

# Load data
df = load_data()

# Main content based on selected page
if page == "📊 Dataset Overview":
    # Your existing Dataset Overview code...
    pass

elif page == "🔍 Movie Analysis":
    # Your existing Movie Analysis code...
    pass

elif page == "📝 Genre Statistics":
    # Your existing Genre Statistics code...
    pass

elif page == "🎬 Movie Recommendations":
    # Your existing Movie Recommendations code...
    pass

elif page == "🤖 AI Movie Chat":
    st.header("🤖 AI Movie Assistant")
    
    if not st.session_state.get('api_key'):
        st.warning("⚠️ Please enter your API key in the sidebar to use this feature.")
    else:
        user_input = st.text_input("Ask me anything about movies:", 
                                  placeholder="e.g., Suggest me a good sci-fi movie from this dataset")
        
        if st.button("Ask AI", key="ask_ai_button"):
            with st.spinner("🧠 Thinking..."):
                try:
                    url = "https://api.openai.com/v1/chat/completions"
                    headers = {
                        "Authorization": f"Bearer {st.session_state['api_key']}",
                        "Content-Type": "application/json"
                    }
                    
                    movie_context = df[['Title', 'Genre', 'Rating']].head(10).to_string()
                    data = {
                        "model": "gpt-3.5-turbo",
                        "messages": [
                            {"role": "system", "content": f"You are a movie expert. Context: {movie_context}"},
                            {"role": "user", "content": user_input}
                        ]
                    }
                    
                    response = requests.post(url, headers=headers, json=data)
                    response.raise_for_status()
                    response_data = response.json()
                    
                    st.markdown("""<div style='background-color: #f0f7fb; padding: 15px; border-radius: 10px; 
                                border-left: 5px solid #1E3D59;'>""", unsafe_allow_html=True)
                    st.markdown(response_data['choices'][0]['message']['content'])
                    st.markdown("</div>", unsafe_allow_html=True)
                    
                except Exception as e:
                    st.error(f"⚠️ An error occurred: {str(e)}")
                    st.info("💡 Tip: Make sure your API key is correct and has sufficient credits.")

# Footer
st.markdown("---")
st.markdown("Built with ❤️ using Streamlit")
