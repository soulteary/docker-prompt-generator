from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

model = AutoModelForSeq2SeqLM.from_pretrained("Helsinki-NLP/opus-mt-zh-en").eval()
tokenizer = AutoTokenizer.from_pretrained("Helsinki-NLP/opus-mt-zh-en")

def translate(text):
    with torch.no_grad():
        encoded = tokenizer([text], return_tensors="pt")
        sequences = model.generate(**encoded)
        return tokenizer.batch_decode(sequences, skip_special_tokens=True)[0]

input = "青春不能回头，所以青春没有终点。 ——《火影忍者》"
print(input, translate(input))