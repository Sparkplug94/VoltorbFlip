from os import listdir
from OCRMethods import *

#path to image
directory = '/Users/dylan/Desktop/'
filelist = listdir(directory)
pathlist = []
for file in filelist:
    if file.endswith('.png'):
        pathlist.append(directory+file)
print(pathlist)

#load digit library
kernels = loadKernels()

imgPath = pathlist[0]

pts = [] #init pts array
vtbs = [] #init voltorbs array
partitions = partitionBoard(imgPath) #partition the voltorb board

for i, img in enumerate(partitions): #for each partition, recognize digits
    imPts, ptsGuess, imVtbs, vtbsGuess, err = recognize(kernels, img)
    if err:
        print("error occurred at image " + str(i))
        break
    pts.append(ptsGuess)
    vtbs.append(vtbsGuess)

stats = (pts[0:5],vtbs[0:5],pts[5::],vtbs[5::])
print(stats)
np.save('OCRstats',stats)
# imshow(loadImg(imgPath))



