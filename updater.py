# updater.py
import os
import requests
from urllib.parse import urlparse
import subprocess

TO_FETCH = [
    # добавь ссылки на репозитории, википедию, archwiki, официальные доки
    "https://raw.githubusercontent.com/docker/cli/master/README.md",
    "https://en.wikipedia.org/wiki/Virtual_environment_(Python)",
    "https://wiki.archlinux.org/title/Steam",
    "https://docs.python.org/3/tutorial/venv.html",
    "https://github.com/langchain-ai/langchain",
    "https://github.com/ggerganov/llama.cpp"
    "https://github.com/rasbt/LLMs-from-scratch"
    "https://simonwillison.net/2025/Mar/11/using-llms-for-code/?utm_source=chatgpt.com"
    "https://github.com/huybery/Awesome-Code-LLM?utm_source=chatgpt.com"
    "https://github.com/codefuse-ai/Awesome-Code-LLM?utm_source=chatgpt.com"
    "https://github.com/sapritanand/Code-Generation-using-LLM?utm_source=chatgpt.com"
]

OUT_DIR = "data/raw_texts"

def fetch_url_to_file(url, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    r = requests.get(url, timeout=30)
    if r.status_code == 200:
        filename = os.path.basename(urlparse(url).path) or "doc.txt"
        path = os.path.join(out_dir, filename)
        with open(path, "w", encoding="utf-8") as f:
            f.write(r.text)
        print("Saved", path)
    else:
        print("Failed", url, r.status_code)

if __name__ == "__main__":
    for u in TO_FETCH:
        try:
            fetch_url_to_file(u, OUT_DIR)
        except Exception as e:
            print("Error", e)
    # после скачивания — run build_embeddings
    print("Запускаю build_embeddings.py ...")
    subprocess.run(["python", "build_embeddings.py"])
