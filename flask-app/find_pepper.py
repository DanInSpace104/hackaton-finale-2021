import sys
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
ic.disable()


def wait_esc():
    while True:
        ch = cv.waitKey(5)
        if ch == 27:
            break


class Img:
    def __init__(self, img=None, path=''):
        self.img = img
        self.mask = None
        self.thresh = None
        if path:
            self.img = cv.imread(path)
        self.start_img = imutils.resize(self.img, width=500)
        self.img = self.start_img

    def center_crop(self, dim: tuple, img=None):
        """Returns center cropped image

        Args:Image Scaling
        img: image to be center cropped
        dim: dimensions (width, height) to be cropped from center
        """
        img = img or self.img
        width, height = img.shape[1], img.shape[0]
        # process crop width and height for max available dimension
        crop_width = dim[0] if dim[0] < img.shape[1] else img.shape[1]
        crop_height = dim[1] if dim[1] < img.shape[0] else img.shape[0]
        mid_x, mid_y = int(width / 2), int(height / 2)
        cw2, ch2 = int(crop_width / 2), int(crop_height / 2)
        crop_img = img[mid_y - ch2 : mid_y + ch2, mid_x - cw2 : mid_x + cw2]
        return crop_img

    def preprocess(self):
        img = self.center_crop((200, 150))
        # img = cv2.GaussianBlur(img, (5, 5), 0)
        img = cv.medianBlur(img, 5)
        self.img = cv2.GaussianBlur(img, (5, 5), 0)
        return self.img.copy()

    def cut_cart(self):
        img = self.img
        contours, hierarchy = cv2.findContours(self.img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        all_areas = []

        for cnt in contours:
            area = cv2.contourArea(cnt)
            all_areas.append(area)

        sorted_contours = sorted(contours, key=cv2.contourArea, reverse=True)
        mask = np.zeros_like(img)  # Create mask where white is what we want, black otherwise
        cv2.drawContours(mask, sorted_contours, 0, WHITE, thickness=-1)
        out = np.zeros_like(img)  # Extract out the object and place into output image
        out[mask == 255] = img[mask == 255]
        (y, x) = np.where(mask == 255)
        (topy, topx) = (np.min(y), np.min(x))
        (bottomy, bottomx) = (np.max(y), np.max(x))
        out = out[topy : bottomy + 1, topx : bottomx + 1]
        # cv.rectangle(out, (0, 0), self.img.shape[:2][::-1], WHITE, 40)
        self.img = out

        h, w = out.shape[:2]
        ic(h, w)
        center = self.start_img.shape[0] / 2, self.start_img.shape[1] / 2
        ic(center)
        x = center[1] - w / 2
        y = center[0] - h / 2

        self.start_img = self.start_img[int(y) : int(y + h), int(x) : int(x + w)]
        return out

    def threshold(self, mask=None):
        mask = mask or self.img
        self.img = cv.threshold(mask, 60, 255, cv.THRESH_BINARY)[1]
        return self.img

    def get_mask(self):
        hsv = cv.cvtColor(self.img, cv.COLOR_BGR2HSV)
        lower = np.array([000, 33, 114])
        upper = np.array([128, 255, 255])
        self.mask = cv.inRange(hsv, lower, upper)
        self.img = self.mask
        return self.mask

    def thick_white_contours(self, img=None):
        img = img or self.img
        contours, hierarchy = cv2.findContours(img.astype(np.uint8), 1, 2)
        cv2.drawContours(img, contours, -1, (255, 255, 255), thickness=3)
        return img, contours, hierarchy

    def find_circles(self, img=None, on_origin=False):
        accum_size = 1
        # Minimum distance between the centers of the detected circles.
        minDist = 20
        # First method-specific parameter. In case of CV_HOUGH_GRADIENT , it is the higher threshold of the two passed to the Canny() edge detector (the lower one is twice smaller).
        param1 = 50
        # Second method-specific parameter. In case of CV_HOUGH_GRADIENT , it is the accumulator threshold for the circle centers at the detection stage. The smaller it is, the more false circles may be detected. Circles, corresponding to the larger accumulator values, will be returned first.
        param2 = 6
        #
        minRadius = 5
        #
        maxRadius = 35
        img = img or self.img
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
        if circles is None:
            ic('Circles not found')
            return self.img

        circles = np.uint16(np.around(circles))
        for i in circles[0, :]:
            circle_img = np.zeros((img.shape[0], img.shape[1]), np.uint8)
            cv2.circle(circle_img, (i[0], i[1]), i[2], WHITE, -1)
            datos_rgb = cv2.mean(img, mask=circle_img)[::-1]
            ic(datos_rgb[3])
            if datos_rgb[3] < 70:
                # print('circle_found')
                cv.circle(cimg, (i[0], i[1]), i[2], BLUE, 2)
                # draw the center of the circle
                cv.circle(cimg, (i[0], i[1]), 2, GREEN, 3)
                if on_origin:
                    cv.circle(self.start_img, (i[0], i[1]), i[2], BLUE, 2)
                    # draw the center of the circle
                    cv.circle(self.start_img, (i[0], i[1]), 2, GREEN, 3)
        self.img = cimg
        return cimg.copy()

    def show(self, img=None, name='Image'):
        if not HAS_DISPLAY:
            return
        if img is None:
            img = self.img
        try:
            cv.imshow(name, img)
        except:
            return
        wait_esc()
        cv.destroyWindow(name)

    def center(self):
        h, w = self.img.shape[:2]
        return (h/2, w/2)

    def draw_sniper(self):
        center = self.center()
        # print(center, self.img.shape)
        point2 = tuple(map(int, (center[0]-30, center[1] - 50)))[::-1]
        point1 = tuple(map(int, (center[0]+30, center[1] + 50)))[::-1]
        # point2 = (center[0]+30, center[1] + 30)
        # print(type(point1), point2)

        cv2.rectangle(self.img, point1, point2, color=RED, thickness=4)
        return self.img.copy()
        # print(type(center), center)
        # center = (150, 100)
        # print(type(center), center)
        # cv2.circle(self.img, center, 10, RED, 10)


def find_pepper(img=None, path=None):
    images = []
    img = Img(img=img, path=path)
    images.append(img.start_img.copy())
    # images.append(img.draw_sniper())
    images.append(img.preprocess())
    mask = img.get_mask()
    images.append(mask.copy())

    thr = img.threshold()
    images.append(thr.copy())

    images.append(img.cut_cart())
    img.thick_white_contours()
    # img.show()
    # cv.rectangle(img.img, (0, 0), img.img.shape[:2][::-1], WHITE, 50)
    # img.show()

    images.append(img.find_circles(on_origin=True))
    return images
    # img.show(img.start_img)


def check_display():
    try:
        img = cv.imread('pictures/g1.jpg')
        cv.imshow(img)
        cv.destroyAllWindows()
        return True
    except:
        return False


if __name__ == '__main__':
    # HAS_DISPLAY = check_display()
    HAS_DISPLAY = False
    ic.enable()
    paths = ['pictures/g1.jpg', 'pictures/g2_clear.jpg', 'pictures/g3.jpg']
    ic(sys.argv)
    if len(sys.argv) > 1:
        path = sys.argv[1]

    list(map(find_pepper, paths))
    # find_pepper()
    if HAS_DISPLAY:
        cv.destroyAllWindows()
