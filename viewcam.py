#!/usr/bin/python2
# Stream Video with OpenCV from an Android running IP Webcam (https://play.google.com/store/apps/details?id=com.pas.webcam)
# Code Adopted from http://stackoverflow.com/questions/21702477/how-to-parse-mjpeg-http-stream-from-ip-camera

import cv2
import urllib2
import numpy as np
import sys
import threading
import time
import datetime
import Camara

# resized image percentage
size = 500

class Camara_obj(object):
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

    def resizeim(self,frame):
        r = float(size) / frame.shape[1]
        dim = (int(size), int(frame.shape[0] * r))
        resized = cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)
        return resized

    def view(self):
        while 1:
            try:
                if len(sys.argv)>1:
                    self.host = sys.argv[1]

                hoststr = 'http://' + self.host + '/video'
                print('Streaming ' + hoststr)

                stream=urllib2.urlopen(hoststr)
                break
            except:
                print("NO DATA FOR: {}".format(self.cam_name))
                return

        bytes=''
        while 1:
            start_time = datetime.datetime.now().strftime('%s')
            try:
                bytes+=stream.read(1024)
                a = bytes.find('\xff\xd8')
                b = bytes.find('\xff\xd9')
                if a!=-1 and b!=-1:
                    jpg = bytes[a:b+2]
                    bytes= bytes[b+2:]
                    # cv2 version 2
                    #i = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8),cv2.CV_LOAD_IMAGE_COLOR)
                    # cv2 version 3
                    i = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8),cv2.IMREAD_COLOR)

                    #print(i.shape)

#                    if self.cam_name == 'House':
#                        # flipping image
#                        rows, cols,_ = i.shape
#                        M = cv2.getRotationMatrix2D((cols/2,rows/2),90,1)
#                        dst = cv2.warpAffine(i, M, (cols, rows))
#                        #cv2.imshow(hoststr,dst)
#                        i = dst
#
#                    with self.turn_lock:
#                        cv2.imshow(self.cam_name,i)
#                        counter_for_frames += 1
#                        end_time = datetime.datetime.now().strftime('%s')

                    # crop top 
#                    i = i[25::,:] # crop from x,y, w,h 
                    # resized
#                    i = self.resizeim(i)

                    #####drawing contours for fun not part of code####
#                    imgray = cv2.cvtColor(i, cv2.COLOR_BGR2GRAY)
#                    ret, thresh = cv2.threshold(imgray, 150,255,0)
#                    _,contours , hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
#                    ih,iw,_ = i.shape
#                    # new image of same size but black
#                    i = np.zeros((ih,iw,3),np.uint8)
#
#                    cv2.drawContours(i, contours, -1, (255,255,255),1)

#                    imgray = cv2.cvtColor(i, cv2.COLOR_BGR2GRAY)
#
#                    ih,iw,_ = i.shape
#                    # new image of same size but black
#                    i = np.zeros((ih,iw,3),np.uint8)

                    # contours drawn by number of iterations
#                    counts = 100
#                    for _ in xrange(6):
#                        ret, thresh = cv2.threshold(imgray, counts,255,0)
#                        _,contours , hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
#
#                        cv2.drawContours(i, contours, -1, (255,255,255),1)
#                        counts += 25
                    ##############################################
                    ###########hsv applied#############
#                    i = cv2.cvtColor(i, cv2.COLOR_BGR2HSV)
#                    low = np.array([0,0,106])
#                    high = np.array([179,255,255])
#                    mask = cv2.inRange(i, low, high)
#                    i = mask
                    ###################################
                    



                    cv2.imshow(self.cam_name,i)

                    key = cv2.waitKey(33) & 0xFF

                    if key == ord('q'):
                        exit(0)
            except Exception as e:
                # if not data then break function ending thread
                print('exceptiong happend',e)
                return
                break

def view_all():
    cam1 = Camara_obj('Bedroom',"192.168.1.131:8080")
    cam2 = Camara_obj('House',"192.168.1.144:8080")
    cam3 = Camara_obj('Living Room',"192.168.1.129:8080")

def main():
    cams = Camara.InStore()
    # Prints the list of cams and it's corresponding index number
    for i,key in enumerate(cams.keys()):
        print("{} {}".format(i,key))

    # Get camara number
    while 1:
        try:
            answer = int(raw_input("Choose Camera:\n"))
            break
        except Exception as e:
            print("Not a number\n{}".format(e))

    if answer == 'All':
        cams['All']()
    else:
        for i, key in enumerate(cams.keys()):
            if i == answer:
                answer = key
                print(answer)
                break
        # runs the choses camara
        cam = Camara_obj(answer, cams[answer])
        cam.run_thread()


# dictionary of all the camaras
#cams = {
#'Bedroom':Camara_obj('Bedroom',"192.168.1.144:8080"),
#'House':Camara_obj('House',"192.168.0.107:8080"),
#'Living Room':Camara_obj('Living Room',"192.168.1.131:8080"),
#'lg':Camara_obj('LG','192.168.1.122:8080'),
#}

main()
