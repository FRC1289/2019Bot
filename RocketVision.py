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
    
    cam = UsbCamera('logitech', 0)
    cam.setResolution(CAM_WIDTH, CAM_HEIGHT)
    camSrv.addCamera(cam)
    
    # Get a CvSink. This will capture images from the camera
    cvSink = camSrv.getVideo()
    
    # (optional) Setup a CvSource. This will send images back to the Dashboard
    outputStream = camSrv.putVideo("Rectangle", CAM_WIDTH, CAM_HEIGHT)
    
    # Allocating new images is very expensive, always try to preallocate
    rawimg = np.zeros(shape=(CAM_HEIGHT, CAM_WIDTH, 3), dtype=np.uint8)

    # OpenCV ranges
    # Hue: 0 - 180
    # Saturation: 0 - 255
    # Vibrancy: 0 - 255
    lower = np.array([30, 50, 175])
    upper = np.array([60,255,255])
  

    while True:
        # Tell the CvSink to grab a frame from the camera and put it
        # in the source image.  If there is an error notify the output.
        time, rawimg = cvSink.grabFrame(rawimg,0.5)
        if time == 0:
            # Send the output the error.
            print(cvSink.getError())
            #outputStream.notifyError(cvSink.getError())
            # skip the rest of the current iteration
            continue

        # Threshold the HSV image to get only the selected colors
        hsv = cv2.cvtColor(rawimg, cv2.COLOR_RGB2HSV)
        mask = cv2.inRange(hsv, lower, upper)

        mask, contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        if len(contours) == 0:
            continue
        try:
            contours.sort(key=cv2.contourArea)
            target1 = contours[-1]
            target2 = contours[-2]
            target1Moment = cv2.moments(target1)
            target2Moment = cv2.moments(target2)
        except:
            continue

        try:
            target1Cx = int(target1Moment['m10'] / target1Moment['m00'])
            target1Cy = int(target1Moment['m01'] / target1Moment['m00'])

            target2Cx = int(target2Moment['m10'] / target2Moment['m00'])
            target2Cy = int(target2Moment['m01'] / target2Moment['m00'])

        except ZeroDivisionError:
            target1Cx = 0
            target1Cy = 0
            target2Cx = 0
            target2Cy = 0

        distance = int(vu.getDistance(target1Cx, target1Cy, target2Cx, target2Cy))
        cv2.drawContours(rawimg, [target1], -1, (0, 0, 255), 2)
        cv2.drawContours(rawimg, [target2], -1, (0, 0, 255), 2)
	# figure the midpoint of x1,y1 and x2,y2, get the angle for midX
        midX, midY = vu.getMidPoint(target1Cx, target1Cy, target2Cx, target2Cy)
        midX = int(midX)
        midY = int(midY)
        if distance > 100:
            cv2.circle(rawimg, (target1Cx, target1Cy), 7, (255, 0, 0), -1)
            cv2.circle(rawimg, (target2Cx, target2Cy), 7, (255, 0, 0), -1)
            cv2.drawMarker(rawimg, (midX, midY), (0,0,255), cv2.MARKER_CROSS, 20, 3)

        cv2.line(rawimg, (336,0), (336,480), (0,255,0), 2)
        cv2.line(rawimg, (304,0), (304,480), (0,255,0), 2)
        #cv2.circle(rawimg, (midX, midY), 7, (0, 0, 255), -1)
        #angle = vu.getAngle(midX, CENTER, DEGREES_PER_PIXEL)

        print('%d\t%d' % (midX, distance))
        table.putNumber('cameraAngle', midX)
        table.putNumber('distance', distance)

        # Give the output stream a new image to display
        outputStream.putFrame(rawimg)    



if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    NetworkTables.initialize(server=RIO)
    sleep(5)
    main(NetworkTables.getTable('SmartDashboard'))
