# MCQ Generator (BERT + PKE + WordNet)

This is one of my undergraduate projects back in year 2020. This project statement seems pretty simple now, but still including it as it was one of the projects I was proud of back then and  that helped professors in their professioanal life. During COVID times, education had transformed to online platform from offline. So our professors found it time-consuming to generate weekly based quizzes manually. Then I came up with this solution, developed it and handed over the application to professors who found it reall really helpful (There was no chatGPT back then to help them out, lol).  It's a Flask app that generates multiple‑choice questions (MCQs) from an uploaded document. Text, doc, pdf files are supported. The number of questions to be generated is custom choice of the user. The generated MCQs with answers can be downloaded as CSV file. 
It uses **BERT** for extractive summarization, **PKE MultipartiteRank** for keyphrases, and **NLTK WordNet** for distractors, with simple fallbacks where needed.

---
## Features
- Upload `.txt`, `.pdf`, or `.docx`
 **Uses BERT** to summarize before question generation
- **PKE** keyphrase extraction (MultipartiteRank), with heuristic fallback
- **WordNet** distractors, with fallback to other keyphrases/words
  

---

Find the demo here - > [▶ Watch the demo](https://github.com/amruthak-code/BertMCQ-Generator/releases/download/v1/Screen.Recording.2025-10-04.at.1.16.02.AM.mov)
You can also find it in the releases (v1) . 
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

### If having trouble with PKE on Python 3.13
Use Python **3.11**. (PKE and scikit‑learn wheels are not always published for 3.13 yet.)

---

## How it works 
1. **Extract text** from the uploaded file (pdfplumber/docx2txt/plain text).
2. **Summarize** the text (optional) using a **pre‑trained BERT** summarizer (no training here).
3. **Extract keyphrases** via **PKE MultipartiteRank** (fallback to a simple heuristic).
4. **Build MCQs** by masking keyphrases in sentences (cloze style).
5. **Generate distractors** using **NLTK WordNet** (fallback to other keyphrases/words).

---


## Notes
- First run may download model weights, subsequent runs are faster.
- If Torch/PKE install fails, verify Python 3.11 and use the official Torch selector for your OS/CPU.
- For deterministic results during grading, set a seed in the pipeline (e.g., `random.seed(42)`).
