#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from llama_cpp import Llama
import subprocess
import shutil
import os

# -----------------------------
# Настройка модели
# -----------------------------
MODEL_PATH = "/home/krvh/llm_model/mistral-7b-instruct-v0.2.Q5_K_M.gguf"
llm = Llama(model_path=MODEL_PATH, n_ctx=51102)

# -----------------------------
# История сообщений
# -----------------------------
messages = []

# -----------------------------
# Создание промпта из истории
# -----------------------------
def build_prompt(messages):
    prompt = "Ты ассистент, говорящий на русском языке. " \
             "Отвечай вежливо, полезно и коротко.\n"
    for m in messages:
        role = m["role"]
        content = m["content"]
        if role == "user":
            prompt += f"Пользователь: {content}\n"
        elif role == "assistant":
            prompt += f"Ассистент: {content}\n"
    prompt += "Ассистент: "
    return prompt

# -----------------------------
# Запрос к LLM
# -----------------------------
def ask_agent(messages, max_tokens=300):
    prompt = build_prompt(messages)
    response = llm(prompt, max_tokens=max_tokens,
                   stop=["Пользователь:", "Ассистент:"])
    text = response["choices"][0]["text"]
    return text.strip()

# -----------------------------
# Запуск приложений (любой из PATH)
# -----------------------------
def run_app(app_name: str):
    # Проверяем, что приложение существует в системе
    path = shutil.which(app_name)

    if not path:
        print(f"Приложение '{app_name}' не найдено в системе!")
        print("Подсказка: в Linux Telegram называется 'telegram-desktop'")
        return

    print(f"Запускаю: {app_name}")
    try:
        subprocess.Popen([path])
    except Exception as e:
        print("Ошибка при запуске:", e)

# -----------------------------
# Выполнение shell-команд
# -----------------------------
def run_command(command):
    print(f"Запрос на выполнение команды: {command}")
    confirm = input("Подтвердить выполнение? (y/n): ").lower()
    if confirm == "y":
        try:
            subprocess.run(command, shell=True, check=True)
        except Exception as e:
            print("Ошибка при выполнении:", e)
    else:
        print("Команда отменена.")

# -----------------------------
# Запись в файл
# -----------------------------
def write_file(path, content):
    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Файл записан: {path}")
    except Exception as e:
        print("Ошибка при записи файла:", e)

# -----------------------------
# Главный цикл
# -----------------------------
def main():
    print("=== Локальный ассистент на Mistral 7B ===")
    print("Для выхода напишите 'выход', 'exit' или 'quit'.")

    while True:
        user_input = input("Ты: ").strip()

        if user_input.lower() in ["выход", "exit", "quit"]:
            print("Завершение работы...")
            break

        # Запуск приложений
        if user_input.startswith("run "):
            app_name = user_input[len("run "):].strip()
            run_app(app_name)
            continue

        # Выполнение shell команд
        if user_input.startswith("cmd "):
            command = user_input[len("cmd "):].strip()
            run_command(command)
            continue

        # Запись в файл
        if user_input.startswith("write "):
            parts = user_input.split(" ", 2)
            if len(parts) < 3:
                print("Использование: write <путь> <текст>")
                continue
            path = parts[1]
            content = parts[2]
            write_file(path, content)
            continue

        # ИИ-ответ
        messages.append({"role": "user", "content": user_input})
        try:
            answer = ask_agent(messages)
        except Exception as e:
            print("Ошибка модели:", e)
            continue

        print(f"Агент: {answer}")
        messages.append({"role": "assistant", "content": answer})

# -----------------------------
# Запуск
# -----------------------------
if __name__ == "__main__":
    main()
