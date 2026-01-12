# &#127916; MovieVerse - AI-Powered Movie Recommendation System with conversational AI

MovieVerse is an end-to-end AI-Powered movie recommendation platform that combines
**collaborative filtering**,**content-based fitering**, and a **conversational AI assistant**
to provide personalised and explainable movie recommendations.

This project is fully deployed using **Hugging Face Spaces**,
with models and dataset hosted on **Hugging Face Hub**.

---
## 👀; App Link

`https://huggingface.co/spaces/Anuj-Verma/MovieVerse`


## Overview 

Traditional recommender systems suggest items but fail to explain *why*
MovieVerse bridges this gap by integrating a **Large Language Model(LLM)** that interacts with users, understands preferences, and explains recommendations naturally.


Users can:
- Get movie recommendations
- Ask natural language questions about movies
- Receive AI-generated explanations for recommendations

---


## &#10024; Key Features

- Personalised movie recommendations
- collaborative filtering (user-user & item-item similarity)
- Content-Based Filtering using TF-IDF
- Conversatioal AI powered by Hugging Face hosted LLMs
- RAG-style retrieval for movie context
- Fully deployed on Hugging Face Spaces

---

## Recommendation Approaches

### Collaborative Filtering
- User similarity based on ratings
- item similarity using cosine similarity
- Precomputed similarity matrices for fast inference

### Content-Based Filtering 
- TF-IDF vectorization in movie metadata
- Similarity search over movie descriptions
- Useful for cold-start scenarios

---


## AI Chat Assistant (LLM)
- Model: `mistralai/Mistral-7B-instruct-v0.2`
- Hosted via Hugging Face inference API
- Chat-based completions (not plain text generation)
- Explain recommendations un natural language

---

## Datasset & Models


All datasets ans trained models are hosted on Hugging Face Hub:

- Movie (20k) datasets (ratings, metadata)
- Pre-trained similarity models (.`pkl`)
- Vector  indexees for retrieval


This keeps the repository lightweight and deployment-friendly

---


## 
Tech Stack

- **python**
- **scikit-learn**
- **Pandas/Numpy**
- **Faiss**
- **hugging Face Hub**
- **Hugging Face Spaces**
- **LLMs (Mistral instruct)**
- **HTML/CSS(styling)**
- **FastAPI(App interface)**

---


## &#128640; Deployment

The application is deployed on **Hugging Face Spaces**.
- No local LLM required
- Uses HF-hosted models and datasets
- Environment variables securely handle API tokens

---


## How to Run Locally
```
bash

git clone https://github.com/AnujVerma-hub/Movie-Recommendation-System

cd Movie-Recommendation-System

pip install -r requirements.txt

export HF_TOKEN=Your_token_here

python app.py
```







