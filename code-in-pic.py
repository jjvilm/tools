import cv2
import numpy as np
import binascii 

def enc_img(binaryMessage):
    """Goes through each element of an the image array to replace the first element of the RGB value"""
    binaryMessage = binaryMessage[2:]

    #############################################
    #### Test purposes
    #print(binaryMessage)
    print("Length of message: {}".format(len(binaryMessage)))
    print(img.shape)
    ###################################################

    row = 0
    index = 0
    write = 0

    while True:
        if write == len(binaryMessage):
            break
        # last element in the first row of last col
        if index == img.shape[1]-1:
            #print("New row!")
            row += 1
            index = 0
        else:
            # encodes here
            img[row][index][0] = binaryMessage[write]
            index += 1
            write += 1

def dec_img(img):
    """Decodes a coded image"""
    binaryMessage = ''
    row = 0
    index = 0

    while True:
        # starts from top-right moves it's way down
        element = img[row][index][0]
        if index == img.shape[1]-1:
            row += 1
            index = 0
        else:
            if element == 0 or element == 1:
                binaryMessage += str(element)
                index += 1
            else:
                break


    #print(binaryMessage)
    binaryMessage = decode(binaryMessage)
    print(binaryMessage)

def encode():
    """adds: 0b to the beginning, needs to be stripped off when encoding to image, then put 
    back in when decoding from image"""
    message = raw_input("Message:\n")
    x = bin(int(binascii.hexlify('{}'.format(message)), 16))
    return x

def decode(message):
    """Takes a string of 0s and 1s and converts to ascii.  '0b' needs to be the first 2 chars"""
    # adds '0b' back into the binary message
    message = "0b"+message
    x = int('{}'.format(message), 2)
    x = binascii.unhexlify('%x' % x)
    return x

def get_image():
    #img = raw_input("Full path of image:\n")
    img = '/home/jj/github/elmacro/screenshot.png'
    img = cv2.imread(img)
    return img

img = get_image()
message = encode()
enc_img(message)

dec_img(img)

cv2.imshow('Secret Embedded Message in Image', img)
cv2.waitKey(0)
