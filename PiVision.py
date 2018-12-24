#! /usr/bin/python3

import cv2
import numpy as np
from networktables import NetworkTables
from cscore import CameraServer, UsbCamera
from time import sleep
import logging

RIO = 'roborio-1289-frc.local'
FIELD_OF_VIEW = 58.0 # degrees per logitech C170 tech specs
CAM_WIDTH = 640
CAM_HEIGHT = 480

DEGREES_PER_PIXEL = FIELD_OF_VIEW / float(CAM_WIDTH)

CENTER = CAM_WIDTH / 2

def translate(xpos):
    return xpos - CENTER

def getAngle(xpos):
    angle = translate(xpos) * DEGREES_PER_PIXEL 
    return angle
    
    
def main(table):
    cs = CameraServer.getInstance()
    cs.enableLogging()
    
    cam = cs.startAutomaticCapture()
    
    cam.setResolution(CAM_WIDTH, CAM_HEIGHT)
    
    # Get a CvSink. This will capture images from the camera
    cvSink = cs.getVideo(camera=cam)
    
    # (optional) Setup a CvSource. This will send images back to the Dashboard
    outputStream = cs.putVideo("Rectangle", CAM_WIDTH, CAM_HEIGHT)
    
    # Allocating new images is very expensive, always try to preallocate
    rawimg = np.zeros(shape=(CAM_HEIGHT, CAM_WIDTH, 3), dtype=np.uint8)    

    while True:
        # Tell the CvSink to grab a frame from the camera and put it
        # in the source image.  If there is an error notify the output.
        #print('grab a frame...')
        time, rawimg = cvSink.grabFrame(rawimg,0.5)
        if time == 0:
            # Send the output the error.
            print(cvSink.getError())
            #outputStream.notifyError(cvSink.getError())
            # skip the rest of the current iteration
            continue

        hsv = cv2.cvtColor(rawimg, cv2.COLOR_RGB2HSV)
        lower = np.array([30, 50, 50])
        upper = np.array([60,255,255])

        # Threshold the HSV image to get only the selected colors
        mask = cv2.inRange(hsv, lower, upper)

        mask, contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        if len(contours) == 0:
            continue
        try:
            target = max(contours, key=cv2.contourArea)
            targetMoment = cv2.moments(target)
        except:
            continue

        try:
            cx = int(targetMoment['m10'] / targetMoment['m00'])
            cy = int(targetMoment['m01'] / targetMoment['m00'])
        except ZeroDivisionError:
            cx = 0
            cy = 0
        angle = getAngle(cx)
        print('%d\t%0.2f' % (cx, angle))
        table.putNumber('cameraAngle', angle)
        #print('%d\t%d\t%0.2f\t%0.2f\t%0.2f' % (cx, cy, cx/float(CAM_HEIGHT), FIELD_OF_VIEW/2, angle))

        
        # Give the output stream a new image to display
        outputStream.putFrame(rawimg)    



if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    NetworkTables.initialize(server=RIO)
    sleep(5)
    main(NetworkTables.getTable('SmartDashboard'))
