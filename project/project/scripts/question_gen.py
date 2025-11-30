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
        # ---------------------------
# simple question generation
# ---------------------------
import random
from pathlib import Path
out_path = Path('project/data/questions.csv')

# helper to get n random distinct values from a Series excluding the correct one
def sample_other(series, correct, n=3):
    pool = series.dropna().astype(str).unique().tolist()
    pool = [x for x in pool if x != str(correct)]
    if len(pool) < n:
        # if not enough distinct, repeat some (shouldn't happen for decent dataset)
        pool = (pool * (n // max(1, len(pool)) + 2))[:n]
    return random.sample(pool, n)

questions = []
rows = df.to_dict(orient='records')

for r in rows:
    title = r.get('title') or r.get('movie_title') or 'Unknown Title'
    year = r.get('year') or r.get('release_year') or ''
    actor = r.get('main_actor') or r.get('actor') or ''
    genres = r.get('genres') or ''

    # Q1: year question (only if year is available)
    if year and str(year).strip():
        correct = str(year)
        distractors = sample_other(df['year'].astype(str), correct, n=3)
        q = {
            'type': 'year',
            'question': f'In which year was "{title}" released?',
            'correct': correct,
            'd1': distractors[0],
            'd2': distractors[1],
            'd3': distractors[2],
            'meta': title
        }
        questions.append(q)

    # Q2: actor question (only if actor is available)
    if actor and str(actor).strip():
        correct = str(actor)
        distractors = sample_other(df['main_actor'].astype(str), correct, n=3)
        q = {
            'type': 'actor',
            'question': f'Who starred as a main actor in "{title}"?',
            'correct': correct,
            'd1': distractors[0],
            'd2': distractors[1],
            'd3': distractors[2],
            'meta': title
        }
        questions.append(q)

# shuffle questions and write to CSV
random.shuffle(questions)

if questions:
    import csv
    fieldnames = ['type','question','correct','d1','d2','d3','meta']
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open('w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for q in questions:
            writer.writerow(q)

    print(f"\nGenerated {len(questions)} questions — saved to {out_path}")
    # print first 5 for quick check
    from itertools import islice
    print("\nSample questions:")
    for q in list(islice(questions, 5)):
        print("-", q['question'])
        print("   A)", q['correct'], "| B)", q['d1'], "| C)", q['d2'], "| D)", q['d3'])
else:
    print("No questions generated (not enough data).")

