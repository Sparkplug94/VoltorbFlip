import re
import cv2
import numpy as np
import pytesseract
from pytesseract import Output
from matplotlib import pyplot as plt

#load kernels
def loadKernels():
    ptsdir = 'DigitLibrary/PointsKernels/'
    vtbsdir = 'DigitLibrary/VoltorbKernels/'

    k2 = cv2.cvtColor(cv2.imread(ptsdir+'02.png'), cv2.COLOR_BGR2GRAY)
    k3 = cv2.cvtColor(cv2.imread(ptsdir+'03.png'), cv2.COLOR_BGR2GRAY)
    k4 = cv2.cvtColor(cv2.imread(ptsdir+'04.png'), cv2.COLOR_BGR2GRAY)
    k5 = cv2.cvtColor(cv2.imread(ptsdir+'05.png'), cv2.COLOR_BGR2GRAY)
    k6 = cv2.cvtColor(cv2.imread(ptsdir+'06.png'), cv2.COLOR_BGR2GRAY)
    k7 = cv2.cvtColor(cv2.imread(ptsdir+'07.png'), cv2.COLOR_BGR2GRAY)
    k8 = cv2.cvtColor(cv2.imread(ptsdir+'08.png'), cv2.COLOR_BGR2GRAY)
    k9 = cv2.cvtColor(cv2.imread(ptsdir+'09.png'), cv2.COLOR_BGR2GRAY)
    k10 = cv2.cvtColor(cv2.imread(ptsdir+'10.png'), cv2.COLOR_BGR2GRAY)

    v0 = cv2.cvtColor(cv2.imread(vtbsdir+'0.png'), cv2.COLOR_BGR2GRAY)
    v1 = cv2.cvtColor(cv2.imread(vtbsdir+'1.png'), cv2.COLOR_BGR2GRAY)
    v2 = cv2.cvtColor(cv2.imread(vtbsdir+'2.png'), cv2.COLOR_BGR2GRAY)
    v3 = cv2.cvtColor(cv2.imread(vtbsdir+'3.png'), cv2.COLOR_BGR2GRAY)
    v4 = cv2.cvtColor(cv2.imread(vtbsdir+'4.png'), cv2.COLOR_BGR2GRAY)


    pMaxs = [202878000.0, 211461300.0, 179989200.0, 205218900.0, 215362800.0, 161001900.0, 235650600.0, 216663300.0, 333708300.0]
    vMaxs = [213802200.0, 122247000.0, 202617900.0, 211461300.0, 179989200.0]
    plist = [k2,k3,k4,k5,k6,k7,k8,k9,k10]
    vlist = [v0,v1,v2,v3,v4]
    return plist, pMaxs, vlist, vMaxs


# get grayscale image
def get_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

def cutout(roi, img):
    cut = img[roi[0]:roi[1],roi[2]:roi[3]]
    cut[90::,0:165] = 255
    return remove_noise(cut)

# noise removal
def remove_noise(image):
    return cv2.medianBlur(image, 5)


# thresholding
def thresholding(image):
    return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)


# dilation
def dilate(image):
    kernel = np.ones((5, 5), np.uint8)
    return cv2.dilate(image, kernel, iterations=1)


# erosion
def erode(image):
    kernel = np.ones((5, 5), np.uint8)
    return cv2.erode(image, kernel, iterations=1)


# opening - erosion followed by dilation
def opening(image):
    kernel = np.ones((5, 5), np.uint8)
    return cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)


# canny edge detection
def canny(image):
    return cv2.Canny(image, 100, 200)


# skew correction
def deskew(image):
    coords = np.column_stack(np.where(image > 0))
    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return rotated


# template matching
def match_template(image, template):
    return cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)