"""
question_gen.py
----------------

This script loads a movie dataset (CSV), cleans column names,
and automatically generates multiple-choice questions (MCQs)
based on movie attributes such as:

- Release year
- Main actor
- Genre

The script outputs a CSV file named:
    project/data/questions.csv

This file includes automatically generated MCQs with:
question, correct option, and 3 distractor options.

Author: Sachin Sharma
Course: Coding for Data Science — UniMi (2025)
"""

import pandas as pd
import random
from pathlib import Path


# ---------------------------------------------------------------------
# 1) Robust CSV Reader
# ---------------------------------------------------------------------

def read_robust_csv(path):
    """
    Reads a CSV file using a robust strategy:
      1. Attempt fast C parser
      2. Fallback to Python engine + warning mode for malformed lines

    Parameters:
        path (str or Path): path to CSV file

    Returns:
        pd.DataFrame: parsed DataFrame
    """
    try:
        # Fast parser (C engine) — fails on malformed rows
        return pd.read_csv(path)
    except Exception as e1:
        print("Fast CSV parser failed. Falling back to Python engine...")
        print("Reason:", e1)

        try:
            # Python engine — tolerant to bad rows
            return pd.read_csv(path, engine="python", on_bad_lines="warn")

        except TypeError:
            # Compatibility for older pandas versions
            return pd.read_csv(path, engine="python", error_bad_lines=False, warn_bad_lines=True)


# ---------------------------------------------------------------------
# 2) Normalize column names
# ---------------------------------------------------------------------

def normalize_columns(df):
    """
    Lowercases and strips whitespace from column names.

    Parameters:
        df (pd.DataFrame): input dataframe

    Returns:
        pd.DataFrame: cleaned dataframe
    """
    df = df.copy()
    df.columns = [str(c).strip().lower() for c in df.columns]
    return df


# ---------------------------------------------------------------------
# 3) Generate MCQ Questions
# ---------------------------------------------------------------------

def generate_questions(df, n_questions=20, seed=42):
    """
    Generates multiple-choice questions from movie dataset.

    Question types include:
      - Release year (e.g., “In which year was The Matrix released?”)
      - Main actor (e.g., “Who starred in The Matrix?”)
      - Genre (e.g., “Which genre best describes Inception?”)

    Parameters:
        df (pd.DataFrame): movie DataFrame with columns:
                           title, year, main_actor, genres
        n_questions (int): number of questions to generate
        seed (int): random seed for repeatability

    Returns:
        list[dict]: list of question dictionaries
    """
    random.seed(seed)
    questions = []

    rows = df.to_dict(orient="records")

    # Collect values for distractors
    all_years = [r.get("year") for r in rows if pd.notna(r.get("year"))]
    all_actors = [r.get("main_actor") for r in rows if pd.notna(r.get("main_actor"))]
    all_genres = [r.get("genres") for r in rows if pd.notna(r.get("genres"))]

    def get_distractors(pool, correct, k=3):
        """Return k distractor values, different from the correct answer."""
        unique = list(set([p for p in pool if p != correct]))
        random.shuffle(unique)
        return unique[:k] + [""] * (k - len(unique))

    for _ in range(n_questions):
        movie = random.choice(rows)

        title = movie.get("title")
        year = movie.get("year")
        actor = movie.get("main_actor")
        genres = movie.get("genres")

        # Choose question type
        qtype = random.choice(["year", "actor", "genre"])

        if qtype == "year" and pd.notna(year):
            question = f"In which year was \"{title}\" released?"
            distractors = get_distractors(all_years, year)
            correct = year

        elif qtype == "actor" and pd.notna(actor):
            question = f"Who starred as the main actor in \"{title}\"?"
            distractors = get_distractors(all_actors, actor)
            correct = actor

        elif qtype == "genre" and pd.notna(genres):
            # Sometimes genres have multiple entries — take the first
            correct = str(genres).split(",")[0]
            question = f"Which best describes the genre of \"{title}\"?"
            distractors = get_distractors(all_genres, genres)

        else:
            continue  # Skip if missing fields

        # Build MCQ dictionary
        q = {
            "type": qtype,
            "question": question,
            "correct": str(correct),
            "d1": str(distractors[0]),
            "d2": str(distractors[1]),
            "d3": str(distractors[2]),
            "meta": title
        }
        questions.append(q)

    return questions


# ---------------------------------------------------------------------
# 4) Main execution block
# ---------------------------------------------------------------------

def main():
    """Main execution: loads CSV, generates questions, saves output."""
    data_dir = Path("project/data")
    input_csv = data_dir / "imdb_sample.csv"
    output_csv = data_dir / "questions.csv"

    print("Loading dataset from:", input_csv)

    df = read_robust_csv(input_csv)
    df = normalize_columns(df)

    print("Loaded rows:", len(df))

    questions = generate_questions(df, n_questions=20)
    print(f"Generated {len(questions)} questions.")

    out_df = pd.DataFrame(questions)
    out_df.to_csv(output_csv, index=False)

    print("Saved questions →", output_csv)


# Run main only when script executed directly
if __name__ == "__main__":
    main()
