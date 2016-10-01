#!/usr/bin/python
# Stream Video with OpenCV from an Android running IP Webcam (https://play.google.com/store/apps/details?id=com.pas.webcam)
# Code Adopted from http://stackoverflow.com/questions/21702477/how-to-parse-mjpeg-http-stream-from-ip-camera

import cv2
import urllib2
import numpy as np
import sys
import threading

class Cam(object):
    def __init__(self, cam_name, host):
        self.cam_name = cam_name
        self.host = host

    def run_thread(self):
        cam_thread = threading.Thread(target=self.view)
        cam_thread.start()
    def view(self):
        if len(sys.argv)>1:
            self.host = sys.argv[1]

        hoststr = 'http://' + self.host + '/video'
        print 'Streaming ' + hoststr

        stream=urllib2.urlopen(hoststr)

        bytes=''
        while True:
            bytes+=stream.read(1024)
            a = bytes.find('\xff\xd8')
            b = bytes.find('\xff\xd9')
            if a!=-1 and b!=-1:
                jpg = bytes[a:b+2]
                bytes= bytes[b+2:]
                i = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8),cv2.CV_LOAD_IMAGE_COLOR)

                # flipping image
        #        rows, cols,_ = i.shape
        #        M = cv2.getRotationMatrix2D((cols/2,rows/2),180,1)
        #        dst = cv2.warpAffine(i, M, (cols, rows))
        #        cv2.imshow(hoststr,dst)
                # flipping image

                cv2.imshow(self.cam_name,i)
                key = cv2.waitKey(33) & 0xFF
                if key == ord('q'):
                    exit(0)
def view_all():
    cam1 = Cam('Bedroom',"192.168.1.131:8080")
    cam2 = Cam('House',"192.168.1.144:8080")
    cam3 = Cam('Living Room',"192.168.1.129:8080")

    cam1.run_thread()
    cam2.run_thread()
    cam3.run_thread()


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

