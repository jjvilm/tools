# Stream Video with OpenCV from an Android running IP Webcam (https://play.google.com/store/apps/details?id=com.pas.webcam)
# Code Adopted from http://stackoverflow.com/questions/21702477/how-to-parse-mjpeg-http-stream-from-ip-camera

import cv2
import urllib2
import numpy as np
import sys

host = "192.168.1.141:8080"
if len(sys.argv)>1:
    host = sys.argv[1]

hoststr = 'http://' + host + '/video'
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
#        M = cv2.getRotationMatrix2D((cols/2,rows/2),270,1)
#        dst = cv2.warpAffine(i, M, (cols, rows))
#        cv2.imshow(hoststr,dst)
        # flipping image

        cv2.imshow(hoststr,i)
        if cv2.waitKey(1) ==27:
            exit(0)


