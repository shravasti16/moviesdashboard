import streamlit as st
import pandas as pd

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Movie Intelligence Hub", layout="wide")

# ---------------- LOAD DATA ----------------
@st.cache_data
def load_data():
    new_df = pd.read_csv("clean_tmdb_5000_movies.csv")
    new_df['year'] = pd.to_numeric(new_df['year'], errors='coerce')
    new_df.dropna(inplace=True)
    return new_df

new_df = load_data()

# ---------------- CUSTOM UI ----------------
st.markdown("""
<style>
.main {
    background-color: #0b1220;
}
h1 {
    text-align: center;
    color: #60a5fa;
}
.card {
    background: #111827;
    padding: 20px;
    border-radius: 10px;
    text-align: center;
}
.metric {
    font-size: 26px;
    font-weight: bold;
    color: #34d399;
}
.label {
    color: #9ca3af;
}
</style>
""", unsafe_allow_html=True)

# ---------------- TITLE ----------------
st.markdown("<h1>🎬 Movie Intelligence Hub</h1>", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
st.sidebar.header("🎛 Filters")

year_range = st.sidebar.slider(
    "Select Year Range",
    int(new_df['year'].min()),
    int(new_df['year'].max()),
    (2000, 2015)
)

rating = st.sidebar.slider(
    "Minimum Rating",
    float(new_df['vote_average'].min()),
    float(new_df['vote_average'].max()),
    5.0
)

search = st.sidebar.text_input("🔍 Search Movie")

mood = st.sidebar.selectbox(
    "Select Mood",
    ["All", "Happy", "Sad", "Thriller", "Romantic"]
)

# ---------------- MOOD LOGIC ----------------
mood_dict = {
    "Happy": ["Comedy", "Family"],
    "Sad": ["Drama"],
    "Thriller": ["Thriller", "Crime"],
    "Romantic": ["Romance"]
}

filtered_df = new_df.copy()

# Filters apply
filtered_df = filtered_df[
    (filtered_df['year'] >= year_range[0]) &
    (filtered_df['year'] <= year_range[1]) &
    (filtered_df['vote_average'] >= rating)
]

if mood != "All":
    filtered_df = filtered_df[
        filtered_df['genres'].apply(
            lambda x: any(g in x for g in mood_dict[mood])
        )
    ]

if search:
    filtered_df = filtered_df[
        filtered_df['title'].str.contains(search, case=False)
    ]

# ---------------- KPI ----------------
col1, col2, col3 = st.columns(3)

col1.markdown(f"<div class='card'><div class='metric'>{len(filtered_df)}</div><div class='label'>Movies Found</div></div>", unsafe_allow_html=True)
col2.markdown(f"<div class='card'><div class='metric'>{round(filtered_df['vote_average'].mean(),2)}</div><div class='label'>Avg Rating</div></div>", unsafe_allow_html=True)
col3.markdown(f"<div class='card'><div class='metric'>{round(filtered_df['popularity'].max(),2)}</div><div class='label'>Top Popularity</div></div>", unsafe_allow_html=True)

# ---------------- SMART SUGGESTION ----------------
st.subheader("🎯 Smart Picks")

top_movies = filtered_df.sort_values(by=['vote_average','popularity'], ascending=False).head(5)

for i, row in top_movies.iterrows():
    st.markdown(f"""
    <div class='card'>
        <h3>{row['title']}</h3>
        <p>⭐ Rating: {row['vote_average']}</p>
        <p>🔥 Popularity: {row['popularity']}</p>
        <p>🎭 Genre: {row['genres']}</p>
    </div>
    """, unsafe_allow_html=True)

st.info("💡 Recommendations based on rating + popularity + mood filters")

# ---------------- ANALYTICS ----------------
st.subheader("📊 Insights")

col4, col5 = st.columns(2)

with col4:
    st.write("Movies per Year")
    st.line_chart(filtered_df['year'].value_counts().sort_index())

with col5:
    st.write("Ratings Distribution")
    st.bar_chart(filtered_df['vote_average'])

# ---------------- TABLE ----------------
st.subheader("📋 Explore Data")

st.dataframe(filtered_df, use_container_width=True)

# ---------------- FOOTER ----------------
st.markdown("---")
st.markdown("🚀 Built with Streamlit | No ML | Smart Logic Based System")