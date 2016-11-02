#!/usr/bin/python
# Stream Video with OpenCV from an Android running IP Webcam (https://play.google.com/store/apps/details?id=com.pas.webcam)
# Code Adopted from http://stackoverflow.com/questions/21702477/how-to-parse-mjpeg-http-stream-from-ip-camera

import cv2
import urllib2
import numpy as np
import sys
import threading
import time
import datetime

class Cam(object):
    turn_lock = threading.Lock()
    def __init__(self, cam_name, host):
        self.cam_name = cam_name
        self.host = host

    def run_thread(self):
        with self.turn_lock:
            cam_thread = threading.Thread(target=self.view)
            cam_thread.start()
    def ping_cam():
        # will bring up a back online cam
        # after exception in self.view()
        pass
    def view(self):
        while True:
            try:
                if len(sys.argv)>1:
                    self.host = sys.argv[1]

                hoststr = 'http://' + self.host + '/video'
                print 'Streaming ' + hoststr

                stream=urllib2.urlopen(hoststr)
                break
            except:
                print("NO DATA FOR: {}".format(self.cam_name))
                return

        bytes=''
        counter_for_frames = 0
        while True:
            start_time = datetime.datetime.now().strftime('%s')
            try:
                bytes+=stream.read(1024)
                a = bytes.find('\xff\xd8')
                b = bytes.find('\xff\xd9')
                if a!=-1 and b!=-1:
                    jpg = bytes[a:b+2]
                    bytes= bytes[b+2:]
                    i = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8),cv2.CV_LOAD_IMAGE_COLOR)

                    if self.cam_name == 'House':
                        # flipping image
                        rows, cols,_ = i.shape
                        M = cv2.getRotationMatrix2D((cols/2,rows/2),90,1)
                        dst = cv2.warpAffine(i, M, (cols, rows))
                        #cv2.imshow(hoststr,dst)
                        i = dst
                        # flipping image

#                    with self.turn_lock:
#                        cv2.imshow(self.cam_name,i)
#                        counter_for_frames += 1
#                        end_time = datetime.datetime.now().strftime('%s')

                    cv2.imshow(self.cam_name,i)
                    counter_for_frames += 1
                    end_time = datetime.datetime.now().strftime('%s')
                    # checks if 1 sec has passed, then shows counter
                    if int(end_time) - int(start_time) >= 1:
                        print(counter)
                        counter = 0
                    key = cv2.waitKey(33) & 0xFF
                    if key == ord('q'):
                        exit(0)
            except:
                # if not data then break function ending thread
                print('exceptiong happend')
                #break
                continue

            
def view_all():
    cam1 = Cam('Bedroom',"192.168.1.131:8080")
    cam2 = Cam('House',"192.168.1.144:8080")
    cam3 = Cam('Living Room',"192.168.1.129:8080")

cams = {
'Bedroom':Cam('Bedroom',"192.168.1.131:8080"),
'House':Cam('House',"192.168.1.144:8080"),
'Living Room':Cam('Living Room',"192.168.1.129:8080"),
'All':view_all
}

for key in cams.keys():
    print("{}".format(key))
answer = raw_input("Choose Camera:\n")
if answer == 'All':
    cams['All']()
else:
    cams[answer].run_thread()

