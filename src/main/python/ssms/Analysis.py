
import cv2
import imutils
import numpy
import time

from PyQt5.QtCore import pyqtSignal, QThread

from ssms import BufferedCamera


def detect_shape(c):
    shape = None
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.02 * peri, True)  # Ramer-Douglas-Peucker algorithm
    if len(approx) == 3:
        shape = 'triangle'
    elif len(approx) == 12:
        shape = 'cross'

    return shape, approx


class Analysis(QThread):
    """
    Performs computer vision analysis.

    Uses the first camera device detected by OpenCV.
    """

    change_image_signal = pyqtSignal(numpy.ndarray, int)

    def __init__(self):
        super().__init__()
        self.device = BufferedCamera.BufferedCamera(0)
        self._run_flag = True

    def run(self):
        while self._run_flag:
            self.perf_analysis()
            time.sleep(0.024)

    def stop(self):
        self._run_flag = False
        self.wait()

    def perf_analysis(self):
        image = self.device.read()

        self.change_image_signal.emit(image, 0)

        resized = imutils.resize(image, width=300)
        ratio = image.shape[0] / float(resized.shape[0])

        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        lower = numpy.array([0, 0, 80], numpy.uint8)
        upper = numpy.array([179, 255, 255], numpy.uint8)
        mask = cv2.inRange(hsv, lower, upper)
        # image2 = cv2.bitwise_and(image, image, mask=mask)

        # gray = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

        self.change_image_signal.emit(mask, 1)

        # blurred = cv2.GaussianBlur(mask, (5, 5), 0)
        thresh = cv2.threshold(mask, 60, 255, cv2.THRESH_BINARY_INV)[1]
        # find contours in the thresholded image and initialize the
        # shape detector
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)

        mask2 = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
        image2 = image.copy()
        draw_on = [mask2, image2]

        for c in cnts:
            try:
                # compute the center of the contour, then detect the name of the
                # shape using only the contour
                M = cv2.moments(c)
                cX = int((M["m10"] / M["m00"]))  # * ratio)
                cY = int((M["m01"] / M["m00"]))  # * ratio)
                shape, approx = detect_shape(c)
                num_vert = len(approx)
                if num_vert in [3, 12]:
                    # multiply the contour (x, y)-coordinates by the resize ratio,
                    # then draw the contours and the name of the shape on the image
                    c = c.astype("int")

                    for img in draw_on:
                        cv2.drawContours(img, [approx], -1, (0, 255, 0), 2)
                        cv2.putText(img, shape, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX,
                                    0.5, (255, 0, 255), 2)
                        for vert in approx:
                            cv2.circle(img, (vert[0][0], vert[0][1]), radius=3, color=(0, 0, 255), thickness=-1)
            except ZeroDivisionError as zde:
                pass  # ignore ZDE errors
            except Exception as e:
                print(e)

        # send Qt signal to display
        self.change_image_signal.emit(mask2, 2)
        self.change_image_signal.emit(image2, 3)

        # show the output image
        #cv2.imshow("Image", image2)
        #key = cv2.waitKey(100)
        #if key == 27:
        #    return
