from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

model = AutoModelForSeq2SeqLM.from_pretrained('Helsinki-NLP/opus-mt-zh-en').eval()
tokenizer = AutoTokenizer.from_pretrained('Helsinki-NLP/opus-mt-zh-en')

def translate(text):
    with torch.no_grad():
        encoded = tokenizer([text], return_tensors='pt')
        sequences = model.generate(**encoded)
        return tokenizer.batch_decode(sequences, skip_special_tokens=True)[0]

from transformers import pipeline, set_seed
import random
import re

text_pipe = pipeline('text-generation', model='succinctly/text2image-prompt-generator')

def text_generate(input):
    seed = random.randint(100, 1000000)
    set_seed(seed)
    text_in_english = translate(input)
    for count in range(6):    
        sequences = text_pipe(text_in_english, max_length=random.randint(60, 90), num_return_sequences=8)
        list = []
        for sequence in sequences:
            line = sequence['generated_text'].strip()
            if line != text_in_english and len(line) > (len(text_in_english) + 4) and line.endswith((':', '-', '—')) is False:
                list.append(line)

        result = "\n".join(list)
        result = re.sub('[^ ]+\.[^ ]+','', result)
        result = result.replace('<', '').replace('>', '')
        if result != '':
            return result
        if count == 5:
            return result

import gradio as gr

with gr.Blocks() as block:
    with gr.Column():
        with gr.Tab('文本生成'):
            input = gr.Textbox(lines=6, label='你的想法', placeholder='在此输入内容...')
            output = gr.Textbox(lines=6, label='生成的 Prompt')
            submit_btn = gr.Button('快给我编')

    submit_btn.click(
        fn=text_generate,
        inputs=input,
        outputs=output
    )

block.queue(max_size=64).launch(show_api=False, enable_queue=True, debug=True, share=False, server_name='0.0.0.0')