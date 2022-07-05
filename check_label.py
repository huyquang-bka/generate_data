import os
from tqdm import tqdm

path = "train/labels"
label_dict = {}
for i in range(5):
    label_dict[str(i)] = 0
for fileName in tqdm(os.listdir(path)):
    if fileName.endswith(".jpg"):
        continue
    with open(f"{path}/{fileName}", "r") as f:
        for line in f.readlines():
            if not line.strip():
                continue
            id = line.split(" ")[0]
            label_dict[id] += 1

print(label_dict)
total = 0
for k, v in label_dict.items():
    total += v

print(total)
