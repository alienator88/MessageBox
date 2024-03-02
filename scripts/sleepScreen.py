#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys, os
from PIL import Image,ImageDraw,ImageFont

picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

import epd2in7_V2

epd = epd2in7_V2.EPD()

def sleepScreen():
    try:
        epd.init()
        epd.Clear()
        epd.sleep()
    
    except IOError as e:
        print(e)
    
    except KeyboardInterrupt:    
        print("ctrl + c:")
        epd2in7_V2.epdconfig.module_exit(cleanup=True)
        exit()

sleepScreen()    