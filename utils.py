import torch
from torch.cuda.amp import autocast
from diffusers import StableDiffusionPipeline
import numpy as np
import PIL
from PIL import Image
import config

TOKEN = config.TOKEN

device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")

def preprocess(image):
    w, h = image.size
    w, h = map(lambda x: x - x % 32, (w, h))
    image = image.resize((w, h), resample=PIL.Image.LANCZOS)
    image = np.array(image).astype(np.float32) / 255.0
    image = image[None].transpose(0, 3, 1, 2)
    image = torch.from_numpy(image)
    return 2.*image - 1.

def pipe_image(prompt,
               init_image=None,
               n_steps=15,
               strength=0.6):
    pipe = StableDiffusionPipeline.from_pretrained("CompVis/stable-diffusion-v1-4", 
                                                revision="fp16", 
                                                torch_dtype=torch.float32,
                                                use_auth_token=TOKEN)
    initial_img = preprocess(Image.fromarray(init_image).convert("RGB"))
    init_img = initial_img.to(device)
    with autocast():
        image = pipe(prompt=prompt,
                     init_image=init_img,
                     strength=strength,
                     guidance_scale=7.5,
                     num_inference_steps=n_steps)["sample"][0] 
    return image