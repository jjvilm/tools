#!/usr/bin/python2
from Tkinter import *
from PIL import Image
from PIL import ImageTk
import tkFileDialog
import time
import cv2
import numpy as np


once = True
img_screenshot = None

class App:
    
    def __init__(self, master):
        self.img_path = None
        frame = Frame(master)
        frame.grid()
        root.title("Sliders")

        self.hue_lbl = Label(text="Hue", fg='red')
        self.hue_lbl.grid(row=2)

        self.low_hue = Scale(master, label='Low',from_=0, to=179, length=500,orient=HORIZONTAL, command=self.show_changes)
        self.low_hue.grid(row=3)

        self.high_hue = Scale(master,label='High', from_=0, to=179, length=500,orient=HORIZONTAL, command=self.show_changes)
        self.high_hue.set(179)
        self.high_hue.grid(row=4)
###########################################################################################################
        self.sat_lbl = Label(text="Saturation", fg='green')
        self.sat_lbl.grid(row=5)

        self.low_sat = Scale(master, label='Low',from_=0, to=255, length=500,orient=HORIZONTAL, command=self.show_changes)
        self.low_sat.set(100)
        self.low_sat.grid(row=6)

        self.high_sat = Scale(master, label="High", from_=0, to=255, length=500,orient=HORIZONTAL, command=self.show_changes)
        self.high_sat.set(255)
        self.high_sat.grid(row=7)
###########################################################################################################
        self.val_lbl = Label(text="Value", fg='Blue')
        self.val_lbl.grid(row=8)

        self.low_val = Scale(master, label="Low",from_=0, to=255, length=500,orient=HORIZONTAL, command=self.show_changes)
        self.low_val.set(100)
        self.low_val.grid(row=9)

        self.high_val = Scale(master, label="High",from_=0, to=255, length=500,orient=HORIZONTAL, command=self.show_changes)
        self.high_val.set(255)
        self.high_val.grid(row=10)
###########################################################################################################
# buttons
        self.reset_btn = Button(text='Reset', command=self.reset_values)
        self.reset_btn.grid(row=1,column=1)

        self.print_btn = Button(text='Print', command=self.print_values)
        self.print_btn.grid(row=2, column=1)

        self.reds = Button(text="Reds", fg='red', command=self.preset_r)
        self.reds.grid(row=3, column=1)

        self.reds = Button(text="Greens", fg='green', command=self.preset_g)
        self.reds.grid(row=4, column=1)

        self.reds = Button(text="Blues", fg='blue', command=self.preset_b)
        self.reds.grid(row=5, column=1)

        # Open
        self.open_btn = Button(text="Open", command=self.open_file)
        self.open_btn.grid(row=6, column=1)

        # Screenshot
        self.screenshot_btn = Button(text="Screenshot", command=self.take_screenshot)
        self.screenshot_btn.grid(row=7, column=1)

##########################################################################################################
        self.hsv_img_lbl = Label(text="HSV", image=None)
        self.hsv_img_lbl.grid(row=0, column=0)

        self.original_img_lbl = Label(text='Original',image=None)
        self.original_img_lbl.grid(row=0, column=1)
##########################################################################################################
    def open_file(self):
        global once
        once = True
        img_file = tkFileDialog.askopenfilename()
        # this makes sure you select a file
        # otherwise program crashes if not
        if img_file  != '':
            self.img_path = img_file 
            # this just makes sure the image shows up after opening it
            self.low_hue.set(1)
            self.low_hue.set(0)
        else:
            print('picked nothing')
            return 0

    def preset_r(self, *args):
        self.low_hue.set(0)
        self.high_hue.set(10)

        self.low_sat.set(100)
        self.low_val.set(100)
        self.high_sat.set(255)
        self.high_val.set(255)
    def preset_g(self, *args):
        self.low_hue.set(50)
        self.high_hue.set(70)

        self.low_sat.set(100)
        self.high_sat.set(255)
        self.low_val.set(100)
        self.high_val.set(255)
    def preset_b(self, *args):
        self.low_hue.set(110)
        self.high_hue.set(130)

        self.low_sat.set(100)
        self.high_sat.set(255)
        self.low_val.set(100)
        self.high_val.set(255)

    def show_changes(self, *args):
        global once, img_screenshot

        if self.img_path == None:
            return 0

        # gets the values from the sliders
        # low blue, green, red
        low_hue = self.low_hue.get()
        low_sat = self.low_sat.get()
        low_val = self.low_val.get()
        # gets upper values from sliders
        high_hue = self.high_hue.get()
        high_sat = self.high_sat.get()
        high_val = self.high_val.get()

        if low_val > high_val or low_sat > high_sat or low_hue > high_hue:
            return 0

        # gets screenshot
        if self.img_path != 'screenshot':
            #img_path = 'objects.png'
            # loaded as BGR 
            img_a = cv2.imread(self.img_path,1)
            img_b = img_a.copy()
        else:
            img_a = img_screenshot
            img_b = img_screenshot.copy()

        if once: 
            # OpenCV represetns images in BGR order; however PIL represents
            # images in RGB order, so we need to swap the channels
            imgO = cv2.cvtColor(img_b, cv2.COLOR_BGR2RGB)
            
            # convert the images to PIL format
            imgO = Image.fromarray(imgO)
            # convert to ImageTk format
            imgO = ImageTk.PhotoImage(imgO)
            # update the original image label
            self.original_img_lbl.configure(image=imgO)
            # Keeping a reference! b/ need to! 
            self.original_img_lbl.image = imgO
            once = False


        
        #converts image to HSV 
        img = cv2.cvtColor(img_a, cv2.COLOR_BGR2HSV)
        #converts image to an array usable for open cv2
        #img = np.array(img)
        
        # sets the lower and uppper values for the mask
        # define range of colors in HSV (hue up to 179, sat-255, value-255
        lower_color = np.array([low_hue,low_sat,low_val]) 
        upper_color= np.array([high_hue,high_sat,high_val])
        # red - 0,255,255 (low (hue-10,100,100) high(hue+10,255,255)
        # green 60,255,255
        # blue -120,255,255

        #creates the mask and result
        mask = cv2.inRange(img, lower_color, upper_color)
        #res = cv2.bitwise_and(img, img, mask=mask)

        # converting to RGB format
        #maskbgr = cv2.cvtColor(mask, cv2.COLOR_HSV2BGR)
        #maskrgb = cv2.cvtColor(maskbgr, cv2.COLOR_BGR2RGB)
        # converting to PIL format
        mask_pil = Image.fromarray(mask)
        # convertint to ImageTk format
        mask_tk = ImageTk.PhotoImage(mask_pil)

        self.hsv_img_lbl.configure(image=mask_tk)
        # adding a reference to the image to Prevent python's garbage collection from deleting it
        self.hsv_img_lbl.image = mask_tk

    def reset_values(self):
        self.low_hue.set(0)
        self.low_sat.set(100)
        self.low_val.set(100)

        self.high_hue.set(179)
        self.high_sat.set(255)
        self.high_val.set(255)

    def print_values(self):
        """Does NOT actually save, just prints, for now"""
        print("Low = [{},{},{}]".format(self.low_hue.get(), self.low_sat.get(), self.low_val.get()))
        print("High= [{},{},{}]".format(self.high_hue.get(), self.high_sat.get(), self.high_val.get()))

    def take_screenshot(self):
        global img_screenshot
        from subprocess import check_output
        from pyscreenshot import grab

        
        # makes sure method 'show_changes' takes screenshot instead of img file
        self.img_path = 'screenshot'
        # initializes coords for screenshot
        x1 = None
        y1 = None
        x2 = None
        y2 = None
        
        for i in xrange(2):
            time.sleep(3)
            # Parses output for x and y coords
            coords = check_output(['xdotool','getmouselocation','--shell'])
            fo = coords.find("=")
            so = coords.find("Y")
            to = coords.find("S")

            if i == 0:
                x1 = int(coords[fo+1:so])
                y1 = int(coords[so+2:to])
            else:
                x2 = int(coords[fo+1:so])
                y2 = int(coords[so+2:to])
            print("Pic taken")

        screenshot = grab(bbox=(x1,y1,x2,y2))
        screenshot = np.array(screenshot)
        cv_img = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)

        img_screenshot = cv_img








root = Tk()
app = App(root)
root.mainloop()
