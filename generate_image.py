from PIL import Image, ImageFont, ImageDraw
import numpy as np


def generate_1lines_image(template, bg='background/bg1.jpg'):
    font = ImageFont.truetype("Font_xe_moi.otf", 108)
    if type(bg).__name__ == 'str':
        im = Image.open(bg)
    else:
        im = bg
    if len(template.replace('-', '').replace('.', '')) > 7:
        im = im.resize((450, 110))
    else:
        im = im.resize((400, 110))
    width, height = im.size
    draw = ImageDraw.Draw(im)
    textsize = font.getsize(template)
    textX = int((width - textsize[0]) / 2)
    textY = int((height - textsize[1]) / 2)
    if (bg.find("_4.jpg") != -1) or (bg.find("_5.jpg") != -1):
        # fill = tuple([np.random.randint(254, 255), np.random.randint(254, 255), np.random.randint(254, 255)])
        fill = (255, 255, 255)
        draw.text((textX, textY), template, font=font, fill=fill)
    else:
        fill = tuple(np.random.randint(20, size=3))
        draw.text((textX, textY), template, font=font, fill=fill)

    return im, textsize


def generate_2lines_images(template, bg='background/bg2.jpg', margin=10, size=(480, 400)):
    font = ImageFont.truetype("Font_xe_moi.otf", 180)
    if type(bg).__name__ == 'str':
        im = Image.open(bg)
    else:
        im = bg
    im = Image.open(bg)
    im = im.resize(size)
    width, height = im.size
    draw = ImageDraw.Draw(im)
    line_1, line_2 = template.split('/')

    textsize1 = font.getsize(line_1)
    textX1 = int((width - textsize1[0]) / 2)
    textY1 = int((height / 2 - textsize1[1]) / 2) + margin
    textsize2 = font.getsize(line_2)
    textX2 = int((width - textsize2[0]) / 2)
    textY2 = int(height / 2 + (height / 2 - textsize2[1]) / 2) - margin / 2
    fill = tuple(np.random.randint(20, size=3))

    shadow = tuple(np.random.randint(200, 255, size=3))

    if (bg.find("_4.jpg") != -1) or (bg.find("_5.jpg") != -1):
        fill = tuple([np.random.randint(200, 255), np.random.randint(200, 255), np.random.randint(200, 255)])

    shadow = tuple(np.random.randint(0, 68, size=3))

    direction = tuple(np.random.randint(-3, 3, size=2))

    # Add drop shadow line 1
    draw.text((textX1 + direction[0], textY1 + direction[1]), line_1, font=font, fill=shadow)
    draw.text((textX1, textY1), line_1, font=font, fill=fill)

    # Add drop shadow line 2
    draw.text((textX2 + direction[0], textY2 + direction[1]), line_2, font=font, fill=shadow)
    draw.text((textX2, textY2), line_2, font=font, fill=fill)

    return im, (textsize1, textsize2)
