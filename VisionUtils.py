import math

def translate(xpos, center):
    return xpos - center

def getAngle(xpos, center, degreesPerPixel):
    angle = translate(xpos, center) * degreesPerPixel
    return angle

def getDistance(x1, y1, x2, y2):
    return math.sqrt((x2-x1)**2 + (y2-y1)**2)

def getMidPoint(x1, y1, x2, y2):
    return ((x2+x1)/2, (y2+y1)/2)
