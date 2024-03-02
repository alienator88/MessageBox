#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys, os, logging
from PIL import Image,ImageDraw,ImageFont

picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

import epd2in7_V2
# logging.basicConfig(level=logging.DEBUG)
epd = epd2in7_V2.EPD()

def displayOnScreen(resp):
    try:
        print("Starting screen render")
        epd.init()
        epd.Clear()

        font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
        x = 0
        y = 0
        line_height = font24.getsize('hg')[1] # How tall each line is using the specified font
        max_width = epd.height - x # Minux the x axis padding here to match it on the right side
        Himage = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame
        draw = ImageDraw.Draw(Himage)
        lines = text_wrap(resp, font24, max_width)

        for line in lines:
            draw.text((x,y), line, font = font24, fill = 0) # Write a line
            y = y + line_height # Move to next line down on y axis
        epd.display(epd.getbuffer(Himage))
        print("Screen sleep")
        epd.sleep()
    except IOError as e:
        print(e)
    
    except KeyboardInterrupt:    
        print("ctrl + c:")
        epd2in7_V2.epdconfig.module_exit(cleanup=True)
        exit()





def text_wrap(text, font, max_width):
    lines = []

    if font.getsize(text)[0] <= max_width:
        lines.append(text)
    else:
        words = text.split(' ')
        line = words[0]

        for word in words[1:]:
            if font.getsize(line + ' ' + word)[0] <= max_width:
                line += ' ' + word
            else:
                lines.append(line)
                line = word

        if line:
            lines.append(line)

    return lines




### Unused functions ###

# char_width = epd.height // font24.getsize("A")[0]

# def text_wrap2(text, font, max_width):
#         lines = []
#         if font.getsize(text)[0]  <= max_width:
#             lines.append(text)
#         else:
#             words = text.split(' ')
#             i = 0
#             while i < len(words):
#                 line = ''
#                 while i < len(words) and font.getsize(line + words[i])[0] <= max_width:
#                     line = line + words[i]+ " "
#                     i += 1
#                 if not line:
#                     line = words[i]
#                     i += 1
#                 lines.append(line)
#         return lines
    
    
# def char_wrap(text, font, max_width):
#     lines = []

#     if font.getsize(text)[0] <= max_width:
#         lines.append(text)
#     else:
#         i = 0
#         while i < len(text):
#             line = ''
#             while i < len(text) and font.getsize(line + text[i])[0] <= max_width:
#                 line = line + text[i]
#                 i += 1
#             lines.append(line)

#     return lines



# def displayOnScreen2(resp):
#     font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
#     print("Screen displaying: " + resp)
#     epd.init()
#     epd.Clear()
#     # Drawing on the Horizontal image
#     Himage = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame
#     draw = ImageDraw.Draw(Himage)
#     draw.text((10, 0), resp, font = font24, fill = 0)
#     epd.display(epd.getbuffer(Himage))
#     logging.info("Goto Sleep...")
#     epd.sleep()