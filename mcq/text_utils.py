import re
def sent_tokenize(text: str):
    try:
        from nltk import sent_tokenize as nltk_sent_tokenize
        return nltk_sent_tokenize(text)
    except Exception:
        return re.split(r'(?<=[.!?])\\s+', text)
def clean(s: str) -> str:
    import re
    s = s.replace('\\xa0',' ').replace('\\n',' ')
    return re.sub(r'\\s+',' ', s).strip()
