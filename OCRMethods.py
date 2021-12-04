import cv2
import numpy as np
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import correlate2d

def loadImg(imgPath):
    imgcolor = cv2.imread(imgPath)
    img = cv2.cvtColor(imgcolor, cv2.COLOR_BGR2GRAY)
    return img

def imshow(img):
    plt.imshow(img, cmap = 'gray')
    plt.show()

def crop(img, r):
    return img[int(r[1]):int(r[1] + r[3]), int(r[0]):int(r[0] + r[2])]

# def ROICrop(img):
#     r = cv2.selectROI(img)
#     imCrop = crop(img, r)
#     cv2.imshow('crop',imCrop)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()
#     return r, imCrop

def partitionBoard(path): #partition a voltorb flip board in a standardized manner into sub-images
    #list of bounding boxes for Voltorb Flip board
    r1 = np.array([2370, 30, 240, 240])
    r2 = np.array([2370, 330, 240, 240])
    deltar = r2-r1
    r3 = r2+deltar
    r4 = r3+deltar
    r5 = r4+deltar
    c1 = np.array([870, 1530, 240, 240])
    c2 = np.array([1170, 1530, 240, 240])
    deltac = c2-c1
    c3 = c2+deltac
    c4 = c3+deltac
    c5 = c4+deltac
    boundlist = (r1, r2, r3, r4, r5, c1, c2, c3, c4, c5)

    #load image
    img = loadImg(path)
    cropList = []
    for r in boundlist:
        cropped = crop(img,r)
        cropList.append(cropped)
    return cropList

def loadKernels(): #I ended up not needing to use the zero kernel, convolving against 1-9 gives a unique enough vector
    k0 = loadImg('/Users/dylan/Documents/PythonScratchPaper/VoltorbFlip/DigitLibrary/NewKernels/0.png')
    k1 = loadImg('/Users/dylan/Documents/PythonScratchPaper/VoltorbFlip/DigitLibrary/NewKernels/1.png')
    k2 = loadImg('/Users/dylan/Documents/PythonScratchPaper/VoltorbFlip/DigitLibrary/NewKernels/2.png')
    k3 = loadImg('/Users/dylan/Documents/PythonScratchPaper/VoltorbFlip/DigitLibrary/NewKernels/3.png')
    k4 = loadImg('/Users/dylan/Documents/PythonScratchPaper/VoltorbFlip/DigitLibrary/NewKernels/4.png')
    k5 = loadImg('/Users/dylan/Documents/PythonScratchPaper/VoltorbFlip/DigitLibrary/NewKernels/5.png')
    k6 = loadImg('/Users/dylan/Documents/PythonScratchPaper/VoltorbFlip/DigitLibrary/NewKernels/6.png')
    k7 = loadImg('/Users/dylan/Documents/PythonScratchPaper/VoltorbFlip/DigitLibrary/NewKernels/7.png')
    k8 = loadImg('/Users/dylan/Documents/PythonScratchPaper/VoltorbFlip/DigitLibrary/NewKernels/8.png')
    k9 = loadImg('/Users/dylan/Documents/PythonScratchPaper/VoltorbFlip/DigitLibrary/NewKernels/9.png')
    return (k1, k2, k3, k4, k5, k6, k7, k8, k9)

def loadlibs(): #load score vectors for comparison
    v0 = [1105425.0, 1820700.0, 2080800.0, 1495575.0, 2015775.0, 2145825.0, 1430550.0, 2340900.0, 2145825.0]
    v1 = [1430550.0, 1235475.0, 1170450.0, 910350.0, 1105425.0, 1235475.0, 1040400.0, 1235475.0, 1170450.0]
    v2 = [1235475.0, 2275875.0, 2015775.0, 1365525.0, 1690650.0, 1820700.0, 1625625.0, 2015775.0, 1950750.0]
    v3 = [1170450.0, 2015775.0, 2340900.0, 1430550.0, 2015775.0, 2145825.0, 1560600.0, 2340900.0, 2210850.0]
    v4 = [910350.0, 1365525.0, 1430550.0, 1950750.0, 1430550.0, 1625625.0, 1235475.0, 1690650.0, 1560600.0]
    vlib = (v0, v1, v2, v3, v4)

    pts2 = [1235475.0, 2275875.0, 2080800.0, 1495575.0, 2015775.0, 2145825.0, 1625625.0, 2340900.0, 2145825.0]
    pts3 = [1170450.0, 2015775.0, 2340900.0, 1495575.0, 2015775.0, 2145825.0, 1560600.0, 2340900.0, 2210850.0]
    pts4 = [1105425.0, 1820700.0, 2080800.0, 1950750.0, 2015775.0, 2145825.0, 1430550.0, 2340900.0, 2145825.0]
    pts5 = [1105425.0, 1820700.0, 2080800.0, 1495575.0, 2275875.0, 2145825.0, 1430550.0, 2340900.0, 2145825.0]
    pts6 = [1235475.0, 1820700.0, 2145825.0, 1625625.0, 2145825.0, 2405925.0, 1430550.0, 2405925.0, 2210850.0]
    pts7 = [1105425.0, 1820700.0, 2080800.0, 1495575.0, 2015775.0, 2145825.0, 1820700.0, 2340900.0, 2145825.0]
    pts8 = [1235475.0, 2015775.0, 2340900.0, 1690650.0, 2145825.0, 2405925.0, 1560600.0, 2601000.0, 2405925.0]
    pts9 = [1170450.0, 1950750.0, 2210850.0, 1560600.0, 2015775.0, 2210850.0, 1560600.0, 2405925.0, 2405925.0]
    pts10 = [1430550.0, 1820700.0, 2080800.0, 1495575.0, 2015775.0, 2145825.0, 1430550.0, 2340900.0, 2145825.0]
    pts11 = [1430550.0, 1235475.0, 1170450.0, 910350.0, 1105425.0, 1235475.0, 1040400.0, 1235475.0, 1170450.0]
    plib = (pts2, pts3, pts4, pts5, pts6, pts7, pts8, pts9, pts10, pts11)
    return vlib, plib

def thres(img, T): #properly threshold the images
    h, w = img.shape
    for i in range(0,h):
        for j in range(0,w):
            if img[i,j] > T:
                img[i,j] = 0
            else:
                img[i,j] = 255
    return img

def downsample(img, num): #downsample
    return img[1::num,1::num]

def mymax(arr): #find max value and position
    maxVal = np.max(np.max(arr))
    pos = np.where(arr==maxVal)
    return maxVal, pos

def corr(img,kernels): #correlate2d img against library of kernels, return score vector
    scores = []
    poss = []
    for kernel in kernels:
        out = correlate2d(np.asarray(img, dtype = float),np.asarray(kernel, dtype=float))
        score, pos = mymax(out)
        scores.append(score)
        poss.append(pos)
    return scores, poss

def recognize(kernels, img): #wrapper for correlating a partition against a digit library and choosing the correct digit from the library

    vlib, plib = loadlibs() #load vectors for comparison

    T = 125
    imPts = downsample(thres(img[0:90, 75::], T), 10) #threshold and downsample images
    imVtbs = downsample(thres(img[90::, 150::], T), 10) #threshold and downsample images
    scores, _ = corr(imVtbs, kernels) #calculate voltorbs score
    scoresP, positionsP = corr(imPts, kernels) #calculate points score

    vtbsGuess = -1
    ptsGuess = -1
    err = 0
    for i, libv in enumerate(vlib):
        overlap2 = np.dot(libv,scores)/np.dot(libv,libv)
        if overlap2 == 1:
            vtbsGuess = i

    for j, libp in enumerate(plib):
        # print(j+2)
        overlap = np.dot(libp,scoresP)/np.dot(libp,libp)
        if overlap == 1:
            ptsGuess = j+2

    if vtbsGuess == -1:
        err = 1
    if ptsGuess == -1:
        err = 1
    return imPts, ptsGuess, imVtbs, vtbsGuess, err
