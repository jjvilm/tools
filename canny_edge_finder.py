#!/usr/bin/python2
#from Tkinter import *
import Tkinter as tk
from PIL import Image
from PIL import ImageTk
import tkFileDialog
import time
import cv2
import numpy as np
from subprocess import check_output
from pyscreenshot import grab
from threading import Thread, Lock

once = True
img_screenshot = None

class App:
    original_image = None
    hsv_image = None
    # switch to make sure screenshot not taken while already pressed
    taking_screenshot = False
    
    def __init__(self, master):
        self.img_path = None
        frame = tk.Frame(master)
        frame.grid()
        root.title("Sliders")

        self.hue_lbl = tk.Label(text="Threshold Values", fg='red')
        self.hue_lbl.grid(row=2)

        self.low_hue = tk.Scale(master, label='Low',from_=0, to=1000, length=1000,orient=tk.HORIZONTAL, command=self.show_changes)
        self.low_hue.grid(row=3)

        self.high_hue = tk.Scale(master,label='High', from_=0, to=1000, length=1000,orient=tk.HORIZONTAL, command=self.show_changes)
        self.high_hue.set(179)
        self.high_hue.grid(row=4)

###########################################################################################################
# buttons

        self.print_btn = tk.Button(text='Print', command=self.print_values)
        self.print_btn.grid(row=2, column=1)

        # Open
        self.open_btn = tk.Button(text="Open", command=self.open_file)
        self.open_btn.grid(row=6, column=1)

        # Screenshot
        self.screenshot_btn = tk.Button(text="Screenshot", command=self.screenshot_standby)
        self.screenshot_btn.grid(row=7, column=1)
        # print mask array
        self.print_mask_array_btn = tk.Button(text="Print Array", command=self.print_img_array)
        self.print_mask_array_btn.grid(row=9, column=1)
###########################################################################################################
        # timer label
        self.screenshot_timer_lbl = tk.Label(text="Timer", fg='Red')
        self.screenshot_timer_lbl.grid(row=8, column=1)

########################################################################################################## Images
        # images
        self.hsv_img_lbl = tk.Label(text="HSV", image=None)
        self.hsv_img_lbl.grid(row=0, column=0)

        self.original_img_lbl = tk.Label(text='Original',image=None)
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
            self.low_hue.set(self.low_hue.get()+1)
            self.low_hue.set(self.low_hue.get()-1)
        else:
            print('picked nothing')
            return 0

    def preset_r(self, *args):
        self.low_hue.set(0)
        self.high_hue.set(13)

        self.low_sat.set(100)
        self.high_sat.set(255)
        
        self.low_val.set(50)
        self.high_val.set(255)

    def preset_g(self, *args):
        self.low_hue.set(36)
        self.high_hue.set(90)

        self.low_sat.set(100)
        self.high_sat.set(255)

        self.low_val.set(50)
        self.high_val.set(255)

    def preset_b(self, *args):
        self.low_hue.set(80)
        self.high_hue.set(125)

        self.low_sat.set(100)
        self.high_sat.set(255)

        self.low_val.set(75)
        self.high_val.set(255)

    def show_changes(self, *args):
        global once, img_screenshot

        if self.img_path == None:
            return 0

        # gets the values from the sliders
        # low blue, green, red
        low_hue = self.low_hue.get()
        # gets upper values from sliders
        high_hue = self.high_hue.get()
        # does nothing if low values go higher than high values
        if  low_hue > high_hue:
            return 0

        # Sets the original image once, manipulates the copy in next iterations
        if once: 
            # gets image from file
            if self.img_path != 'screenshot':
                #img_path = 'objects.png'
                # loaded as BGR 
                self.original_image = cv2.imread(self.img_path,1)
                # image resized
                self.original_image = self.resize_image(self.original_image)
                self.hsv_image = self.original_image.copy()
                #converts image to HSV 
                self.hsv_image = cv2.cvtColor(self.hsv_image, cv2.COLOR_BGR2HSV)

            # gets screenshot
            else:
                self.original_image = img_screenshot
                self.hsv_image = img_screenshot.copy()
                #converts image to gray 
                self.hsv_image = cv2.cvtColor(self.hsv_image, cv2.COLOR_BGR2GRAY)

            # OpenCV represetns images in BGR order; however PIL represents
            # images in RGB order, so we need to swap the channels
            self.original_image = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2RGB)
            
            # convert the images to PIL format
            self.original_image = Image.fromarray(self.original_image)
            # convert to ImageTk format
            self.original_image = ImageTk.PhotoImage(self.original_image)
            # update the original image label
            self.original_img_lbl.configure(image=self.original_image)
            # Keeping a reference! b/ need to! 
            self.original_img_lbl.image = self.original_image
            once = False


        

        #creates the mask and result
        print("{} {}".format(self.low_hue.get(), self.high_hue.get()))
        low_val = self.low_hue.get()
        high_val = self.high_hue.get()
        mask = cv2.Canny(self.hsv_image, low_val, high_val)
        #res = cv2.bitwise_and(img, img, mask=mask)

        # converting to RGB format
        #maskbgr = cv2.cvtColor(mask, cv2.COLOR_HSV2BGR)
        #maskrgb = cv2.cvtColor(maskbgr, cv2.COLOR_BGR2RGB)
        # converting to PIL format
        mask = Image.fromarray(mask)
        # convertint to ImageTk format
        mask = ImageTk.PhotoImage(mask)
        # setting the hsv image to tk image label
        self.hsv_img_lbl.configure(image=mask)
        # adding a reference to the image to Prevent python's garbage collection from deleting it
        self.hsv_img_lbl.image = mask

    def reset_values(self,*args):
        self.low_hue.set(0)
        self.low_sat.set(100)
        self.low_val.set(100)

        self.high_hue.set(179)
        self.high_sat.set(255)
        self.high_val.set(255)

    def print_values(self,*args):
        """Does NOT actually save, just prints, for now"""
        print('\n')
        print("Low = [{},{},{}]".format(self.low_hue.get(), self.low_sat.get(), self.low_val.get()))
        print("High= [{},{},{}]".format(self.high_hue.get(), self.high_sat.get(), self.high_val.get()))
        print(self.hsv_img_lbl)
        print(self.hsv_img_lbl.image)
        #screen_width = root.winfo_screenwidth()
        #screen_height = root.winfo_screenheight()
        #print("Screen width:", screen_width)
        #print("Screen height:", screen_height)

    def screenshot_standby(self,*args):
        if not self.taking_screenshot:
            take_screenshot_thread = Thread(target=self.take_screenshot)
            take_screenshot_thread.start()
        else:
            return 0

    def take_screenshot(self,*args):
        global img_screenshot, once
        # switch to stop screenshot button from snaping a shot while snapping a shot
        self.taking_screenshot = True

        # switch to always display the screenshot as original everytime
        once = True

        # makes sure method 'show_changes' takes screenshot instead of img file
        self.img_path = 'screenshot'
        # initializes coords for screenshot
        x1 = None
        y1 = None
        x2 = None
        y2 = None
        
        # starts a cound down timer of 3 seconds, parallel to the for loop
        screenshot_timer_thread = Thread(target=self.screenshot_timer_lbl_update)
        screenshot_timer_thread.start()
        for i in xrange(2):
            for _ in xrange(3):
                time.sleep(1)
            # Parses output for x and y coords
            coords = check_output(['xdotool','getmouselocation','--shell'])
            fo = coords.find("=")
            so = coords.find("Y")
            to = coords.find("S")
           # sets the first point of screenshot 
            if i == 0:
                x1 = int(coords[fo+1:so])
                y1 = int(coords[so+2:to])
           # sets the second point of screenshot 
            else:
                x2 = int(coords[fo+1:so])
                y2 = int(coords[so+2:to])
        # screenshot taken here with the grabbed coordinates
        try:
            screenshot = grab(bbox=(x1,y1,x2,y2))
            screenshot = np.array(screenshot)
        except:
            print("Could not capture image")
            return
        # converts the PIL image format to opencv2 image format
        img_screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)
        # printing image array, by taking another screenshot and processing, effects will now show
        try:
            if args[0] == 'array':
                self.taking_screenshot = False
                return img_screenshot
        except:
            pass

        # resizes image if higher than 300px in width or height
        img_screenshot = self.resize_image(img_screenshot)

        # this just makes sure the image shows up after opening it
        self.low_hue.set(self.low_hue.get()+1)
        self.low_hue.set(self.low_hue.get()-1)
        # switch to allow for next screenshot
        self.taking_screenshot = False

    def screenshot_timer_lbl_update(self,*args):
        for _ in range(2):
            for i in range(3):
                self.screenshot_timer_lbl.config(text="{}".format(i+1))
                time.sleep(1)
        self.screenshot_timer_lbl.config(text="{}".format(" "))

    def resize_image(self,img,*args):
        # unpacks width, height
        height, width,_ = img.shape
        print("Original size: {} {}".format(width, height))
        count_times_resized = 0
        while width > 500 or height > 500:
        #if width > 300 or height > 300:
            # divides images WxH by half
            width = width / 2
            height = height /2
            count_times_resized += 1
        # prints x times resized to console
        if count_times_resized != 0:
            print("Resized {}x smaller, to: {} {}".format(count_times_resized*2,width, height))
        # makes sures image is not TOO small
        if width < 300 and height < 300:
            width = width * 2
            height = height * 2

        img = cv2.resize(img,(width,height))

        return img

    def print_img_array(self):
        img = self.take_screenshot('array')
        #converts image to HSV 
        img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        # gets the values from the sliders
        low_hue = self.low_hue.get()
        low_sat = self.low_sat.get()
        low_val = self.low_val.get()
        # gets upper values from sliders
        high_hue = self.high_hue.get()
        high_sat = self.high_sat.get()
        high_val = self.high_val.get()
        lower_color = np.array([low_hue,low_sat,low_val]) 
        upper_color= np.array([high_hue,high_sat,high_val])
        #creates the mask and result
        mask = cv2.inRange(self.hsv_image, lower_color, upper_color)
        mask = np.array(mask)
        mask.view


# Instance of Tkinter
root = tk.Tk()
# New tkinter instnace of app
app = App(root)
# loops over to keep window active
root.mainloop()
