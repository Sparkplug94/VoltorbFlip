import re
import cv2
import numpy as np
import pytesseract
from pytesseract import Output
import matplotlib.pyplot as plt
from OldCode.OCRmethods import *
import os
import scipy
from scipy import signal
from tqdm import tqdm

#Set directory of images
IMG_DIR = '/Users/dylan/Desktop/'

#list all files in directory
filelist = os.listdir(IMG_DIR)
imagelist = []
print(filelist)
print(os.getcwd())

#find all images
for file in filelist:
    if file.endswith('.png'):
        imagelist.append(file)

#convert to rgb
image = cv2.imread(IMG_DIR + imagelist[0])
b,g,r = cv2.split(image)
rgb_img = cv2.merge([r,g,b])

#grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

#threshold
cutoff = 100
(T, thresh) = cv2.threshold(gray, cutoff, 255, cv2.THRESH_BINARY)
# plt.imshow(thresh, cmap = 'gray')
# plt.show()

#right hand side box ROIs
b1p = np.array([30, 280, 2365, 2610])
b2p = np.array([330, 580, 2365, 2610])
delta1 = b2p-b1p
b3p = b2p+delta1
b4p = b3p+delta1
b5p = b4p+delta1

#left hand side box ROIs (maybe implement convolutional detection of boxes?)
b6p = np.array([1520, 1770, 855, 1125])
b7p = np.array([1520, 1770, 1155, 1425])
delta2 = b7p-b6p
b8p = b7p+delta2
b9p = b8p+delta2
b10p = b9p+delta2

bplist = [b1p,b2p,b3p,b4p,b5p,b6p,b7p,b8p,b9p,b10p]

#cutout boxes
blist = []
for bp in bplist:
    blist.append(cutout(bp,thresh))


pointsList = []
voltorbsList = []
for image in blist:

    #split image into points and voltorbs
    ptsImg = np.asarray(cv2.bitwise_not(image[0:100,70::]), dtype = float)
    voltorbsImg = np.asarray(cv2.bitwise_not(image[120:240,150::]), dtype = float)
    # plt.imshow(ptsImg, cmap = 'gray')
    # plt.show()
    # plt.imshow(voltorbsImg, cmap = 'gray')
    # plt.show()

    #load correlation kernels
    pKernels, pMaxs, vKernels, vMaxs = loadKernels()

    #convolve against all points kernels
    corrNums = []
    for i, mykernel in enumerate(pKernels):
        kernel = np.asarray(cv2.bitwise_not(mykernel), dtype=float)
        conv = signal.correlate2d(kernel, ptsImg)
        convmax = np.max(np.max(conv))
        corrNums.append(convmax/pMaxs[i])
    print(np.round(corrNums,3))
    #convolve against all voltorb kernels
    vNums = []
    for j, mykernel in enumerate(vKernels):
        kernel = np.asarray(cv2.bitwise_not(mykernel), dtype=float)
        # if j == 4:
        #     print(np.max(np.max(signal.correlate2d(kernel,kernel))))
        conv = signal.correlate2d(kernel,voltorbsImg)
        convmax = np.max(np.max(conv))
        vNums.append(convmax/vMaxs[j])
    print(vNums)
    ptsGuess = 2+np.argmax(corrNums)
    if np.abs(corrNums[1]-1) < 0.02:
        if np.abs(corrNums[6]-1) < 0.02:
            ptsGuess = 8

    voltorbsGuess = np.argmax(vNums)
    pointsList.append(ptsGuess)
    voltorbsList.append(voltorbsGuess)
    # print('Guesses are ('+str(ptsGuess)+', '+str(voltorbsGuess)+')')
    # plt.imshow(image,cmap='gray')
    # plt.title(ptsGuess)
    # plt.show()

print(pointsList)
print(voltorbsList)

stats = pointsList[0:5], voltorbsList[0:5], pointsList[5:10], voltorbsList[5:10]
np.save('OCRstats',stats)
print(stats)
plt.imshow(rgb_img)
plt.show()
