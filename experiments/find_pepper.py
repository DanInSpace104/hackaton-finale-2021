import cv2
import cv2 as cv
import imutils
import numpy as np

cv2.namedWindow("result")
cv2.namedWindow("w1")
img = cv2.imread('grechka.jpg')
(R, G, B) = cv2.split(img)
zeros = np.zeros(img.shape[:2], dtype="uint8")
img = cv2.merge([zeros, zeros, R])

img = imutils.resize(img, width=500)
img = cv2.medianBlur(img, 5)
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

cv2.imshow('w1', hsv)


# gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# ret, thresh = cv2.threshold(img, 50, 200, cv2.THRESH_BINARY)  # <--- Try different values here
h_min = np.array((0, 0, 0), np.uint8)
h_max = np.array((255, 222, 76), np.uint8)

# накладываем фильтр на кадр в модели HSV
thresh = cv2.inRange(hsv, h_min, h_max)
cv2.imshow('w1', thresh)

accum_size = 1
# Minimum distance between the centers of the detected circles.
minDist = 30
# First method-specific parameter. In case of CV_HOUGH_GRADIENT , it is the higher threshold of the two passed to the Canny() edge detector (the lower one is twice smaller).
param1 = 50
# Second method-specific parameter. In case of CV_HOUGH_GRADIENT , it is the accumulator threshold for the circle centers at the detection stage. The smaller it is, the more false circles may be detected. Circles, corresponding to the larger accumulator values, will be returned first.
param2 = 9
#
minRadius = 10
#
maxRadius = 30


def trash(img):
    cimg = img
    # circles = cv2.HoughCircles(
    #     thresh,
    #     cv2.HOUGH_GRADIENT,
    #     accum_size,
    #     minDist,
    #     param1=param1,
    #     param2=param2,
    #     minRadius=minRadius,
    #     maxRadius=maxRadius,
    # )
    # # circles = cv.HoughCircles(
    # #     img, cv.HOUGH_GRADIENT, 1, 20, param1=50, param2=30, minRadius=0, maxRadius=0
    # # )
    # circles = np.uint16(np.around(circles))
    # for i in circles[0, :]:
    #     # draw the outer circle
    #     cv.circle(cimg, (i[0], i[1]), i[2], (0, 255, 0), 2)
    #     # draw the center of the circle
    #     cv.circle(cimg, (i[0], i[1]), 2, (0, 0, 255), 3)
    return cimg


res = trash(img)
cv2.imshow('result', res)


while True:
    ch = cv2.waitKey(5)
    if ch == 27:
        break
cv2.destroyAllWindows()
