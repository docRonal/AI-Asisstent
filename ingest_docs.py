"""
Собирает тексты из указанных директорий в одну папку для дальнейшей обработки.
Пример использования:
  python ingest_docs.py --dirs ~/projects ~/docs /usr/share/doc --out data/raw_texts
"""
import argparse
import os
from pathlib import Path
from utils import read_text_file, clean_text
from tqdm import tqdm

TEXT_EXT = {".md", ".txt", ".rst", ".html", ".py", ".c", ".cpp", ".h", ".json", ".yml"}

def iterate_files(dirs):
    for d in dirs:
        for root, _, files in os.walk(d):
            for f in files:
                p = Path(root) / f
                if p.suffix.lower() in TEXT_EXT or f.lower().startswith("readme"):
                    yield p

def save_texts(paths, outdir):
    os.makedirs(outdir, exist_ok=True)
    idx = 0
    for p in tqdm(paths):
        text = read_text_file(str(p))
        text = clean_text(text)
        if not text:
            continue
        fname = f"doc_{idx}.txt"
        with open(os.path.join(outdir, fname), "w", encoding="utf-8") as fo:
            fo.write(f"## SOURCE: {p}\n\n")
            fo.write(text)
        idx += 1

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dirs", nargs="+", required=True)
    parser.add_argument("--out", default="data/raw_texts")
    args = parser.parse_args()

    paths = list(iterate_files(args.dirs))
    save_texts(paths, args.out)
    print("Saved:", args.out)
