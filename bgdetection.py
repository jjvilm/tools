# Stream Video with OpenCV from an Android running IP Webcam (https://play.google.com/store/apps/details?id=com.pas.webcam)
# Code Adopted from http://stackoverflow.com/questions/21702477/how-to-parse-mjpeg-http-stream-from-ip-camera

import cv2
import urllib2
import numpy as np
import sys

#Define the codec and create VideoWriter object
fourcc = cv2.cv.CV_FOURCC(*'mp4v')
out = cv2.VideoWriter('output.mp4',fourcc, 20.0, (640,480))

host = "192.168.1.141:8080"
if len(sys.argv)>1:
    host = sys.argv[1]

hoststr = 'http://' + host + '/video'
print 'Streaming ' + hoststr

stream=urllib2.urlopen(hoststr)

bytes=''
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))
fgbg = cv2.BackgroundSubtractorMOG()

while True:
    bytes+=stream.read(1024)
    a = bytes.find('\xff\xd8')
    b = bytes.find('\xff\xd9')
    if a!=-1 and b!=-1:
        jpg = bytes[a:b+2]
        bytes= bytes[b+2:]
        frame = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8),cv2.CV_LOAD_IMAGE_COLOR)

        # saving frame
        out.write(frame)

        #fgmask = fgbg.apply(frame)
        #fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)

        # flipping image
#        rows, cols,_ = i.shape
#        M = cv2.getRotationMatrix2D((cols/2,rows/2),270,1)
#        dst = cv2.warpAffine(i, M, (cols, rows))
#        cv2.imshow(hoststr,dst)
        # flipping image

        #cv2.imshow(hoststr,fgmask)
        cv2.imshow(hoststr,frame)
        if cv2.waitKey(1) ==27:
            break
            #exit(0)

out.release()
cv2.destroyAllWindows()
print('done')

