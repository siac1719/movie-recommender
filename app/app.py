import streamlit as st
import pandas as pd
import numpy as np
import pickle
import ast
import requests
import os

st.set_page_config(
    page_title="CineMatch",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&display=swap');

html, body, [data-testid="stAppViewContainer"] {
    background: #0d0d14 !important;
    font-family: 'DM Sans', sans-serif !important;
    color: #e2e0d8 !important;
}
[data-testid="stAppViewContainer"] {
    background: radial-gradient(ellipse at top left, #1e0a3c 0%, #0d0d14 55%) !important;
}
[data-testid="stHeader"] { background: transparent !important; }
[data-testid="stDecoration"] { display: none !important; }

.hero { padding: 2.5rem 0 1.5rem 0; }
.hero-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 5.5rem;
    letter-spacing: 0.04em;
    line-height: 0.88;
    background: linear-gradient(135deg, #ffffff 0%, #c084fc 45%, #7c3aed 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.hero-sub {
    font-size: 1.52rem;
    font-weight: 300;
    color: #55556a;
    letter-spacing: 0.3em;
    text-transform: uppercase;
    margin-top: 0.5rem;
}
.divider {
    height: 1px;
    background: linear-gradient(90deg, rgba(124,58,237,0.4), transparent);
    margin: 1.5rem 0;
}
.label {
    font-size: 1.2rem;
    font-weight: 500;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    color: #c084fc;
    margin-bottom: 0.75rem;
}
.seed-wrap {
    background: rgba(124,58,237,0.07);
    border: 1px solid rgba(124,58,237,0.18);
    border-radius: 14px;
    padding: 1.25rem 1.5rem;
    margin-bottom: 1.5rem;
}
.seed-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.5rem;
    letter-spacing: 0.05em;
    color: #fff;
    line-height: 1;
}
.seed-genre {
    font-size: 1rem;
    color: #7c3aed;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin: 0.3rem 0 0.6rem;
}
.seed-overview {
    font-size: 1.5rem;
    color: #6b6b80;
    line-height: 1.65;
}
.results-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.1rem;
    letter-spacing: 0.2em;
    color: #55556a;
    margin-bottom: 1rem;
    margin-top: 0.5rem;
}
.card {
    background: rgba(255,255,255,0.025);
    border: 1px solid rgba(255,255,255,0.055);
    border-radius: 10px;
    overflow: hidden;
    height: 100%;
    transition: border-color 0.2s;
}
.card:hover { border-color: rgba(192,132,252,0.35); }
.card img {
    width: 100%;
    aspect-ratio: 2/3;
    object-fit: cover;
    display: block;
}
.card-no-poster {
    width: 100%;
    aspect-ratio: 2/3;
    background: linear-gradient(135deg, #1a0a2e, #0d0d14);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 2.5rem;
}
.card-body { padding: 0.7rem 0.75rem 0.85rem; }
.card-rank {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 2rem;
    color: rgba(192,132,252,0.3);
    line-height: 1;
    margin-bottom: 0.3rem;
}
.card-title {
    font-size: 1.5rem;
    font-weight: 500;
    color: #e2e0d8;
    line-height: 1.35;
    margin-bottom: 0.55rem;
    min-height: 2.6rem;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
}
.card-footer {
    display: flex;
    align-items: center;
    justify-content: space-between;
}
.badge {
    background: rgba(124,58,237,0.18);
    border: 1px solid rgba(124,58,237,0.3);
    color: #c084fc;
    font-size: 0.85rem;
    font-weight: 500;
    padding: 0.25rem 0.6rem;
    border-radius: 5px;
}
.card-genre {
    font-size: 0.9rem;
    color: #55556a;
}
/* streamlit widget overrides */
div[data-testid="stSelectbox"] > div > div {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.09) !important;
    border-radius: 9px !important;
}
div[data-testid="stSlider"] label { color: #6b6b80 !important; font-size: 0.78rem !important; }
div[data-testid="stButton"] > button {
    background: linear-gradient(135deg, #7c3aed 0%, #4f46e5 100%) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 9px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 500 !important;
    font-size: 0.88rem !important;
    letter-spacing: 0.06em !important;
    width: 100% !important;
    padding: 0.55rem 0 !important;
}
div[data-testid="stMetric"] {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(255,255,255,0.07) !important;
    border-radius: 9px !important;
    padding: 0.6rem 0.9rem !important;
}
div[data-testid="stMetricLabel"] { color: #55556a !important; font-size: 0.7rem !important; }
div[data-testid="stMetricValue"] { color: #e2e0d8 !important; font-size: 1.2rem !important; }
</style>
""", unsafe_allow_html=True)

OMDB_KEY = "8defdb15"
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

@st.cache_resource(show_spinner=False)
def load_models():
    movies = pd.read_csv(os.path.join(BASE, 'data/processed/movies_final.csv'))
    movies['genres'] = movies['genres'].apply(ast.literal_eval)
    movies['keywords'] = movies['keywords'].apply(ast.literal_eval)
    movies['top_cast'] = movies['top_cast'].apply(ast.literal_eval)

    with open(os.path.join(BASE, 'models/indices.pkl'), 'rb') as f:
        indices = pickle.load(f)
    with open(os.path.join(BASE, 'models/cosine_sim.pkl'), 'rb') as f:
        cosine_sim = pickle.load(f)

    links = pd.read_csv(os.path.join(BASE, 'data/processed/links_cleaned.csv'))

    return movies, indices, cosine_sim, links

@st.cache_data(show_spinner=False)
def get_poster(imdb_id):
    try:
        imdb_str = f"tt{str(int(imdb_id)).zfill(7)}"
        r = requests.get(
            f"http://www.omdbapi.com/?i={imdb_str}&apikey={OMDB_KEY}",
            timeout=3)
        data = r.json()
        p = data.get('Poster', '')
        return p if p and p != 'N/A' else None
    except:
        return None

def get_recommendations(movies, cosine_sim, indices, title, n=10):
    if title not in indices:
        return None
    idx = indices[title]
    sim_scores = sorted(list(enumerate(cosine_sim[idx])),
                        key=lambda x: x[1], reverse=True)[1:n+20]
    candidate_indices = [i[0] for i in sim_scores]
    candidate_scores = {i[0]: i[1] for i in sim_scores}
    candidates = movies.iloc[candidate_indices][
        ['title', 'id', 'genres', 'vote_average',
         'vote_count', 'weighted_score', 'overview']].copy()
    candidates['content_score'] = candidates.index.map(candidate_scores)
    cs = candidates['content_score']
    candidates['content_norm'] = (cs - cs.min()) / (cs.max() - cs.min() + 1e-9)
    candidates['final_score'] = (
        0.7 * candidates['content_norm'] +
        0.3 * candidates['weighted_score'] / candidates['weighted_score'].max()
    )
    return candidates.sort_values(
        'final_score', ascending=False).head(n).reset_index(drop=True)

def get_imdb_id(tmdb_id, links):
    row = links[links['tmdbId'] == tmdb_id]
    return row['imdbId'].values[0] if len(row) > 0 else None

# ── LOAD ──────────────────────────────────────────────────────
with st.spinner(""):
    movies, indices, cosine_sim, links = load_models()

# ── HERO ──────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <div class="hero-title">CineMatch</div>
  <div class="hero-sub">AI · Content-Based · Hybrid Recommendations</div>
</div>
<div class="divider"></div>
""", unsafe_allow_html=True)

# ── SEARCH BAR ────────────────────────────────────────────────
st.markdown('<div class="label">🎬 Pick a movie you love</div>',
            unsafe_allow_html=True)

col1, col2, col3 = st.columns([4, 1, 1])
with col1:
    all_titles = sorted(movies['title'].dropna().tolist())
    selected = st.selectbox(" ", all_titles, label_visibility="collapsed")
with col2:
    n_recs = st.slider(" ", 5, 15, 8, label_visibility="collapsed")
with col3:
    go = st.button("✦  Recommend")

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ── SEED MOVIE ────────────────────────────────────────────────
movie_row = movies[movies['title'] == selected]
if len(movie_row) > 0:
    m = movie_row.iloc[0]
    imdb_id = get_imdb_id(m['id'], links)
    poster = get_poster(imdb_id) if imdb_id else None
    genres_str = ', '.join(m['genres'][:3]) if isinstance(
        m['genres'], list) else ''

    pcol, infocol = st.columns([1, 5])
    with pcol:
        if poster:
            st.image(poster, width=150)
        else:
            st.markdown('<div style="width:110px;height:165px;background:#1a0a2e;'
                        'border-radius:8px;display:flex;align-items:center;'
                        'justify-content:center;font-size:2rem">🎬</div>',
                        unsafe_allow_html=True)
    with infocol:
        st.markdown(f"""
        <div class="seed-wrap">
            <div class="seed-title">{selected}</div>
            <div class="seed-genre">{genres_str}</div>
            <div class="seed-overview">{m['overview']}</div>
        </div>
        """, unsafe_allow_html=True)

    mc1, mc2 = st.columns(2)
    with mc1:
        st.metric("TMDB Score", f"{m['vote_average']}/10")
    with mc2:
        st.metric("Total Votes", f"{int(m['vote_count']):,}")

# ── RESULTS ───────────────────────────────────────────────────
if go:
    with st.spinner("Finding your next obsession..."):
        results = get_recommendations(
            movies, cosine_sim, indices, selected, n_recs)

    if results is None:
        st.error("Movie not found.")
    else:
        st.markdown(f"""
        <div class="divider"></div>
        <div class="results-title">
            BECAUSE YOU LIKED &nbsp;{selected.upper()}
        </div>""", unsafe_allow_html=True)

        # 4 cards per row
        cols_per_row = 4
        rows = [results.iloc[i:i+cols_per_row]
                for i in range(0, len(results), cols_per_row)]

        for row_df in rows:
            cols = st.columns(cols_per_row, gap="small")
            for col, (_, row) in zip(cols, row_df.iterrows()):
                imdb_id = get_imdb_id(row['id'], links)
                poster = get_poster(imdb_id) if imdb_id else None
                genres_d = ', '.join(row['genres'][:2]) if isinstance(
                    row['genres'], list) else ''
                rank = row.name + 1

                with col:
                    if poster:
                        st.image(poster, width=220)
                    else:
                        st.markdown(
                            '<div class="card-no-poster">🎬</div>',
                            unsafe_allow_html=True)
                    st.markdown(f"""
                    <div class="card-body">
                        <div class="card-rank">0{rank}</div>
                        <div class="card-title">{row['title']}</div>
                        <div class="card-footer">
                            <span class="badge">★ {row['vote_average']:.1f}</span>
                            <span class="card-genre">{genres_d}</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)