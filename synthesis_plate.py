import cv2
import glob
import os
import random
from PIL import ImageFont, ImageDraw, Image
import numpy as np
from tqdm import tqdm
import math
from generate_image import *
from utils import *
from aug import augmention
import args
from threading import Thread

try:
    os.mkdir(args.output_dir)
except:
    pass

try:
    os.mkdir(args.output_dir + "/images")
    os.mkdir(args.output_dir + "/labels")
except:
    pass

available_number = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
available_char = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
                  'U', 'V', 'W', 'X', 'Y', 'Z']

# available_template = ['NN-CN/NNNN', 'NN-CN/NNN.NN', 'NNC/NNN.NN', 'NNC/NNNN', 'NNC-NNNN', 'NNC-NNN.NN', 'NN-CC/NNN-NN',
#                       'NN-CC-NNN-NN', 'CC/NN-NN', 'CC-NN-NN']
# available_template = ['NNC/NNNNN', 'NNC-NNNNN', 'NNC/NNNN', 'NNC-NNNN']
available_template = ['NNC/NNNNN', 'NNC/NNNN', "NNCN/NNNN", "NNCN/NNNNN", "NNCC/NNNNN"]
available_square_bg = sorted(glob.glob('background/square*.jpg'))
available_rec_bg = sorted(glob.glob('background/rec*.jpg'))

total_template = len(available_template)
total_number = len(available_number)
total_char = len(available_char)

visual = False

data = open('classes.txt', 'r').read().strip().split('\n')
box_label = dict()
for i in range(len(data)):
    box_label[data[i]] = i

assert os.path.exists('classes.txt') == True, 'Not exists file classes.txt, try again !'


def sort_boxes(boxes, max_distance=0.3):
    total_numb = len(boxes)

    line_1 = []
    sorted_line_1 = []
    line_2 = []
    sorted_line_2 = []

    min_y = np.min(boxes[:, 1])

    for i in range(total_numb):
        if math.fabs(boxes[i][1] - min_y) < max_distance:
            line_1.append(boxes[i])
        else:
            line_2.append(boxes[i])

    sorted_line_1 = [x for x in sorted(line_1, key=lambda line_1: line_1[0])]
    if len(line_2) > 0:
        sorted_line_2 = [x for x in sorted(line_2, key=lambda line_2: line_2[0])]
    return sorted_line_1 + sorted_line_2


def segment_and_get_boxes(img, sample, textsize, margin=3):
    if type(textsize[0]).__name__ == 'tuple':
        tmp = list(textsize).copy()
        textsize = list(tmp[0])
        textsize[0] = textsize[0] + tmp[1][0]
    else:
        textsize = list(textsize)
    height, width, _ = img.shape
    gray = cv2.cvtColor(img.copy(), cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 19, 255, cv2.THRESH_BINARY_INV)
    contours, hier = cv2.findContours(thresh.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    list_box = []
    for i in range(len(contours)):
        x, y, w, h = cv2.boundingRect(contours[i])
        x += random.randint(-margin, 0)
        y += random.randint(-margin, 0)
        w += random.randint(0, 2 * margin)
        h += random.randint(0, 2 * margin)

        if h >= 0.95 * textsize[1] and h <= 1.05 * textsize[1]:
            list_box.append([x, y, (x + w), (y + h)])
    if len(list_box):
        list_box = nms_fast(list_box)
        list_box = format_boundingbox(list_box, width, height)
        sorted_list_box = sort_boxes(list_box)
        return sorted_list_box
    else:
        _, thresh = cv2.threshold(gray, 190, 255, cv2.THRESH_BINARY)
        contours, hier = cv2.findContours(thresh.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        list_box = []
        for i in range(len(contours)):
            x, y, w, h = cv2.boundingRect(contours[i])
            x += random.randint(-margin, 0)
            y += random.randint(-margin, 0)
            w += random.randint(0, 2 * margin)
            h += random.randint(0, 2 * margin)

            if h >= 0.95 * textsize[1] and h <= 1.05 * textsize[1]:
                list_box.append([x, y, (x + w), (y + h)])
        if len(list_box):
            list_box = nms_fast(list_box)
            list_box = format_boundingbox(list_box, width, height)
            sorted_list_box = sort_boxes(list_box)
            return sorted_list_box
        else:
            return list_box


def generate_sample(template):
    count_numb = template.count('N')
    count_char = template.count('C')
    for i in range(count_numb):
        idx_numb = random.randint(0, total_number - 1)
        template = template.replace('N', available_number[idx_numb], 1)
    for i in range(count_char):
        idx_char = random.randint(0, total_char - 1)
        while available_char[idx_char] == 'I' or available_char[idx_char] == 'J' or available_char[idx_char] == 'O' or \
                available_char[idx_char] == 'Q' or available_char[idx_char] == 'W':
            idx_char = random.randint(0, total_char - 1)

        template = template.replace('C', available_char[idx_char], 1)
    return template


def generate_plate(template):
    if '/' in template:
        idx = random.randint(0, len(available_square_bg) - 1)
        bg = available_square_bg[idx]
        print(f"template: {template}, idx: {idx}, bg: {bg}")
        print("*" * 20)
        return generate_2lines_images(template, bg), idx
    else:
        idx = random.randint(0, len(available_rec_bg) - 1)
        bg = available_rec_bg[idx]
        return generate_1lines_image(template, bg), idx


def generate_yolo_label(boxes, sample_formated, filename):
    # print(sample_formated)
    assert len(boxes) == len(sample_formated)
    filename_txt = filename.split('.')[0] + '.txt'
    # Delete current label file
    open(filename_txt, 'w+')
    # Write yolo label
    with open(filename_txt, 'a') as f:
        for i in range(len(boxes)):
            x, y, w, h = boxes[i]
            f.write('{} {} {} {} {}\n'.format(box_label[sample_formated[i]], x, y, w, h))


def generate_yolo_label_2(filename, idx_bg):
    with open(filename, 'w+') as f:
        if idx_bg != 0:
            idx_bg -= 1
        f.write(f"{idx_bg} 0.5 0.5 1.0 1.0")


def gen(start=0):
    err = 0
    for i in tqdm(range(int(args.numb))):
        try:
            # filename = os.path.join(args.output_dir, 'syn_{}.jpg'.format(int(start) + i))
            image_path = f"{args.output_dir}/images/{start + i}.jpg"
            label_path = f"{args.output_dir}/labels/{start + i}.txt"
            idx = random.randint(0, total_template - 1)
            template = available_template[idx]
            sample = generate_sample(template)  # gen digit
            (img, textsize), idx_bg = generate_plate(sample)
            print(idx_bg)
            img = augmention(img)
            width, height = img.size
            boxes = segment_and_get_boxes(np.array(img), sample, textsize)
            generate_yolo_label_2(label_path, idx_bg)
            img.save(image_path)
        except AssertionError:
            err += 1


thread_dict = {}
num_wokers = 5
for i in range(num_wokers):
    thread_dict[i] = Thread(target=gen, args=(i * args.numb,))

if __name__ == '__main__':
    for i in range(num_wokers):
        thread_dict[i].start()

    for i in range(num_wokers):
        thread_dict[i].join()
