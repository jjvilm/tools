import os
import time

os.system('xdotool search --name ~/github/tools windowsize 145 98')

while True:
    os.system('clear')
    os.system('xdotool getmouselocation --shell')
    time.sleep(1)
