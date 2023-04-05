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

from clip_interrogator import Config, Interrogator
import torch
import gradio as gr

config = Config()
config.device = 'cuda' if torch.cuda.is_available() else 'cpu'
config.blip_offload = False if torch.cuda.is_available() else True
config.chunk_size = 2048
config.flavor_intermediate_count = 512
config.blip_num_beams = 64
config.clip_model_name = "ViT-H-14/laion2b_s32b_b79k"

ci = Interrogator(config)

def get_prompt_from_image(image, mode):
    image = image.convert('RGB')
    if mode == 'best':
        prompt = ci.interrogate(image)
    elif mode == 'classic':
        prompt = ci.interrogate_classic(image)
    elif mode == 'fast':
        prompt = ci.interrogate_fast(image)
    elif mode == 'negative':
        prompt = ci.interrogate_negative(image)
    return prompt

with gr.Blocks() as block:
    with gr.Column():
        gr.HTML('<h1>MidJourney / SD2 懒人工具</h1>')
        with gr.Tab('从图片中生成'):
            with gr.Row():
                input_image = gr.Image(type='pil')
                with gr.Column():
                    input_mode = gr.Radio(['best', 'fast', 'classic', 'negative'], value='best', label='Mode')
            img_btn = gr.Button('这图里有啥')
            output_image = gr.Textbox(lines=6, label='生成的 Prompt')

        with gr.Tab('从文本中生成'):
            input_text = gr.Textbox(lines=6, label='你的想法', placeholder='在此输入内容...')
            output_text = gr.Textbox(lines=6, label='生成的 Prompt')
            text_btn = gr.Button('快给我编')

    img_btn.click(fn=get_prompt_from_image, inputs=[input_image, input_mode], outputs=output_image)
    text_btn.click(fn=text_generate, inputs=input_text, outputs=output_text)

block.queue(max_size=64).launch(show_api=False, enable_queue=True, debug=True, share=False, server_name='0.0.0.0')