#!/usr/bin/python

import cv2
import os
import time
import commands

switch = False

def get_dir_size(start_path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    print("Size of directory: {}".format((total_size/1024)/1024))
    time.sleep(.5)

folder_name = raw_input('Folder name: ')
folder = '/home/pi/sec-imgs/'+folder_name
get_dir_size(folder)
#frame = None

os.chdir(folder)
# sorted list by creation time 

imgs_list = commands.getstatusoutput("ls -ltr | awk '{print $9}'")
imgs_list = imgs_list[1].split('\n')

new_frame_from_slider = False

frame_selected = 0

def frame_selection():
    while True:
        frame_selected = raw_input("Start frame:\n")
        try:
            frame_selected = int(frame_selected)
            return frame_selected
        except:
            print("NOT AN INT\n")

def frame_slider(x):
    global frame_selected, new_frame_from_slider, switch
    c_frame = cv2.getTrackbarPos('Frames:', 'Frames-Control')
    frame_selected = c_frame
    new_frame_from_slider = True
    switch = True




def main():
    global frame_selected, imgs_list, new_frame_from_slider, switch

    cv2.namedWindow('Frames-Control')
    cv2.createTrackbar('Frames:', 'Frames-Control', 0, len(imgs_list)-1,frame_slider)

    while True:
        if frame_selected < 0:
            frame_selected = 0
        print('Frame_selected = {}'.format(frame_selected))

        for n_current_frame,i in enumerate(imgs_list[frame_selected:]):
           # Outputs frame to terminal
            print("Curr: {} Sel: {}".format(n_current_frame, frame_selected))
            print("Frame:{} ".format(n_current_frame+frame_selected))

            # skips first empty file
            if i == '':
                continue
            # if slider turns on switch then skip till new frame
            if switch:
                if n_current_frame == frame_selected:
                    switch = False
                else:
                    continue
            frame = cv2.imread(folder+"/"+i, -1)
            cv2.imshow("Frames-Control",frame)

            key = cv2.waitKey(33) & 0xFF

            if key == ord('q'):
                exit(0)
            if key == ord('p'):
                cv2.waitKey(0)
            if key == ord('f'):
                print("Max frame == {}".format(len(imgs_list)))
                frame_selected = frame_selection()
                break

            if new_frame_from_slider:
                new_frame_from_slider = False
                break
            time.sleep(.25)


main()
