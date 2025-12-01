# Python Project – Coding for Data Science (UniMi 2025)

### Student Details
- Name: Sachin Sharma  
- Student ID (Matricola): 69003A  
- Email: sachin.sharma@studenti.unimi.it  
- Course: Coding for Data Science & Data Management – Python Module  
- University: Università degli Studi di Milano (UniMi)

---

## Project Title
**Who Wants to Be a Millionaire — automatic multiple-choice quiz generator (IMDB dataset)**

---

## Project Description
Automatically generate multiple-choice quizzes from a movie dataset (IMDB / Kaggle).  
Each question is generated from dataset facts (e.g., actor in movie X, year of release, genre). For each question the system creates 4 options (1 correct + 3 distractors) with controlled difficulty. Project includes data ingestion, cleaning, question-generation logic, scoring, and a small Streamlit demo as optional bonus.

---

## Repository Structure

unimi-python-project-2025/
│
├── project/
│   ├── data/            → Raw dataset (CSV)
│   ├── notebooks/       → Jupyter Notebooks for analysis
│   ├── scripts/         → Python scripts used for cleaning or plotting
│   ├── app/             → Streamlit demo (optional)
│   └── outputs/         → Final charts, tables, and report
│
├── README.md
├── requirements.txt
└── project_report.pdf
# Question Generator – Python Project

This project generates multiple-choice questions from a simple IMDb-style CSV file.

---

## Quick Usage

### 1. Create & activate venv
python -m venv .venv
source .venv/Scripts/activate      # Git Bash on Windows
# OR
.\venv\Scripts\activate            # PowerShell on Windows

### 2. Install dependencies
pip install -r requirements.txt

### 3. Run the generator
python project/scripts/question_gen.py

**Output file:**
project/data/questions.csv

---

## Input format
The script expects a CSV file with columns:
`title,year,director,main_actor,genres,rating`

Example input file:
`project/data/imdb_sample.csv`

---

## Output
The script generates ~5–10 MCQ questions such as:
- "In which year was 'Inception' released?"
- "Who starred as main actor in 'The Matrix'?"

These are saved into:
`project/data/questions.csv`

