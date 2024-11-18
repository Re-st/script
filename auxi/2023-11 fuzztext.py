# -*- coding: utf-8 -*-
'''날짜 : 2023-10-27
제작이유 : 발표자료에 들어갈 애니메이션을 만들기 위해'''

import random as r
import string
import os
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, 'data')
OUTPUT_DIR = os.path.join(BASE_DIR, 'output')


def fuzz_string(s):
    """Fuzzing function that randomly changes the input string."""
    idx = r.randint(0, len(s) - 1)
    ch = r.choice(string.ascii_letters + string.digits + string.punctuation)
    if r.randint(0, 2) == 1:
        ch = chr(r.randint(0x4e00, 0x9fff))
    match r.randint(0, 10):
    # case 0:
    #     input_string = input_string[
    #         random_index + 1:] + random_char + input_string[:random_index]
        case 1:
            s = s[:idx] + ch + s[idx + 1:]
        case 2:
            s = s[:idx - r.randint(0, 3)] + s[idx + r.randint(0, 3):]
        case 3:
            s = s[:idx] + s[idx:]
        case 4:
            s = ch * r.randint(0, 2) + s
        case 5:
            s = s[idx + 1:] + s[:idx]
        case 6:
            s = s[idx:] + s[:idx]
        case 7:
            s = s[:idx] + ch + s[idx:]
    return s


INPUT = "입력값"
frames = []
predefined = [
    '입력값', '입력1값', '입결1값', '鳰결1값', '鳰헉1값', 'aaaa鳰헉1값', 'aa값aa鳰헉1', 'a驨값aa鳰헉1',
    'a驨값aa鳰1'
]

for i in range(100):
    if i < 9:
        INPUT = predefined[i]
    else:
        INPUT = fuzz_string(INPUT)
    print_value = INPUT + '을 계속 조금 바꿔 넣는다.'
    print(print_value, '  ', i)
    # Create a white background image
    img = Image.new('RGB', (800, 100), color='white')

    # Use a default font, you can specify your own font file
    custom_font_path = os.path.join(DATA_DIR, 'Hancom Gothic Regular.ttf')
    font = ImageFont.truetype(custom_font_path, size=40)
    draw = ImageDraw.Draw(img)

    text_color = (0, 0, 0)  # RGB color code for black
    text_color2 = (52, 87, 159)  # RGB color code for #34579F

    # # Calculate the text width
    # text_width, _ = draw.textsize(print_value, font=font)

    # Calculate the position for the second part (in black)
    x1 = len(INPUT)
    x2 = draw.textlength(INPUT, font=font) + 10
    # Draw the first part (in color)
    draw.text((10, 10), print_value[:x1], fill=text_color2, font=font)

    # Draw the second part (in black)
    draw.text((x2, 10), print_value[x1:], fill=text_color, font=font)

    frames.append(img)
    if i == 0:
        for _ in range(5):
            frames.append(img)

# Save the frames as a GIF
output_path = os.path.join(OUTPUT_DIR, 'fuzzed_text.gif')
frames[0].save(output_path,
               save_all=True,
               append_images=frames[1:],
               duration=200,
               loop=0)
