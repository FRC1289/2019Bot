#! /usr/bin/python3

import cv2
import numpy as np
from networktables import NetworkTables
from cscore import CameraServer, UsbCamera
from time import sleep
import logging
import VisionUtils as vu

RIO = 'roborio-1289-frc.local'
FIELD_OF_VIEW = 58.0 # degrees per logitech C170 tech specs
CAM_WIDTH = 640
CAM_HEIGHT = 480

DEGREES_PER_PIXEL = FIELD_OF_VIEW / float(CAM_WIDTH)
CENTER = CAM_WIDTH / 2
   
def main(table):
    camSrv = CameraServer.getInstance()
    camSrv.enableLogging()

    cam = UsbCamera("logitech", 0)
    camSrv.addCamera(cam)
    #cam = cs.startAutomaticCapture()
    
    cam.setResolution(CAM_WIDTH, CAM_HEIGHT)
    
    # Get a CvSink. This will capture images from the camera
    cvSink = camSrv.getVideo() #camera=cam)
    
    # (optional) Setup a CvSource. This will send images back to the Dashboard
    outputStream = camSrv.putVideo("Rectangle", CAM_WIDTH, CAM_HEIGHT)
    
    # Allocating new images is very expensive, always try to preallocate
    rawimg = np.zeros(shape=(CAM_HEIGHT, CAM_WIDTH, 3), dtype=np.uint8)
    # OpenCV ranges
    # Hue: 0 - 180
    # Saturation: 0 - 255
    # Vibrancy: 0 - 255
    lower = np.array([0, 0, 200])
    upper = np.array([10, 100, 255])

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

        # convert RGB to HSV
        hsv = cv2.cvtColor(rawimg, cv2.COLOR_RGB2HSV)

        # Threshold the HSV image to get only the selected colors
        mask = cv2.inRange(hsv, lower, upper)
        
        mask, contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        if len(contours) == 0:
            print('no contours')
            continue
        try:
            contours.sort(key=lambda x: cv2.contourArea(x))
            target = max(contours, key=cv2.contourArea)
            boundingBox = cv2.minAreaRect(target)
        except:
            print('no bounding box')
            continue

        angle = boundingBox[2]
        if angle < -45:
            angle = angle + 90
            
        table.putNumber('cameraAngle', angle)

        # draw a red outline on the output image
        # so that the user can see what is targeted
        boxPoints = cv2.boxPoints(boundingBox)
        boxPoints = np.int0(boxPoints)
        rawimg = cv2.drawContours(rawimg, [boxPoints], 0, (0,0,255), 2)
        # Give the output stream a new image to display
        outputStream.putFrame(rawimg)    



if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    NetworkTables.initialize(server=RIO)
    sleep(5)
    main(NetworkTables.getTable('SmartDashboard'))
