# Robust CSV loader for imdb_sample.csv

from pathlib import Path
import pandas as pd

p = Path('project/data/imdb_sample.csv')

rows = []
with p.open('r', encoding='utf-8') as f:
    header = f.readline().strip()
    for ln, line in enumerate(f, start=2):
        line = line.rstrip('\n')
        if not line:
            continue
        # split at most 5 times so the genres field keeps internal commas
        parts = line.split(',', 5)
        if len(parts) != 6:
            print(f"Skipping malformed line {ln}: expected 6 parts, saw {len(parts)}")
            continue
        rows.append(parts)

# column names
cols = [c.strip() for c in header.split(',')]
if len(cols) != 6:
    cols = ['title','year','director','main_actor','genres','rating']

df = pd.DataFrame(rows, columns=cols)
df['rating'] = pd.to_numeric(df['rating'], errors='coerce')

print("Loaded rows:", len(df))
print(df.head().to_string(index=False))

# -------------------------------------------
# Below this line you will add question logic
# -------------------------------------------
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
