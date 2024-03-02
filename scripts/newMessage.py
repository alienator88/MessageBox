#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys, os
from PIL import Image,ImageDraw,ImageFont
from datetime import datetime

picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

import epd2in7_V2

epd = epd2in7_V2.EPD()
current_datetime = datetime.now()
formatted_datetime = current_datetime.strftime("%b %dth at %I:%M %p")

def newMessageScreen():
    try:
        font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
        font18 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18)
        epd.init_Fast()
        # epd.init()
        epd.Clear()
        # Drawing on the Horizontal image
        Himage = Image.new('1', (epd.height, epd.width), 255)
        draw = ImageDraw.Draw(Himage)
        # draw.line((0, 10, 50, 10), fill = 0) # line pointing at 1st button
        # draw.text((60, 0), "VIEW", font = font18, fill = 0) # text after the line
        
        x_start = 30
        y = 5
        box_size = 20
        spacing = 5
        labels = ["View", "Quote", "Sleep", "N/A"]
        
        for i in range(4):
            # Draw the box
            draw.rectangle([(x_start, y), (x_start + box_size, y + box_size)], outline="black", width=2)

            # Set font properties for numbers
            font_size = 20
            font = ImageFont.load_default()

            # Get text size to center the number
            text_width, text_height = draw.textsize(str(i + 1), font=font)

            # Calculate text position to center it in the box
            text_x = x_start + (box_size - text_width) // 2
            text_y = y + (box_size - text_height) // 2

            # Draw the number inside the box
            draw.text((text_x, text_y), str(i + 1), fill="black", font=font)

            # Set font properties for labels
            label_font_size = 18
            label_font = ImageFont.load_default()

            # Get text size for labels
            label_width, label_height = draw.textsize(labels[i], font=label_font)

            # Calculate text position for labels
            label_x = x_start + box_size + spacing
            label_y = y + (box_size - label_height) // 2

            # Draw the label to the right of the box
            draw.text((label_x, label_y), labels[i], fill="black", font=label_font)

            # Move to the next box
            x_start += box_size + spacing + label_width + spacing
        
        draw.text((10, 0), "\n\n       NEW MESSAGE\n          FROM ALIN", font = font24, fill = 0)
        draw.text((0, 150), f"Received: {formatted_datetime}", font = font18, fill = 0) # timestamp
        epd.display(epd.getbuffer(Himage))
        epd.sleep()
    
    except IOError as e:
        print(e)
    
    except KeyboardInterrupt:    
        print("ctrl + c:")
        epd2in7_V2.epdconfig.module_exit(cleanup=True)
        exit()

newMessageScreen()
# os.system("python buttonListener.py")

    