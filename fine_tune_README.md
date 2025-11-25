# Fine-tuning plan (QLoRA) — краткая инструкция

1. Подготовь датасет JSONL с парами instruction/response (пример):
{"instruction":"Что такое Counter-Strike 2?","output":"Counter-Strike 2 — ... (актуальная информация)... "}
2. Используй репозитории: transformers + peft + bitsandbytes + accelerate/trlx/qlora scripts (пример: https://github.com/artidoro/qlora)
3. Пример команд (на машине с A100/4090 и CUDA):
pip install transformers accelerate bitsandbytes peft datasets safetensors
python finetune_qlora.py \
  --model_name_or_path path/to/mistral-7b-pytorch \
  --dataset your_dataset.jsonl \
  --output_dir ./mistral_finetuned \
  --use_peft lora --lora_r 8 --lora_alpha 16 --lora_dropout 0.05 \
  --bits 4

4. После обучения у тебя будут LoRA веса (safetensors). Применяй адаптер при инференсе:
- либо с Transformers pipeline
- либо переконвертируй в GGUF с помощью утилит (или загрузить base FP16 + adapter через inference pipeline)
