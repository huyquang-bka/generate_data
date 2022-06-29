import random
from PIL import Image
import cv2
import numpy as np


def augmention(img):
    rotate_angle = random.randint(-15, 15)
    if True:
        img = img.rotate(rotate_angle, resample=Image.NEAREST, expand=1)

    if random.random() > 0.4:
        img = np.array(img)
        img = cv2.GaussianBlur(img, (5, 5), 0)
        img = Image.fromarray(img)

    return img
