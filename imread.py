import cv2
import os
import time
import commands

folder_name = raw_input('Folder name: ')
folder = '/home/pi/sec-imgs/'+folder_name
#frame = None

os.chdir(folder)
# sorted list by creation time
# from Descending order
imgs_list = commands.getstatusoutput("ls -ltr | awk '{print $9}'")
imgs_list = imgs_list[1].split('\n')

while True:
    imgs_list = commands.getstatusoutput("ls -ltr | awk '{print $9}'")
    imgs_list = imgs_list[1].split('\n')
    for i in imgs_list:
        if i == '':
            continue
        frame = cv2.imread(folder+"/"+i,-1)
        cv2.imshow("image",frame)
        cv2.waitKey(0)



index = 0
#while True:
#    for n,i in enumerate(imgs_list):
#        if i == '':
#            continue
##        frame = cv2.imread(folder+"/"+i,-1)
#        cv2.imshow("image",frame)
        #if index == n:
        #    break
        #if index == len(os.listdir(folder))+1:
        #    index = 0
        #    break
        

    #time.sleep(.1)
    #index += 1

#    if cv2.waitKey(1) == 27:
#        exit(0)
