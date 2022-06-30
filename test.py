from PIL import Image
import numpy as np
from perlin_noise import PerlinNoise
import cv2

for i in range(10):
    perlin_noise_image_dict = {}
    for j in range(3):
        noise = PerlinNoise(octaves=5)
        xpix, ypix = 100, 100
        pic = [[noise([i/xpix, j/ypix]) for j in range(xpix)] for i in range(ypix)]

        image = Image.fromarray(np.array(pic) * 255, 'L')
        image = np.array(image)
        perlin_noise_image_dict[j] = image
    final_img = np.dstack([perlin_noise_image_dict[0], perlin_noise_image_dict[1], perlin_noise_image_dict[2]]).astype(np.uint8)
    cv2.imwrite('Noise_bg/{}.jpg'.format(i), final_img)
    print(final_img.shape)
    # cv2.imshow("image", final_img)
    # cv2.waitKey(0)