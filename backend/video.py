###
### module for video processing
###

import picamera
import time
from imutils.perspective import four_point_transform
from imutils import contours
import imutils
import cv2
import numpy as np
import os

# define the dictionary of digit segments so we can identify
# each digit.
DIGITS_LOOKUP = {
	(1, 1, 1, 0, 1, 1, 1): 0,
	(0, 0, 1, 0, 0, 1, 0): 1,
	(1, 0, 1, 1, 1, 0, 1): 2,
	(1, 0, 1, 1, 0, 1, 1): 3,
	(0, 1, 1, 1, 0, 1, 0): 4,
	(1, 1, 0, 1, 0, 1, 1): 5,
	(1, 1, 0, 1, 1, 1, 1): 6,
    (1, 0, 0, 1, 1, 1, 1): 6,
	(1, 1, 1, 0, 0, 1, 0): 7,
	(1, 1, 1, 1, 1, 1, 1): 8,
    (1, 1, 1, 1, 0, 1, 0): 9
}

FP_MARGIN = 15


# For debugging.
def showimg(img):
    cv2.imshow('img', img)
    cv2.waitKey(0)

def get_rectangle(pts):
    result = [pts[0], pts[0], pts[0], pts[0]]
    for p in pts:
        i = p[0] + p[1]
        j = p[0] - p[1]
        if (i < sum(result[0])):
            result[0] = p
        if (i > sum(result[2])):
            result[2] = p
        if (j < result[1][0] - result[1][1]):
            result[1] = p
        if (j > result[3][0] - result[3][1]):
            result[3] = p
    for i in range(len(result)):
        result[i] = list(map(int, result[i]))
    return result



errcnt = 0

# Read data from camara in Raspberry Pi, extract remaining
# time data by seven segment recognition. Return remaining
# time is success, -1 otherwise.
def get_remaining_time():
    global errcnt
    try:
        # Capture with Raspberry Pi camera
        with picamera.PiCamera() as camera:
            camera.resolution = (1024, 768)
            camera.capture('capture.jpg')
        # Open, Read an image.
        image = cv2.imread('capture.jpg')
        image = cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)
        image = imutils.resize(image, height=500)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        for i in range(len(gray)):
            for j in range(len(gray[i])):
                if (gray[i][j] < 250):
                    gray[i][j] = 255
                else:
                    gray[i][j] = 0

        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        edged = cv2.Canny(blurred, 50, 200, 255)

        cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        digitCnts = []

        for c in cnts:
            (x, y, w, h) = cv2.boundingRect(c)
            if (h > 50 and h < 80):
                digitCnts.append(c)

        digitCnts = contours.sort_contours(digitCnts, method='left-to-right')[0]
        for c in digitCnts:
            (x, y, w, h) = cv2.boundingRect(c)
        # Create rectangle containing LCD, for four point transformation.
        rect = get_rectangle(list(cv2.boxPoints(cv2.minAreaRect(digitCnts[0]))) +
                             list(cv2.boxPoints(cv2.minAreaRect(digitCnts[3]))))

        rect[0][0] -= FP_MARGIN
        rect[0][1] -= FP_MARGIN
        rect[1][0] -= FP_MARGIN
        rect[1][1] += FP_MARGIN
        rect[2][0] += FP_MARGIN
        rect[2][1] += FP_MARGIN
        rect[3][0] += FP_MARGIN
        rect[3][1] -= FP_MARGIN

        # Perform four point transform with rectangle created above.
        image = four_point_transform(image, np.array(rect, dtype=int))
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        for i in range(len(gray)):
            for j in range(len(gray[i])):
                if (gray[i][j] < 250):
                    gray[i][j] = 255
                else:
                    gray[i][j] = 0
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        edged = cv2.Canny(blurred, 50, 200, 255)

        cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        digitCnts = []
        for c in cnts:
            (x, y, w, h) = cv2.boundingRect(c)
            if (h >= 60):
                digitCnts.append(c)

        digitCnts = contours.sort_contours(digitCnts, method='left-to-right')[0]
        digits = []
        thresh = cv2.threshold(gray, 0, 255,
                               cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (1, 5))
        thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)

        for c in digitCnts:
            (x, y, w, h) = cv2.boundingRect(c)
            # if width is small enough, we recognize it as `1`.
            if (w < 30):
                digits.append(1)
                continue
            roi = gray[y:y+h, x:x+w]
            # compute the width and height of each of the 7 segments
            # we are going to examine
            (roiH, roiW) = roi.shape
            (dW, dH) = (int(roiW * 0.25), int(roiH * 0.15))
            dHC = int(roiH * 0.05)
            # define the set of 7 segments
            segments = [
                ((0, 0), (w, dH)),  # top
                ((0, 0), (dW, h // 2)),  # top-left
                ((w - dW, 0), (w, h // 2)),  # top-right
                ((0, (h // 2) - dHC), (w, (h // 2) + dHC)),  # center
                ((0, h // 2), (dW, h)),  # bottom-left
                ((w - dW, h // 2), (w, h)),  # bottom-right
                ((0, h - dH), (w, h))  # bottom
            ]
            on = [1] * len(segments)
            # loop over the segments
            for (i, ((xA, yA), (xB, yB))) in enumerate(segments):
                # extract the segment ROI, count the total number of
                # thresholded pixels in the segment, and then compute
                # the area of the segment
                segROI = roi[yA:yB, xA:xB]
                total = cv2.countNonZero(segROI)
                area = (xB - xA) * (yB - yA)
                # if the total number of non-zero pixels is greater than
                # 50% of the area, mark the segment as "on"
                if total / float(area) > 0.5:
                    on[i] = 0
            # lookup the digit and draw it on the image
            digit = DIGITS_LOOKUP[tuple(on)]
            digits.append(digit)
        return digits[0] * 1000 + digits[1] * 100 + digits[2] * 10 + digits[3]
    except Exception:
        os.rename("capture.jpg", "{0}.jpg".format(errcnt))
        errcnt += 1
        return -1


if __name__ == '__main__':
    while True:
        print(get_remaining_time())
