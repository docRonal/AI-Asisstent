# utils.py
import os
import re

def read_text_file(path):
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()
    except Exception:
        return ""

def split_text(text, chunk_size=1000, overlap=200):
    tokens = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        tokens.append(text[start:end])
        start = max(0, end - overlap)
    return tokens

def clean_text(text):
    # минимальная очистка
    text = text.replace("\r\n", "\n")
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()
