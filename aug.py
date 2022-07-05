import random
from PIL import Image
import cv2
import numpy as np
import os
import random

noise_bg_path = "Noise_bg"
list_noise_bg = os.listdir(noise_bg_path)


def random_add_bg_noise(img, expand=70):
    bg_path = random.choice(list_noise_bg)
    bg_image = cv2.imread(os.path.join(noise_bg_path, bg_path))
    img = np.array(img)
    H, W = img.shape[:2]
    # bg_image_overlay = cv2.resize(bg_image, dsize=(W, H))
    bg_image_overlay = np.ones_like(img) * 255
    alpha = random.choice([0.5, 0.6, 0.7, 0.8, 0.9])
    img_add_weight = cv2.addWeighted(img, alpha, bg_image_overlay, 1 - alpha, 0)
    bg_image = cv2.resize(bg_image, (W + expand * 2, H + expand * 2))
    bg_image[expand:expand + H, expand:expand + W] = img_add_weight
    return Image.fromarray(bg_image)


def augmention(img):
    rotate_angle = random.randint(-5, 5)
    img = random_add_bg_noise(img)
    if True:
        img = img.rotate(rotate_angle, resample=Image.NEAREST, expand=1)

    if random.random() > 0.4:
        img = np.array(img)
        img = cv2.GaussianBlur(img, (5, 5), 0)
        img = Image.fromarray(img)

    w, h = img.size
    img = img.crop((50, 50, w - 50, h - 50))

    return img
