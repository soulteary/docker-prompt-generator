from transformers import pipeline, set_seed
import random
import re

text_pipe = pipeline('text-generation', model='succinctly/text2image-prompt-generator')

def text_generate(input):
    seed = random.randint(100, 1000000)
    set_seed(seed)

    for count in range(6):    
        sequences = text_pipe(input, max_length=random.randint(60, 90), num_return_sequences=8)
        list = []
        for sequence in sequences:
            line = sequence['generated_text'].strip()
            if line != input and len(line) > (len(input) + 4) and line.endswith((":", "-", "—")) is False:
                list.append(line)

        result = "\n".join(list)
        result = re.sub('[^ ]+\.[^ ]+','', result)
        result = result.replace("<", "").replace(">", "")
        if result != "":
            return result
        if count == 5:
            return result

input = "Youth can't turn back, so there's no end to youth."
print(input, text_generate(input))