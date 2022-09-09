import torch
from torch.cuda.amp import autocast
from diffusers import StableDiffusionImg2ImgPipeline
import numpy as np
from PIL import Image
import config

TOKEN = config.TOKEN
torch.cuda.empty_cache()
device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")

def pipe_image(prompt,
               init_image=None,
               n_steps=15,
               strength=0.6):
    pipe = StableDiffusionImg2ImgPipeline.from_pretrained("CompVis/stable-diffusion-v1-4", 
                                                revision="fp16", 
                                                torch_dtype=torch.float16,
                                                use_auth_token=TOKEN)

    initial_img = Image.fromarray(init_image).convert("RGB")
    init_img = initial_img.resize((348, 256))
    pipe = pipe.to(device)
    pipe.enable_attention_slicing()
    with autocast():
        image = pipe(prompt=prompt,
                     init_image=init_img,
                     strength=strength,
                     guidance_scale=7.5,
                     num_inference_steps=n_steps).images[0] 
    return image