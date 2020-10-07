
# PyQt5 imports
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread
from PyQt5.QtWidgets import QWidget, QLabel, QGridLayout
from PyQt5 import QtGui
from PyQt5.QtGui import QPixmap, QColor

# OpenCV imports
import cv2

# numpy imports
import numpy as np

# SSMS imports
from ssms import Analysis


class Display(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SSMS")
        self.display_width = 1600
        self.display_height = 900

        # create a text label
        self.textLabel = QLabel('Webcam')

        # create a vertical box layout and add the two labels
        self.layout = QGridLayout()
        self.layout.addWidget(self.textLabel)

        # create the 4 image labels
        self.previews = []
        self.previews.append(self._create_im_preview(0, 0))
        self.previews.append(self._create_im_preview(0, 1))
        self.previews.append(self._create_im_preview(1, 0))
        self.previews.append(self._create_im_preview(1, 1))

        # set the vbox layout as the widgets layout
        self.setLayout(self.layout)

        # create the video capture thread
        self.thread = Analysis.Analysis()
        # connect its signal to the update_image slot
        self.thread.change_image_signal.connect(self.update_image)
        # start the thread
        self.thread.start()

    def _create_im_preview(self, row, col):
        im = QLabel(self)
        self.layout.addWidget(im, row, col)
        return im

    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert.scaled(int(self.display_width / 2), int(self.display_height / 2), Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)

    @pyqtSlot(np.ndarray, int)
    def update_image(self, cv_img, index):
        """Updates the image_label with a new opencv image"""
        qt_img = self.convert_cv_qt(cv_img)
        self.previews[index].setPixmap(qt_img)
