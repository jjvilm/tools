#!/usr/bin/python
import cv2
import os
import time
import commands

# switch to iterate to equal frame n 
switch = False
# Global variable to control speed of frames
frame_speed = 0.30 # .3 normilizes time
# global variable for max frames
t_n_frames = 0
# exit switch for empty directory
exit_switch = False

def get_dir_size(start_path):
    global t_n_frames
    total_size = 0
    counter = 0 
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
            counter += 1
    t_n_frames = counter - 1
    print("Size of directory: {:.2f}MB\nFrames: {}\n".format((total_size/1024.0)/1024.0, t_n_frames))
    raw_input()
    if total_size <= 0:
        return True
    return False

#folder_name = raw_input('Folder name: ')
folder = 'sec-imgs'
# exit if directory is empty
if get_dir_size(folder):
    exit_switch = True


#creates above folder if it does not exist
if not os.path.exists(folder):
	print('{} created!'.format(folder))
	os.makedirs(folder)

os.chdir(folder)

# sorted list by creation time 
imgs_list = commands.getstatusoutput("ls -ltr | awk '{print $9}'")
imgs_list = imgs_list[1].split('\n')
#print(imgs_list)


new_frame_from_slider = False

frame_selected = 0

def frame_selection():
    global t_n_frames
    while True:
        frame_selected = raw_input("Start frame:\n")
        if frame_selected == 'q':
            return
        try:
            frame_selected = int(frame_selected)
            if frame_selected > t_n_frames:
                print('Frame out of range')
                continue
            return frame_selected
        except:
            print("NOT AN INT\n")

def frame_slider(x):
    global frame_selected, new_frame_from_slider, switch
    c_frame = cv2.getTrackbarPos('Frames:', 'Frames-Control')
    frame_selected = c_frame
    new_frame_from_slider = True
    switch = True

def set_frame_speed(x):
    global frame_speed
    slider_speed = cv2.getTrackbarPos('Speed','Frames-Control')
    speeds = {
            0: 0,
            1: .005,
            2: .015,
            3: .025,
            4: .050,
            5: .075,
            6: .1,
            7: .3,
            8: .5,
            9: .9,
            10: 1
            }
    frame_speed = speeds[slider_speed]

def frame_by_frame(current_frame_n):
    global imgs_list, folder
    once = True
    # initialize frame to avoid crash when frame > max frames or < current frame
    frame = None
    while True:
        if once:
            image_file_path = imgs_list[current_frame_n]
            frame = cv2.imread(image_file_path)
            once = False
        # resizes 400% on frame by frame
        frame = resize(frame)
        cv2.imshow("Frames", frame)

        key = cv2.waitKey(33) & 0xFF
       
        # forward
        if key == ord('.'):
            if current_frame_n  < t_n_frames:
                current_frame_n += 1
                once = True
            else:
                current_frame_n = 1
                once = True

        # backward
        if key == ord(','):
            if current_frame_n >= 2:
                current_frame_n -= 1
                once = True
            else:
                current_frame_n = t_n_frames
                once = True
        if key == ord('/'):
            return current_frame_n

def resize(frame):
    r = 400.0 / frame.shape[1]
    dim = (400 , int(frame.shape[0] * r))
    resized = cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)
    return resized

def main():
    global exit_switch
    # does not run main if folder is empty size is <= 0
    if exit_switch:
        return

    # window for slider
    #cv2.namedWindow('Frames-Control')
    # Slider for frame tuning
    #cv2.createTrackbar('Frames:', 'Frames-Control', 0, len(imgs_list)-1,frame_slider)
    # Speed slider
    #cv2.createTrackbar('Speed','Frames-Control',0,10, set_frame_speed)

    def main_loop():
        global frame_selected, imgs_list, new_frame_from_slider, switch, frame_speed, exit_switch

        while True:
            if frame_selected < 0:
                frame_selected = 1
            #print('Frame_selected = {}'.format(frame_selected))

            for n_current_frame,i in enumerate(imgs_list[frame_selected:]):
                # reverts back to original with same frame
                if n_current_frame < frame_selected:
                    continue
               # Outputs frame to terminal
                #print("Curr: {} Sel: {}".format(n_current_frame, frame_selected))
                #print("Frame:{} ".format(n_current_frame))

                # skips first empty file
                if i == '':
                    continue
                # if slider turns on switch then skip till new frame
                if switch:
                    if n_current_frame == frame_selected:
                        switch = False
                    else:
                        continue
                # Sometimes imshow crashes on this line while 
                # reading image file
                try:
                    frame = cv2.imread(i, -1)
                    cv2.imshow("Frames",frame)
                except Exception as e:
                    print(e,'\nBAD Frame')
                    continue

                key = cv2.waitKey(33) & 0xFF

                if key == ord('q'):
                    exit_switch = 1
                    exit(0)
                    return
                if key == ord('p'):
                    cv2.waitKey(0)
                # Increases speed
                if key == ord('>'):
                    if frame_speed != 0 and frame_speed >= .005:
                        frame_speed -= .005
                    print('Frame speed changed to {}'.format(frame_speed))
                # Decrases frame play
                if key == ord('<'):
                    frame_speed += .005
                    print('Frame speed changed to {}'.format(frame_speed))
                # Normal Speed
                if key == ord('/'):
                    frame_speed  = 0
                    print('Frame speed changed to {}'.format(frame_speed))
                # Frame selection prompt
                if key == ord('f'):
                    print("Max frame == {}".format(len(imgs_list)))
                    frame_selected = frame_selection()
                    break
                # Frame by frame paused
                if key == ord('.'):
                    #frame_selected = frame_by_frame(frame_selected)
                    # goes into a loop that pauses frames
                    frame_selected = frame_by_frame(n_current_frame)
                # skips by 100 frames
                if key == ord('='):
                    if (frame_selected+n_current_frame+200) < t_n_frames:
                        frame_selected += 100 
                        break
                # backwards by 100 frames
                if key == ord('-'):
                    frame_selected -= 100 
                    break

                #print("Frame speed: {}".format(frame_speed))
                time.sleep(frame_speed)
                if new_frame_from_slider:
                    #new_frame_from_slider = False
                    break
            else:
                # frames end here so restart loop
                print('Looping...')
                frame_selected = 0

    while 1:
        try:
            main_loop()
        
        except Exception as e:
            print('major exception',e)
            continue
    

main()
