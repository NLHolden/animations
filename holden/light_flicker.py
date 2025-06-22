import cv2
import numpy as np
from PIL import Image

image_path = "./holden/Holden_Final.png"
original_img = cv2.imread(image_path)
original_img = cv2.cvtColor(original_img, cv2.COLOR_BGR2RGB)

num_frames = 50
flicker_strength = 0.1

frames = []
for i in range(num_frames):
    brightness_factor = 1.0 - (flicker_strength * np.random.rand())

    flicker_img = np.clip(original_img * brightness_factor, 0, 255).astype(np.uint8)
    
    frames.append(Image.fromarray(flicker_img))

gif_path = "flicker_effect.gif"

frames[0].save(
    gif_path,
    format='GIF',
    append_images=frames[1:],
    save_all=True,
    duration=100,
    loop=0
)
