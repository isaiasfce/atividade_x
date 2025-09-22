import re

URL_PATTERN = re.compile(r'https?://\S+|www\.S+')
MENTION_HASHTAG = re.compile(r'[@#]\w+')
NON_ALNUM = re.compile(r'[^0-9a-zA-ZÀ-ÿ\s]')
MULTI_SPACE = re.compile = re.compile(r'\s+')

def clean_text(text: str) -> str:
    t = text or ""
    t = URL_PATTERN.sub('', t)
    t = MENTION_HASHTAG.sub('', t)
    t = NON_ALNUM.sub(' ', t)
    t = t.lower().strip()
    t = MULTI_SPACE.sub(' ', t)
    return t