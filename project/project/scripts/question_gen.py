"""
question_gen.py
---------------------------------------
Core logic for generating multiple-choice quiz questions
from a movie dataset (IMDB/Kaggle).
---------------------------------------
Author: Sachin Sharma (UniMi 2025)
Course: Coding for Data Science & Data Management – Python Module
"""

import pandas as pd
import numpy as np
import random
import requests


# ---------------------------------------
# 1. Load dataset
# ---------------------------------------

def load_dataset(url):
    """
    Load CSV from a GitHub raw URL (or local file path).
    Returns a cleaned pandas DataFrame.
    """
    try:
        df = pd.read_csv(url, engine='python')
    except Exception:
        # Fallback robust read
        txt = requests.get(url).text.strip().splitlines()
        rows = []
        for line in txt:
            parts = line.split(',')
            if len(parts) <= 6:
                rows.append(parts)
            else:
                title = parts[0]
                year = parts[1]
                director = parts[2]
                main_actor = parts[3]
                rating = parts[-1]
                genres = ",".join(parts[4:-1])
                rows.append([title, year, director, main_actor, genres, rating])

        df = pd.DataFrame(rows[1:], columns=rows[0])  # first row is header

    # Clean & normalize
    df.columns = [c.strip().lower() for c in df.columns]

    for c in df.columns:
        if df[c].dtype == object:
            df[c] = df[c].astype(str).str.strip()

    # Convert numeric
    if 'year' in df.columns:
        df['year'] = pd.to_numeric(df['year'], errors='coerce')
    if 'rating' in df.columns:
        df['rating'] = pd.to_numeric(df['rating'], errors='coerce')

    # Split genres
    def split_genres(x):
        if pd.isna(x): 
            return []
        if '|' in x:
            return [g.strip() for g in x.split('|') if g.strip()]
        return [g.strip() for g in x.split(',') if g.strip()]

    if 'genres' in df.columns:
        df['genres_list'] = df['genres'].apply(split_genres)

    return df



# ---------------------------------------
# Helper: sample distractors
# ---------------------------------------

def sample_distractors(df, col, correct, k=3):
    """
    Sample k unique distractors from a column, excluding the correct one.
    """
    vals = df[col].dropna().astype(str).unique().tolist()
    vals = [v for v in vals if str(v) != str(correct)]

    if len(vals) < k:
        return random.sample(vals, len(vals))
    return random.sample(vals, k)



# ---------------------------------------
# Question templates
# ---------------------------------------

def q_year(df, row):
    q = f"In which year was the movie '{row['title']}' released?"
    correct = int(row['year'])
    distractors = sample_distractors(df, 'year', correct)
    options = [str(correct)] + [str(d) for d in distractors]
    random.shuffle(options)
    return {'question': q, 'options': options, 'answer': str(correct)}


def q_actor(df, row):
    q = f"Who is a main actor in '{row['title']}'?"
    correct = row['main_actor']
    distractors = sample_distractors(df, 'main_actor', correct)
    options = [correct] + distractors
    random.shuffle(options)
    return {'question': q, 'options': options, 'answer': correct}


def q_director(df, row):
    q = f"Who directed the movie '{row['title']}'?"
    correct = row['director']
    distractors = sample_distractors(df, 'director', correct)
    options = [correct] + distractors
    random.shuffle(options)
    return {'question': q, 'options': options, 'answer': correct}


def q_genre(df, row):
    if len(row.get('genres_list', [])) == 0:
        return None
    correct = random.choice(row['genres_list'])
    all_genres = list({g for sub in df['genres_list'] for g in sub})
    distractors = [g for g in all_genres if g != correct]
    if len(distractors) >= 3:
        distractors = random.sample(distractors, 3)
    options = [correct] + distractors
    random.shuffle(options)

    q = f"Which of the following is a genre of '{row['title']}'?"
    return {'question': q, 'options': options, 'answer': correct}



# ---------------------------------------
# Master function: generate a quiz
# ---------------------------------------

def generate_quiz(df, n=5):
    """
    Generate n quiz questions using random templates.
    Returns a list of dicts.
    """
    templates = [q_year, q_actor, q_director, q_genre]
    quiz = []

    sample_rows = df.sample(n=min(n, len(df)), random_state=None)
    for _, row in sample_rows.iterrows():
        t = random.choice(templates)
        q = t(df, row)
        if q:
            quiz.append(q)

    return quiz



# ---------------------------------------
# If running this file directly
# ---------------------------------------

if __name__ == "__main__":
    # Replace with your actual raw GitHub URL:
    url = "https://raw.githubusercontent.com/sachinsharma-unimi/unimi-python-project-2025/refs/heads/main/project/data/imdb_sample.csv"
    df = load_dataset(url)

    questions = generate_quiz(df, n=5)

    for q in questions:
        print("\nQuestion:", q['question'])
        for i, opt in enumerate(q['options'], 1):
            print(f"  {i}. {opt}")
        print("Answer:", q['answer'])
