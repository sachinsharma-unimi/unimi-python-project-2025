🎬 Movie MCQ Question Generator

Python Project – Coding for Data Science (UniMi 2025)
Student: Sachin Sharma · Matricola: 69003A

📖 Overview

This project automatically generates multiple-choice questions (MCQs) from a movie dataset (CSV).
It demonstrates Python fundamentals, data handling using pandas, basic automation logic, and reproducible workflow using Git & virtual environments.

Input:
project/data/imdb_sample.csv
(Columns: title, year, director, main_actor, genres, rating)

Output:
project/data/questions.csv — automatically generated quiz questions.

🚀 Features

Robust CSV loading (handles malformed rows & inconsistent separators)

Automatic generation of MCQs:

“Which year was ___ released?”

“Who starred in ___?”

“Which genre best describes ___?”

CSV output for easy viewing/sharing

Jupyter Notebook demo included

Clean repository structure with reproducible steps

📂 Project Structure
unimi-python-project-2025/
│
├── project/
│   ├── data/
│   │   ├── imdb_sample.csv
│   │   └── questions.csv            # generated
│   └── scripts/
│       └── question_gen.py          # main generator
│
└── notebooks/
    └── demo_question_generator.ipynb

🛠️ Installation & Setup
1. Clone the repository
git clone https://github.com/sachinsharma-unimi/unimi-python-project-2025
cd unimi-python-project-2025

2. Create & activate virtual environment
Git Bash:
python -m venv .venv
source .venv/Scripts/activate

PowerShell:
python -m venv .venv
.\.venv\Scripts\Activate.ps1

3. Install dependencies
pip install -r requirements.txt

▶️ How to Run the Question Generator

From repo root:

python project/scripts/question_gen.py


Expected:

Loaded rows: X
Generated X questions — saved to project/data/questions.csv

📓 Run the Jupyter Notebook Demo
jupyter notebook


Then open:

notebooks/demo_question_generator.ipynb


Inside notebook: Cell → Run All

📝 Example Output

project/data/questions.csv

question	option1	option2	option3	option4	correct
In which year was "Inception" released?	2010	1999	2008	2014	2010
🧪 Notes / Troubleshooting

If git push fails → run:

git pull --rebase origin main
git push


If CSV parsing warnings appear — they are expected due to messy sample data.

If notebook cannot find files → ensure Jupyter was launched from repo root.

👨‍🎓 Author

Sachin Sharma
Coding for Data Science — University of Milan
GitHub: https://github.com/sachinsharma-unimi

✔️ License

MIT License (optional)
