import os, random
from typing import List, Dict, Tuple
from .text_utils import sent_tokenize, clean

def extract_text(path: str) -> str:
    ext = os.path.splitext(path)[1].lower()
    if ext == ".txt":
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            return clean(f.read())
    if ext == ".pdf":
        import pdfplumber
        pages = []
        with pdfplumber.open(path) as pdf:
            for p in pdf.pages:
                pages.append(p.extract_text() or "")
        return clean("\\n".join(pages))
    if ext == ".docx":
        import docx2txt
        return clean(docx2txt.process(path) or "")
    raise RuntimeError("Unsupported file type.")

_summarizer = None
def _get_summarizer():
    global _summarizer
    if _summarizer is None:
        from summarizer import Summarizer
        _summarizer = Summarizer()
    return _summarizer

def _summarize(text: str, max_sentences: int = 8) -> str:
    try:
        model = _get_summarizer()
        return clean(model(text, num_sentences=max_sentences))
    except Exception:
        
        sents = [s for s in sent_tokenize(text) if 60 <= len(s) <= 300] or sent_tokenize(text)
        return " ".join(sents[:max_sentences])


def _keyphrases(text: str, top_n: int = 40) -> List[str]:
    try:
        import pke
        extractor = pke.unsupervised.MultipartiteRank()
        extractor.load_document(input=text, language='en')
        extractor.candidate_selection(pos={'NOUN', 'PROPN', 'ADJ'})
        extractor.candidate_weighting(alpha=1.1, threshold=0.75)
        phrases = [kp for kp, _ in extractor.get_n_best(n=top_n)]
        # dedupe
        phrases = sorted(list(set(phrases)), key=lambda p: (-len(p), p.lower()))
        return phrases[:top_n]
    except Exception:
        # fallback: simple noun-ish heuristic
        words = text.split()
        uniq = []
        seen = set()
        for w in words:
            wl = w.strip(",.?!;:()").lower()
            if wl and (w.istitle() or len(w) > 6) and wl not in seen:
                uniq.append(w); seen.add(wl)
        return uniq[:top_n]


def _distractors(answer: str, max_n: int = 20) -> List[str]:
    cands = set()
    try:
        from nltk.corpus import wordnet as wn
        for s in wn.synsets(answer):
            for l in s.lemmas():
                w = l.name().replace("_", " ")
                if w.lower() != answer.lower():
                    cands.add(w)
            for rel in s.hyponyms() + s.hypernyms():
                for l in rel.lemmas():
                    w = l.name().replace("_", " ")
                    if w.lower() != answer.lower():
                        cands.add(w)
    except Exception:
        pass
    out = [c for c in cands if c.isalpha() and 3 <= len(c) <= 20]
    if answer.istitle():
        out = [w.title() for w in out]
    return out[:max_n]


def _mask(sent: str, keyphrases: List[str]):
    s_low = sent.lower()
    for kp in keyphrases:
        i = s_low.find(kp.lower())
        if i != -1:
            real = sent[i:i+len(kp)]
            masked = sent[:i] + "_____" + sent[i+len(kp):]
            return masked.strip(), real.strip()
    return "", ""

def generate_mcqs(text: str, n: int = 8, use_summary: bool = True) -> List[Dict]:
    base = _summarize(text, max_sentences=max(5, n)) if use_summary else text
    sents = [s.strip() for s in sent_tokenize(base) if len(s.strip()) >= 40]
    kps = _keyphrases(base, top_n=60)
    mcqs = []
    used = set()

    for s in sents:
        if len(mcqs) >= n: break
        q, ans = _mask(s, kps)
        if not q or not ans or ans.lower() in used: continue
        ds = _distractors(ans, max_n=30)
        if len(ds) < 3:
            others = [kp for kp in kps if kp.lower() != ans.lower()]
            random.shuffle(others); ds += others[: 3 - len(ds)]
        opts = [ans] + [d for d in ds if d.lower() != ans.lower()][:3]
        random.shuffle(opts)
        mcqs.append({"question": q, "options": opts, "answer": ans})
        used.add(ans.lower())

    i = 0
    while len(mcqs) < n and i < len(sents):
        s = sents[i]; i += 1
        words = [w.strip(".,!?;:()") for w in s.split() if len(w.strip(".,!?;:()")) >= 6]
        if not words: continue
        ans = random.choice(words)
        q = s.replace(ans, "_____", 1)
        ds = _distractors(ans, max_n=30)
        if len(ds) < 3:
            pool = [w for w in words if w.lower() != ans.lower()]
            random.shuffle(pool); ds += pool[: 3 - len(ds)]
        opts = [ans] + ds[:3]
        random.shuffle(opts)
        mcqs.append({"question": q, "options": opts, "answer": ans})
    return mcqs[:n]
