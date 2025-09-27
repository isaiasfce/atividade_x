import re # Biblioteca para localizar e substituir padrões em strings

URL_PATTERN = re.compile(r'https?://\S+|www\.S+') # Remove links
MENTION_HASHTAG = re.compile(r'[@#]\w+') # Remove menções e hashtags
NON_ALNUM = re.compile(r'[^0-9a-zA-ZÀ-ÿ\s]') # Remove caracteres que não são letras, números ou acentos
MULTI_SPACE = re.compile(r'\s+') # Substitui espaços múltiplos por apenas um espaço

def clean_text(text: str) -> str:
    t = text or ""
    t = URL_PATTERN.sub('', t)
    t = MENTION_HASHTAG.sub('', t)
    t = NON_ALNUM.sub(' ', t)
    t = t.lower().strip()
    t = MULTI_SPACE.sub(' ', t)
    return t