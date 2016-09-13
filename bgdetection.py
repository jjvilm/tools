# Stream Video with OpenCV from an Android running IP Webcam (https://play.google.com/store/apps/details?id=com.pas.webcam)
# Code Adopted from http://stackoverflow.com/questions/21702477/how-to-parse-mjpeg-http-stream-from-ip-camera

import cv2
import urllib2
import numpy as np
import sys
import datetime
from os import system
import time 


#Define the codec and create VideoWriter object
#fourcc = cv2.cv.CV_FOURCC(*'DIVX')
#out = cv2.VideoWriter('output.mov',fourcc, 30.0, (320,240))

host = "192.168.1.157:8080"

if len(sys.argv)>1:
    host = sys.argv[1]

hoststr = 'http://' + host + '/video'
print 'Streaming ' + hoststr

stream=urllib2.urlopen(hoststr)

bytes=''
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))
fgbg = cv2.BackgroundSubtractorMOG()

counter = 0
while True:
    bytes+=stream.read(1024)
    a = bytes.find('\xff\xd8')
    b = bytes.find('\xff\xd9')
    if a!=-1 and b!=-1:
        jpg = bytes[a:b+2]
        bytes= bytes[b+2:]
        frame = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8),cv2.CV_LOAD_IMAGE_COLOR)

        # saving frame
        #out.write(frame)

        # crop top text off frame off
        frame_crop = frame[14::,:] # Crop from x, y, w, h -> 100, 200, 300, 400


        fgmask = fgbg.apply(frame_crop)
        fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)

        contours, _ = cv2.findContours(fgmask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for con in contours:
            if con == []:
                break
            else:
                cv2.imwrite('/home/jj/github/tools/imgs/{}.png'.format(datetime.datetime.now().strftime("%H:%M:%S.%f-%F")), frame)
            #print('Found a contour')

        # work on this 

        # flipping image
#        rows, cols,_ = i.shape
#        M = cv2.getRotationMatrix2D((cols/2,rows/2),270,1)
#        dst = cv2.warpAffine(i, M, (cols, rows))
#        cv2.imshow(hoststr,dst)
        # flipping image

        cv2.imshow(hoststr,fgmask)
        #cv2.imshow(hoststr,frame)
        if cv2.waitKey(1) ==27:
            exit(0)
            break
        #counter += 1
        #if counter == 20:
        #    break
            #exit(0)

#out.release()
cv2.destroyAllWindows()
print('done')

