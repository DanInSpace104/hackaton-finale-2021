import time

import cv2
import cv2 as cv
import imutils
import numpy as np
from icecream import ic

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (0, 0, 255)
GREEN = (0, 255, 0)
BLUE = (255, 0, 0)


def thresh(img):
    _, thresh = cv.threshold(img, 60, 255, cv.THRESH_BINARY)  # <--- Try different values here
    return thresh


def find_circles(img):
    accum_size = 1
    # Minimum distance between the centers of the detected circles.
    minDist = 60
    # First method-specific parameter. In case of CV_HOUGH_GRADIENT , it is the higher threshold of the two passed to the Canny() edge detector (the lower one is twice smaller).
    param1 = 50
    # Second method-specific parameter. In case of CV_HOUGH_GRADIENT , it is the accumulator threshold for the circle centers at the detection stage. The smaller it is, the more false circles may be detected. Circles, corresponding to the larger accumulator values, will be returned first.
    param2 = 6
    #
    minRadius = 15
    #
    maxRadius = 30
    cimg = cv.cvtColor(img, cv.COLOR_GRAY2BGR)
    circles = cv.HoughCircles(
        img,
        cv.HOUGH_GRADIENT,
        accum_size,
        minDist,
        param1=param1,
        param2=param2,
        minRadius=minRadius,
        maxRadius=maxRadius,
    )

    circles = np.uint16(np.around(circles))
    for i in circles[0, :]:
        circle_img = np.zeros((img.shape[0], img.shape[1]), np.uint8)
        cv2.circle(circle_img, (i[0], i[1]), i[2], (255, 255, 255), -1)
        datos_rgb = cv2.mean(img, mask=circle_img)[::-1]
        ic(datos_rgb)
        if datos_rgb[3] < 70:
            cv.circle(cimg, (i[0], i[1]), i[2], BLUE, 2)
            # draw the center of the circle
            cv.circle(cimg, (i[0], i[1]), 2, GREEN, 3)
    return cimg


def create_mask(img):
    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    lower = np.array([000, 33, 114])
    upper = np.array([128, 255, 255])
    mask = cv.inRange(hsv, lower, upper)
    return mask


def wait_esc():
    while True:
        ch = cv.waitKey(5)
        if ch == 27:
            break


def show_image(img):
    cv2.namedWindow('Display', cv2.WINDOW_NORMAL)
    cv2.imshow('Display', img)
    wait_esc()
    cv.destroyWindow('Display')


def find_greatest_contour(contours):
    largest_area = 0
    largest_contour_index = -1
    i = 0
    total_contours = len(contours)
    while i < total_contours:
        area = cv2.contourArea(contours[i])
        if area > largest_area:
            largest_area = area
            largest_contour_index = i
        i += 1

    return largest_area, largest_contour_index


if __name__ == '__main__':

    img = cv.imread('grechka.jpg')
    img = imutils.resize(img, width=500)
    img = cv2.GaussianBlur(img, (5, 5), 0)
    img = cv.medianBlur(img, 5)
    img = cv2.GaussianBlur(img, (5, 5), 0)
    mask = create_mask(img)
    # cv.imshow('mask', mask)

    thr = thresh(mask)

    contours, hierarchy = cv2.findContours(thr.astype(np.uint8), 1, 2)
    cv2.drawContours(thr, contours, -1, (255, 255, 255), thickness=8)
    show_image(thr)
    # mean = cv.mean(img, mask=mask)
    # ic(mean)

    # show_image(thr)
    # ic(hierarchy)
    # cnts = contours
    # for cnt in cnts:
    #     if cv2.contourArea(cnt) > 800:  # filter small contours
    #         x, y, w, h = cv2.boundingRect(cnt)  # offsets - with this you get 'mask'
    #         cv2.circle(
    #             img,
    #             (x, y),
    #         )
    #         cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
    # cv2.imshow('cutted contour', img[y : y + h, x : x + w])
    # print(
    #     'Average color (BGR): ',
    #     np.array(cv2.mean(img[y : y + h, x : x + w])).astype(np.uint8),
    # )
    # wait_esc()

    img = find_circles(thr)
    show_image(img)

    cv.destroyAllWindows()
