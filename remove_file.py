import os
import shutil
from tqdm import tqdm
from random import shuffle

path = "train/labels"
images_path = "train/images"
ls = os.listdir(path)
shuffle(ls)

count = 0
for txt_file in tqdm(ls):
    image_file = txt_file.replace(".txt", ".jpg")
    with open(f"{path}/{txt_file}", "r") as f:
        for line in f.readlines():
            if not line.strip():
                continue
            id = line.split(" ")[0]
            if id == "0":
                count += 1
                os.remove(f"{images_path}/{image_file}")
                os.remove(f"{path}/{txt_file}")
                count += 1
                break
    if count == 1000:
        break
