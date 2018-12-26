#! /usr/bin/python3

import cv2
import numpy as np
import sys

if len(sys.argv) < 4:
    print('need r g b')
    sys.exit(1)

red = int(sys.argv[1])
green = int(sys.argv[2])
blue = int(sys.argv[3])

bgrImage = np.uint8([[[blue, green, red]]])
hsvImage = cv2.cvtColor(bgrImage, cv2.COLOR_BGR2HSV)

print('HSV: ', hsvImage)
sys.exit(0)