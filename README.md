# 🎬 CineMatch — Movie Recommendation System

An ML-powered movie recommendation system built with content-based filtering, 
SVD matrix factorization, and a hybrid ensemble model trained on 25M ratings.

---

🚀 Live Demo
> 🌐 [Live Demo](https://siac1719-movie-recommender-appapp-dvdlmp.streamlit.app)

---

 📌 Features
-  Content-based filtering using TF-IDF + cosine similarity
-  Collaborative filtering using SVD matrix factorization
-  Hybrid model with dynamic alpha weighting
-  Real movie posters via OMDB API
-  Trained on 25M ratings from 162,000 users
-  86% Precision@10 · RMSE 0.78

---

 🧠 ML Concepts Used
 Concept --> Where Used 

 TF-IDF Vectorization--> Content-based filtering 
 Cosine Similarity--> Finding similar movies 
 SVD Matrix Factorization--> Collaborative filtering 
 Sparse Matrices (scipy)--> Efficient rating matrix storage 
 Mean Centering--> Removing user rating bias 
 Hybrid Ensemble--> Combining both models 
 IMDB Weighted Rating--> Popularity-aware scoring 
 Precision@K & RMSE--> Model evaluation 

---

## 📁 Project Structure
movie-reccomender/                                                                                                      
├── app/                                                                                                              
│   └── app.py              # Streamlit web app                                                                         
├── data/                                                                                                               
│   ├── raw/                # Original datasets (not tracked)                                                           
│   └── processed/          # Cleaned & merged data                                                                     
├── models/                 # Saved model artifacts                                                                    
├── notebooks/                                                                                                         
│   ├── 01_eda.ipynb        # Exploratory data analysis                                                                
│   ├── 02_content_based.ipynb  # TF-IDF + cosine similarity                                                           
│   ├── 03_collaborative.ipynb  # SVD collaborative filtering                                                           
│   ├── 04_hybrid.ipynb     # Hybrid model                                                                              
│   └── 05_evaluation.ipynb # RMSE + Precision@K                                                                        
├── requirements.txt                                                                                                    
└── README.md                                                                                                           

---

## 📊 Datasets
| Dataset | Source | Size |
|---|---|---|
| TMDB 5000 Movies | Kaggle | 4,800 movies |
| MovieLens 25M | GroupLens | 25M ratings · 162K users |

---

## 🔧 How It Works

### Phase 1 — Data Processing
- Merged TMDB metadata with MovieLens ratings via TMDB/IMDb IDs
- Parsed JSON genre, keyword, cast, crew fields
- Achieved 95.9% match rate between datasets

### Phase 2 — Content-Based Filtering
- Built a "soup" string per movie combining genres, keywords, cast, director, overview
- Applied TF-IDF vectorization (10,000 features)
- Computed pairwise cosine similarity matrix (4800 × 4800)

### Phase 3 — Collaborative Filtering
- Built sparse user-item matrix (20,000 × 5,000) from 11M ratings
- Mean-centered ratings to remove user bias
- Applied SVD with k=50 latent factors using scipy.sparse.linalg.svds

### Phase 4 — Hybrid Model
- Combined content and collaborative scores with weighted ensemble
- Dynamic alpha: new users → content-heavy, active users → collab-heavy
- Added IMDB weighted rating formula for popularity awareness

### Phase 5 — Evaluation
RMSE:          0.7833
MAE:           0.5906
Precision@10:  86.0%
---

## 🛠️ Tech Stack
- **Python** — pandas, numpy, scikit-learn, scipy
- **ML** — TF-IDF, SVD, cosine similarity
- **Frontend** — Streamlit
- **API** — OMDB for movie posters
- **Data** — TMDB 5000, MovieLens 25M

---

## ⚙️ Run Locally

```bash
git clone https://github.com/siac1719/movie-recommender.git
cd movie-recommender
pip install -r requirements.txt
```

Download datasets:
- [TMDB 5000](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata) → `data/raw/`
- [MovieLens 25M](https://grouplens.org/datasets/movielens/25m/) → `data/raw/`

Run notebooks 01 → 05 in order to rebuild models, then:

```bash
streamlit run app/app.py
```

---

## 📈 Results
> 86% of recommended movies were ones users actually rated 4+ stars out of 5
> RMSE of 0.78 — comparable to production recommendation systems
