#!/usr/bin/env python3
"""
Simple robust question generator for the project:
 - reads a CSV with movies (columns like title,year,director,main_actor,genres,rating)
 - tolerates occasional malformed rows
 - generates simple MCQ questions (who starred, which year, genre)
 - writes questions to project/data/questions.csv
"""
from pathlib import Path
import random
import pandas as pd
import numpy as np

HERE = Path(__file__).resolve().parents[1]  # repo/project
DATA_DIR = HERE / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

INPUT_CSV = DATA_DIR / "imdb_sample.csv"
OUTPUT_CSV = DATA_DIR / "questions.csv"

def read_robust_csv(path):
    # Try default parser first, then fall back to python engine with loose parsing.
    try:
        df = pd.read_csv(path)
        return df
    except Exception:
        # try with python engine and warn on bad lines (pandas >=1.3)
        try:
            df = pd.read_csv(path, engine="python", on_bad_lines="warn")
            return df
        except TypeError:
            # older pandas that doesn't have on_bad_lines param
            df = pd.read_csv(path, engine="python", error_bad_lines=False, warn_bad_lines=True)
            return df

def normalise_cols(df):
    # Lower-case column names and strip whitespace
    df.columns = [c.strip() for c in df.columns]
    # keep only useful columns if present
    wanted = []
    for c in ("title", "movie_title"):
        if c in df.columns:
            wanted.append(c)
            break
    # optional columns
    for c in ("year", "release_year"):
        if c in df.columns:
            wanted.append(c); break
    for c in ("main_actor","actor","lead"):
        if c in df.columns:
            wanted.append(c); break
    for c in ("director",):
        if c in df.columns:
            wanted.append(c); break
    for c in ("genres",):
        if c in df.columns:
            wanted.append(c); break
    if "rating" in df.columns:
        wanted.append("rating")
    return df, wanted

def sample_distractors(df, correct_value, field, n=3):
    # sample distractors from dataframe values in that field (exclude correct)
    candidates = df[field].dropna().astype(str).unique().tolist()
    candidates = [c for c in candidates if c != str(correct_value)]
    if not candidates:
        return []
    return random.sample(candidates, k=min(n, len(candidates)))

def make_questions(df, n_questions=20, seed=42):
    random.seed(seed)
    np.random.seed(seed)
    out = []
    # ensure typical column names exist
    df = df.copy()
    for i, row in df.iterrows():
        # unify possible title columns
        title = None
        for c in ("title","movie_title"):
            if c in df.columns:
                title = row.get(c)
                break
        if pd.isna(title):
            continue
        # pick a question type
        qtype = random.choice(["year","actor","genre"])
        if qtype == "year":
            if "year" not in df.columns and "release_year" not in df.columns:
                continue
            year_field = "year" if "year" in df.columns else "release_year"
            correct = row.get(year_field)
            if pd.isna(correct):
                continue
            distract = sample_distractors(df, correct, year_field, 3)
            # some formatting
            choices = [str(correct)] + [str(x) for x in distract]
            choices = choices[:4]
            random.shuffle(choices)
            qtext = f'In which year was "{title}" released?'
            out.append({
                "type":"year",
                "question": qtext,
                "correct": str(correct),
                "d1": choices[0] if len(choices)>0 else "",
                "d2": choices[1] if len(choices)>1 else "",
                "d3": choices[2] if len(choices)>2 else "",
                "d4": choices[3] if len(choices)>3 else "",
                "meta": title
            })
        elif qtype == "actor":
            # need main actor column
            actor_col = None
            for c in ("main_actor","actor","lead"):
                if c in df.columns:
                    actor_col = c; break
            if not actor_col:
                continue
            correct = row.get(actor_col)
            if pd.isna(correct):
                continue
            distracts = sample_distractors(df, correct, actor_col, 3)
            choices = [str(correct)] + [str(x) for x in distracts]
            choices = choices[:4]
            random.shuffle(choices)
            qtext = f'Who starred as a main actor in "{title}"?'
            out.append({
                "type":"actor",
                "question": qtext,
                "correct": str(correct),
                "d1": choices[0] if len(choices)>0 else "",
                "d2": choices[1] if len(choices)>1 else "",
                "d3": choices[2] if len(choices)>2 else "",
                "d4": choices[3] if len(choices)>3 else "",
                "meta": title
            })
        else:  # genre
            if "genres" not in df.columns:
                continue
            correct = row.get("genres")
            if pd.isna(correct):
                continue
            # genres could be pipe/comma separated; take first as canonical
            if isinstance(correct, str) and ("," in correct or "|" in correct):
                correct_first = correct.split(",")[0].split("|")[0].strip()
            else:
                correct_first = str(correct)
            distracts = sample_distractors(df, correct_first, "genres", 3)
            choices = [str(correct_first)] + [str(x) for x in distracts]
            choices = choices[:4]
            random.shuffle(choices)
            qtext = f'Which of these best describes the genre of "{title}"?'
            out.append({
                "type":"genre",
                "question": qtext,
                "correct": str(correct_first),
                "d1": choices[0] if len(choices)>0 else "",
                "d2": choices[1] if len(choices)>1 else "",
                "d3": choices[2] if len(choices)>2 else "",
                "d4": choices[3] if len(choices)>3 else "",
                "meta": title
            })
        if len(out) >= n_questions:
            break
    return out

def main():
    if not INPUT_CSV.exists():
        print("ERROR: input CSV not found:", INPUT_CSV)
        return 2
    df = read_robust_csv(INPUT_CSV)
    print("Loaded rows:", len(df))
    df, cols = normalise_cols(df)
    # if genres column exists and is single string, fine
    questions = make_questions(df, n_questions=20)
    if not questions:
        print("No questions generated (not enough columns/data).")
        return 3
    qdf = pd.DataFrame(questions)
    qdf.to_csv(OUTPUT_CSV, index=False)
    print(f"Generated {len(qdf)} questions — saved to {OUTPUT_CSV}")
    # print a few sample questions
    for r in qdf.head(5).itertuples(index=False):
        print("-", r.question)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
