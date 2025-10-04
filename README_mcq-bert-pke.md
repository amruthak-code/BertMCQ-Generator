# MCQ Generator (BERT + PKE + WordNet)

A minimal Flask app that generates multiple‑choice questions (MCQs) from an uploaded document. 
It uses **BERT** for extractive summarization, **PKE MultipartiteRank** for keyphrases, and **NLTK WordNet** for distractors, with simple fallbacks where needed.

> **Screenshots:** _Attach your UI and results screenshots here._

---

## Features
- Upload `.txt`, `.pdf`, or `.docx`
- (Optional) **Use BERT** to summarize before question generation
- **PKE** keyphrase extraction (MultipartiteRank), with heuristic fallback
- **WordNet** distractors, with fallback to other keyphrases/words
- Simple, assignment‑friendly UI

---

## Quick Start

> **Python 3.11 is recommended** (Torch & PKE install cleanly). Python 3.13 may fail to build PKE.

```bash
# 0) Unzip and enter the project
cd ~/Downloads
unzip mcq-bert-pke.zip -d mcq-bert-pke
cd mcq-bert-pke

# 1) Create & activate a virtual environment
python -m venv .venv
source .venv/bin/activate     # Windows: .venv\Scripts\Activate.ps1
python -V
pip install -U pip wheel setuptools

# 2) Install Torch first (choose correct build if needed)
pip install torch torchvision torchaudio

# 3) Install remaining dependencies
pip install -r requirements.txt

# 4) Download language resources (once)
python -m spacy download en_core_web_sm
python - <<'PY'
import nltk
nltk.download('wordnet'); nltk.download('omw-1.4'); nltk.download('punkt')
PY

# 5) Run
python app.py
# Open http://127.0.0.1:5000
```

### Having trouble with PKE on Python 3.13?
Use Python **3.11**. (PKE and scikit‑learn wheels are not always published for 3.13 yet.)

---

## How it works (brief)
1. **Extract text** from the uploaded file (pdfplumber/docx2txt/plain text).
2. **Summarize** the text (optional) using a **pre‑trained BERT** summarizer (no training here).
3. **Extract keyphrases** via **PKE MultipartiteRank** (fallback to a simple heuristic).
4. **Build MCQs** by masking keyphrases in sentences (cloze style).
5. **Generate distractors** using **NLTK WordNet** (fallback to other keyphrases/words).

---

## .gitignore (recommended)
Create a `.gitignore` with at least:
```
.venv/
__pycache__/
uploads/
*.pyc
*.DS_Store
```

---

## Deploy / Hosting
- You can host the **code** on GitHub. 
- **GitHub Pages** is static-only and will not run Flask. Use a backend host (Render, Railway, Fly.io, Cloud Run, etc.) for live deployments.

---

## Upload to GitHub (new repo)

1. Create an empty repository on GitHub (no README/license).
2. In your project folder:
```bash
git init
git add .
git commit -m "Initial commit: MCQ generator (BERT + PKE + WordNet)"
git branch -M main
git remote add origin https://github.com/<YOUR-USERNAME>/<REPO-NAME>.git
git push -u origin main
```

> To push updates later:
```bash
git add .
git commit -m "Update"
git push
```

---

## Notes
- First run may download model weights; subsequent runs are faster.
- If Torch/PKE install fails, verify Python 3.11 and use the official Torch selector for your OS/CPU.
- For deterministic results during grading, set a seed in the pipeline (e.g., `random.seed(42)`).

