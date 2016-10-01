import cv2 
import urllib2
import numpy as np
import sys
import datetime
import time 
import os
import threading

class Cam(object):
    def __init__(self, cam_name, host):
        self.cam_name = cam_name 
        self.host = host

        object_thread = threading.Thread(target=self.run_motion_detection)
        object_thread.start()

    def run_motion_detection(self):

        if len(sys.argv)>1:
            self.host = sys.argv[1]

        hoststr = 'http://' + self.host + '/video'
        print 'Streaming ' + hoststr

        stream=urllib2.urlopen(hoststr)

        bytes=''
        firstFrame = None

        while True:
            bytes+=stream.read(1024)
            a = bytes.find('\xff\xd8')
            b = bytes.find('\xff\xd9')
            if a!=-1 and b!=-1:
                jpg = bytes[a:b+2]
                bytes= bytes[b+2:]
                frame = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8),cv2.CV_LOAD_IMAGE_COLOR)
                # crop top text off frame off
                frame_cropped = frame[:-16:,:] # Crop from x, y, w, h -> 100, 200, 300, 400

                gray = cv2.cvtColor(frame_cropped, cv2.COLOR_BGR2GRAY)
                gray = cv2.GaussianBlur(gray, (21, 21), 0)

                if firstFrame is None:
                    firstFrame = gray
                    continue

                # compute the absolute difference between the current frame and first frame
                frameDelta = cv2.absdiff(firstFrame, gray)
                thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]

                # dilate the thresholded image to fill in holes, then find contours on thresholded image
                thresh = cv2.dilate(thresh, None, iterations=2)

                #cv2.imshow(hoststr+'mask',thresh)
                #cv2.imshow(hoststr,frame)

                (cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

                if cnts != []:
                    try:
                        cv2.imwrite('/home/pi/sec-imgs/{}/{}.png'.format(self.cam_name, datetime.datetime.now().strftime("%H:%M:%S:%f")), frame)

                    except:
                        os.mkdir('/home/pi/sec-imgs/{}'.format(self.cam_name))
                        cv2.imwrite('/home/pi/sec-imgs/{}/{}.png'.format(self.cam_name, datetime.datetime.now().strftime("%H:%M:%S:%f")), frame)

                    #time.sleep(1)
                    firstFrame = None
                    continue


                firstFrame = None

camA = Cam("Living Room", "192.168.1.129:8080")
camB = Cam("Bedroom", "192.168.1.131:8080")
camC = Cam("House", "192.168.1.144:8080")
