""" 
@Author: Coralie Grobel, Clément Chaffard, David Roch
@Date: 23.12.2021
@Description : This file contains the live stream functionnality.
"""
from body_parts_temperature import main
from create_parser import create_parser
import numpy as np
import cv2
from PIL import Image

args = create_parser()
# modify the parser here to modify the parameter that will be used in body_parts_temperature.py
args.model = 'shufflenetv2k16' # fastest model used
args.body_parts = ["nose", "forehead"]

# cv2 parameter
f = cv2.FONT_HERSHEY_SIMPLEX
col = (255,0,0)

vid_capture = cv2.VideoCapture(0)
#vid_capture.set(cv2.CAP_PROP_BUFFERSIZE, 0)
while(vid_capture.isOpened()):
    # vCapture.read() methods returns a tuple, first element is a bool
    # and the second is frame
    ret, frame = vid_capture.read()
    if ret == True:
        images_name, images, thermal_matrices, body_parts, body_parts_pos, body_parts_temps = \
                        main(args, Image.fromarray(frame), frame[:,:,0])
        im = np.array(images[0])
        # add the body parts and their temperatures to the image
        for human in range(len(body_parts_pos[0])):
            for body_part in range(len(body_parts_pos[0][human])):
                if body_parts_pos[0][human][body_part] != (0,0):
                    pos = (body_parts_pos[0][human][body_part][1],body_parts_pos[0][human][body_part][0])
                    im = cv2.circle(im, pos, radius = 2, color = col, thickness = 2)
                    im = cv2.putText(im, str(body_parts_temps[0][human][body_part]), pos,
                                        f, 1, col, 3, cv2.LINE_AA)
        
        cv2.imshow('Frame',im)
        k = cv2.waitKey(20)
        # press q to stop the stream
        if k == 113:
            vid_capture.release()
            cv2.destroyAllWindows() 
            break
    else:
        break