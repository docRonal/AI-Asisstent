#!/usr/bin/env bash
set -e

PROJECT_DIR="$HOME/ai_assistant"
mkdir -p "$PROJECT_DIR"
cd "$PROJECT_DIR"

python3 -m venv venv
source venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt

echo "Done. Activate with: source $PROJECT_DIR/venv/bin/activate"
echo "Then run the assistant with: python main.py"