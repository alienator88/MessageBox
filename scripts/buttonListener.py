from customWaveshare import *
from time import sleep
from signal import pause
import sys, os, subprocess
sys.path.insert(1, "../lib")
from gpiozero import Button
from customWaveshare import *

btn = Button(5)
btn2 = Button(6)
btn3 = Button(13)
btn4 = Button(19)
unread = True
print("Button listener running..")

def handleBtnPress():
    global unread
    unread = False
    subprocess.run(["python", "displayMessage.py"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
def handleBtnPress2():
    global unread
    unread = False
    subprocess.run(["python", "displayQuote.py"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def handleBtnPress3():
    global unread
    unread = False
    subprocess.run(["python", "sleepScreen.py"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    
def handleBtnPress4():
    global unread
    unread = False
    print("4")

button_handlers = {
    btn: handleBtnPress,
    btn2: handleBtnPress2,
    btn3: handleBtnPress3,
    btn4: handleBtnPress4,
}

try:
    while True:
        for button, handler in button_handlers.items():
            if button.is_pressed:
                handler()
        sleep(0.1)

except KeyboardInterrupt:
    pass
finally:
    pass
# while unread is not False:
#     # os.system("echo running")
#     btn.when_pressed = handleBtnPress
#     btn2.when_pressed = handleBtnPress2
#     btn3.when_pressed = handleBtnPress3
#     btn4.when_pressed = handleBtnPress4

