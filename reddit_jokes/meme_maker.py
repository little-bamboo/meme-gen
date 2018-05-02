from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
import requests
from StringIO import StringIO


import textwrap
import base64

import re


class MemeGenerator(object):

    def __init__(self):
        self.meme_creating = False

    def slugify(self, text):
        text = text.encode('utf-8').lower().rstrip('?')
        print text
        return re.sub(r'\W+', '-', text)

    def make_meme(self, top_string, bottom_string, file_object):
        image_file_object = requests.get(file_object['image'], stream=True, verify=True)
        img = Image.open(StringIO(image_file_object.content))
        image_size = img.size

        # find biggest font size that works
        font_size = int(image_size[1] / 8)
        font = ImageFont.truetype("/Library/Fonts/Impact.ttf", font_size)

        top_lines = textwrap.wrap(top_string, width=image_size[1])
        bottom_lines = textwrap.wrap(bottom_string, width=image_size[1])

        top_text_size = font.getsize(top_lines[0])
        bottom_text_size = font.getsize(bottom_lines[0])

        while top_text_size[0] > image_size[0] - 20 or bottom_text_size[0] > image_size[0] - 20:
            font_size = font_size - 1
            font = ImageFont.truetype("/Library/Fonts/Impact.ttf", font_size)
            top_text_size = font.getsize(top_string)
            bottom_text_size = font.getsize(bottom_string)

        # find top centered position for top text
        top_text_position_x = (image_size[0] / 2) - (top_text_size[0] / 2)
        top_text_position_y = 0
        top_text_position = (top_text_position_x, top_text_position_y)

        # find bottom centered position for bottom text
        bottom_text_position_x = (image_size[0] / 2) - (bottom_text_size[0] / 2)
        bottom_text_position_y = image_size[1] - bottom_text_size[1]
        bottom_text_position = (bottom_text_position_x, bottom_text_position_y)

        draw = ImageDraw.Draw(img)

        # draw outlines
        # there may be a better way
        outline_range = int(font_size / 15)
        for x in range(-outline_range, outline_range + 1):
            for y in range(-outline_range, outline_range + 1):
                draw.text((top_text_position[0] + x, top_text_position[1] + y), top_string, (0, 0, 0), font=font)
                draw.text((bottom_text_position[0] + x, bottom_text_position[1] + y), bottom_string, (0, 0, 0),
                          font=font)

        for line in top_lines:
            draw.text(top_text_position, line, (255, 255, 255), font=font)

        for line in bottom_lines:
            draw.text(bottom_text_position, line, (255, 255, 255), font=font)
        file_name = self.slugify(top_lines[0])
        file_name = file_name + '.' + img.format.lower()
        print file_name
        path = '../uploads/auto-memes/'
        img.save(path+file_name, img.format)
        return img
