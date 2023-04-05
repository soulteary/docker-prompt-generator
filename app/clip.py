from clip_interrogator import Config, Interrogator
import torch
config = Config()
config.device = 'cuda' if torch.cuda.is_available() else 'cpu'
config.blip_offload = False if torch.cuda.is_available() else True
config.chunk_size = 2048
config.flavor_intermediate_count = 512
config.blip_num_beams = 64
config.clip_model_name = "ViT-H-14/laion2b_s32b_b79k"
ci = Interrogator(config)

def get_prompt_from_image(image):
    return ci.interrogate(image.convert('RGB'))

import requests
import shutil
r = requests.get("https://pic1.zhimg.com/v2-6e056c49362bff9af1eb39ce530ac0c6_1440w.jpg?source=d16d100b", stream=True)
if r.status_code == 200:
    with open('./image.jpg', 'wb') as f:
        r.raw.decode_content = True
        shutil.copyfileobj(r.raw, f) 

from PIL import Image
print(get_prompt_from_image(Image.open('./image.jpg')))