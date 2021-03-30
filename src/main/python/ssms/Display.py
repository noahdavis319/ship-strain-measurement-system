# PyQt5 imports
import sys

# OpenCV imports
import cv2

# numpy imports
import numpy as np

# Qt imports
import pyqtgraph as pg
from PyQt5 import QtCore, QtWidgets
from PyQt5 import QtGui
from PyQt5.QtGui import QPixmap

# scipy imports
from scipy.signal import savgol_filter

# SSMS imports
from ssms import Analysis
from ssms import Range

# pySerial imports
import serial


def configure_plot(plot, y_min, y_max, title, x_label, y_label, invert, bottom_major_spacing,
                   bottom_minor_spacing, left_major_spacing, left_minor_spacing, bottom_grid, left_grid):
    plot.setYRange(y_min, y_max)
    plot.setTitle(title=title)
    plot.setLabel('left', text=y_label)
    plot.setLabel('bottom', text=x_label)
    plot.invertX(invert)
    plot.getAxis('bottom').setTickSpacing(bottom_major_spacing, bottom_minor_spacing)
    plot.getAxis('left').setTickSpacing(left_major_spacing, left_minor_spacing)
    plot.getAxis('bottom').setGrid(bottom_grid)
    plot.getAxis('left').setGrid(left_grid)


class Ui_MainWindow(object):
    def __init__(self, MainWindow, args):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1600, 900)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
        self.tab_main = QtWidgets.QWidget()
        self.tab_main.setObjectName("tab_main")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.tab_main)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.tab_1_layout = QtWidgets.QGridLayout()
        self.tab_1_layout.setObjectName("tab_1_layout")
        self.frame_1 = QtWidgets.QFrame(self.tab_main)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_1.sizePolicy().hasHeightForWidth())
        self.frame_1.setSizePolicy(sizePolicy)
        self.frame_1.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_1.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_1.setObjectName("frame_1")
        self.frame_1_layout = QtWidgets.QGridLayout(self.frame_1)
        self.frame_1_layout.setContentsMargins(4, 4, 4, 4)
        self.frame_1_layout.setObjectName("frame_1_layout")
        self.tab_1_layout.addWidget(self.frame_1, 0, 0, 1, 1)
        self.frame_4 = QtWidgets.QFrame(self.tab_main)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_4.sizePolicy().hasHeightForWidth())
        self.frame_4.setSizePolicy(sizePolicy)
        self.frame_4.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.frame_4_layout = QtWidgets.QGridLayout(self.frame_4)
        self.frame_4_layout.setContentsMargins(4, 4, 4, 4)
        self.frame_4_layout.setObjectName("frame_4_layout")
        self.tab_1_layout.addWidget(self.frame_4, 1, 1, 1, 1)
        self.frame_3 = QtWidgets.QFrame(self.tab_main)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_3.sizePolicy().hasHeightForWidth())
        self.frame_3.setSizePolicy(sizePolicy)
        self.frame_3.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.frame_3_layout = QtWidgets.QGridLayout(self.frame_3)
        self.frame_3_layout.setContentsMargins(4, 4, 4, 4)
        self.frame_3_layout.setObjectName("frame_3_layout")
        self.tab_1_layout.addWidget(self.frame_3, 1, 0, 1, 1)
        self.frame_2 = QtWidgets.QFrame(self.tab_main)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_2.sizePolicy().hasHeightForWidth())
        self.frame_2.setSizePolicy(sizePolicy)
        self.frame_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.frame_2_layout = QtWidgets.QGridLayout(self.frame_2)
        self.frame_2_layout.setContentsMargins(4, 4, 4, 4)
        self.frame_2_layout.setObjectName("frame_2_layout")
        self.tab_1_layout.addWidget(self.frame_2, 0, 1, 1, 1)
        self.frame_5 = QtWidgets.QFrame(self.tab_main)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_5.sizePolicy().hasHeightForWidth())
        self.frame_5.setSizePolicy(sizePolicy)
        self.frame_5.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_5.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_5.setObjectName("frame_5")
        self.frame_5_layout = QtWidgets.QGridLayout(self.frame_5)
        self.frame_5_layout.setContentsMargins(0, 0, 0, 0)
        self.frame_5_layout.setHorizontalSpacing(6)
        self.frame_5_layout.setObjectName("frame_5_layout")
        self.camera_view_mini = QtWidgets.QLabel(self.frame_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.camera_view_mini.sizePolicy().hasHeightForWidth())
        self.camera_view_mini.setSizePolicy(sizePolicy)
        self.camera_view_mini.setScaledContents(False)
        self.camera_view_mini.setAlignment(QtCore.Qt.AlignCenter)
        self.camera_view_mini.setObjectName("camera_view_mini")
        self.frame_5_layout.addWidget(self.camera_view_mini, 0, 0, 1, 1)
        self.tab_1_layout.addWidget(self.frame_5, 2, 0, 1, 1)
        self.value_frame = QtWidgets.QFrame(self.tab_main)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.value_frame.sizePolicy().hasHeightForWidth())
        self.value_frame.setSizePolicy(sizePolicy)
        self.value_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.value_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.value_frame.setObjectName("value_frame")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.value_frame)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.value_layout = QtWidgets.QGridLayout()
        self.value_layout.setObjectName("value_layout")
        self.z_val_label = QtWidgets.QLabel(self.value_frame)
        font = QtGui.QFont()
        font.setFamily("Monospace")
        font.setPointSize(36)
        self.z_val_label.setFont(font)
        self.z_val_label.setObjectName("z_val_label")
        self.value_layout.addWidget(self.z_val_label, 1, 0, 1, 1)
        self.x_val_label = QtWidgets.QLabel(self.value_frame)
        font = QtGui.QFont()
        font.setFamily("Monospace")
        font.setPointSize(36)
        self.x_val_label.setFont(font)
        self.x_val_label.setObjectName("x_val_label")
        self.value_layout.addWidget(self.x_val_label, 0, 0, 1, 1)
        self.y_val_label = QtWidgets.QLabel(self.value_frame)
        font = QtGui.QFont()
        font.setFamily("Monospace")
        font.setPointSize(36)
        self.y_val_label.setFont(font)
        self.y_val_label.setObjectName("y_val_label")
        self.value_layout.addWidget(self.y_val_label, 0, 1, 1, 1)
        self.angle_val_label = QtWidgets.QLabel(self.value_frame)
        font = QtGui.QFont()
        font.setFamily("Monospace")
        font.setPointSize(36)
        self.angle_val_label.setFont(font)
        self.angle_val_label.setObjectName("angle_val_label")
        self.value_layout.addWidget(self.angle_val_label, 1, 1, 1, 1)
        self.verticalLayout_2.addLayout(self.value_layout)
        self.command_button = QtWidgets.QPushButton(self.value_frame)
        self.command_button.setObjectName("command_button")
        self.verticalLayout_2.addWidget(self.command_button)
        self.tab_1_layout.addWidget(self.value_frame, 2, 1, 1, 1)
        self.gridLayout_4.addLayout(self.tab_1_layout, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab_main, "")
        self.tab_x = QtWidgets.QWidget()
        self.tab_x.setObjectName("tab_x")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.tab_x)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.tab_x_layout = QtWidgets.QGridLayout()
        self.tab_x_layout.setObjectName("tab_x_layout")
        self.gridLayout_3.addLayout(self.tab_x_layout, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab_x, "")
        self.tab_y = QtWidgets.QWidget()
        self.tab_y.setObjectName("tab_y")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.tab_y)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.tab_y_layout = QtWidgets.QGridLayout()
        self.tab_y_layout.setObjectName("tab_y_layout")
        self.gridLayout_5.addLayout(self.tab_y_layout, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab_y, "")
        self.tab_z = QtWidgets.QWidget()
        self.tab_z.setObjectName("tab_z")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.tab_z)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.tab_z_layout = QtWidgets.QGridLayout()
        self.tab_z_layout.setObjectName("tab_z_layout")
        self.gridLayout_6.addLayout(self.tab_z_layout, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab_z, "")
        self.tab_a = QtWidgets.QWidget()
        self.tab_a.setObjectName("tab_a")
        self.gridLayout_7 = QtWidgets.QGridLayout(self.tab_a)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.tab_a_layout = QtWidgets.QGridLayout()
        self.tab_a_layout.setObjectName("tab_a_layout")
        self.gridLayout_7.addLayout(self.tab_a_layout, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab_a, "")
        self.tab_c = QtWidgets.QWidget()
        self.tab_c.setObjectName("tab_c")
        self.gridLayout_8 = QtWidgets.QGridLayout(self.tab_c)
        self.gridLayout_8.setObjectName("gridLayout_8")
        self.tab_c_layout = QtWidgets.QGridLayout()
        self.tab_c_layout.setObjectName("tab_c_layout")
        self.camera_view = QtWidgets.QLabel(self.tab_c)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.camera_view.sizePolicy().hasHeightForWidth())
        self.camera_view.setSizePolicy(sizePolicy)
        self.camera_view.setScaledContents(False)
        self.camera_view.setAlignment(QtCore.Qt.AlignCenter)
        self.camera_view.setObjectName("camera_view")
        self.tab_c_layout.addWidget(self.camera_view, 0, 0, 1, 1)
        self.gridLayout_8.addLayout(self.tab_c_layout, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab_c, "")
        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 3)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1600, 22))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.menubar.sizePolicy().hasHeightForWidth())
        self.menubar.setSizePolicy(sizePolicy)
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # Begin custom adjustments
        self.plot_pen = pg.mkPen('g', width=2)

        self.plot_1_parent = pg.PlotWidget(MainWindow)
        configure_plot(self.plot_1_parent, -20, 20, 'X Position (in) vs. Time (s)', 'Time (s)', 'X Position (in)',
                       True, 60, 15, 10, 1, 255, 255)
        self.tab_x_layout.addWidget(self.plot_1_parent)
        self.plot_1 = self.plot_1_parent.plot([1])
        self.plot_1a = self.plot_1_parent.plot([1])
        self.plot_1_mini = pg.PlotWidget(MainWindow)
        configure_plot(self.plot_1_mini, -20, 20, 'X Position (in) vs. Time (s)', 'Time (s)', 'X Position (in)',
                       True, 60, 15, 10, 1, 255, 255)
        self.frame_1_layout.addWidget(self.plot_1_mini)
        self.plot_1_mini = self.plot_1_mini.plot([0])

        self.plot_2_parent = pg.PlotWidget(MainWindow)
        configure_plot(self.plot_2_parent, -20, 20, 'Y Position (in) vs. Time (s)', 'Time (s)', 'Y Position (in)',
                       True, 60, 15, 10, 1, 255, 255)
        self.tab_y_layout.addWidget(self.plot_2_parent)
        self.plot_2 = self.plot_2_parent.plot([1])
        self.plot_2a = self.plot_2_parent.plot([1])
        self.plot_2_mini = pg.PlotWidget(MainWindow)
        configure_plot(self.plot_2_mini, -20, 20, 'Y Position (in) vs. Time (s)', 'Time (s)', 'Y Position (in)',
                       True, 60, 15, 10, 1, 255, 255)
        self.frame_2_layout.addWidget(self.plot_2_mini)
        self.plot_2_mini = self.plot_2_mini.plot([0])

        self.plot_3_parent = pg.PlotWidget(MainWindow)
        configure_plot(self.plot_3_parent, args['range_min'], args['range_max'], 'Z Position (in) vs. Time (s)',
                       'Time (s)', 'Z Position (in)', True, 60, 15, 10, 1, 255, 255)
        self.tab_z_layout.addWidget(self.plot_3_parent)
        self.plot_3 = self.plot_3_parent.plot([1])
        self.plot_3a = self.plot_3_parent.plot([1])
        self.plot_3_mini = pg.PlotWidget(MainWindow)
        configure_plot(self.plot_3_mini, args['range_min'], args['range_max'], 'Z Position (in) vs. Time (s)',
                       'Time (s)', 'Z Position (in)', True, 60, 15, 10, 1, 255, 255)
        self.frame_3_layout.addWidget(self.plot_3_mini)
        self.plot_3_mini = self.plot_3_mini.plot([0])

        self.plot_4_parent = pg.PlotWidget(MainWindow)
        configure_plot(self.plot_4_parent, -20, 20, 'Angle (degrees) vs. Time (s)', 'Time (s)', 'Angle (deg)',
                       True, 60, 15, 10, 1, 255, 255)
        self.tab_a_layout.addWidget(self.plot_4_parent)
        self.plot_4 = self.plot_4_parent.plot([1])
        self.plot_4a = self.plot_4_parent.plot([1])
        self.plot_4_mini = pg.PlotWidget(MainWindow)
        configure_plot(self.plot_4_mini, -20, 20, 'Angle (degrees) vs. Time (s)', 'Time (s)', 'Angle (deg)',
                       True, 60, 15, 10, 1, 255, 255)
        self.frame_4_layout.addWidget(self.plot_4_mini)
        self.plot_4_mini = self.plot_4_mini.plot([0])

        self.plots = [self.plot_1, self.plot_2, self.plot_3, self.plot_4]
        self.plotsa = [self.plot_1a, self.plot_2a, self.plot_3a, self.plot_4a]
        self.plots_mini = [self.plot_1_mini, self.plot_2_mini, self.plot_3_mini, self.plot_4_mini]
        self.data_labels = [self.x_val_label, self.y_val_label, self.z_val_label, self.angle_val_label]

        self.x_val = 0.0
        self.y_val = 0.0
        self.z_val = 0.0
        self.a_val = 0.0

        # create the video capture thread
        self.thread = Analysis.Analysis(args)
        # connect its camera view signal to the update_image slot
        self.thread.change_image_signal.connect(self.update_image)
        # connect its plot view signal to the update_plot slot
        self.thread.change_plot_signal.connect(self.update_plot)
        # start the thread
        self.thread.start()

        self.ranger = Range.Range(args)
        self.all_z_data = []

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Ship Strain Measurement System"))
        self.camera_view_mini.setText(_translate("MainWindow", "Loading"))
        self.z_val_label.setText(_translate("MainWindow", "Z: +0.0000"))
        self.x_val_label.setText(_translate("MainWindow", "X: +0.0000"))
        self.y_val_label.setText(_translate("MainWindow", "Y: +0.0000"))
        self.angle_val_label.setText(_translate("MainWindow", "A: +0.0000"))
        self.command_button.setText(_translate("MainWindow", "Start Analysis"))
        self.command_button.clicked.connect(self.button_click)
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_main), _translate("MainWindow", "Overview"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_x), _translate("MainWindow", "X Axis"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_y), _translate("MainWindow", "Y Axis"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_z), _translate("MainWindow", "Z Axis"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_a), _translate("MainWindow", "Angle"))
        self.camera_view.setText(_translate("MainWindow", "Loading"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_c), _translate("MainWindow", "Camera"))
        self.fill_data([1, np.nan, 0])

    def convert_cv_qt(self, cv_img, scaled=False):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        if scaled:
            convert = convert.scaled(self.camera_view_mini.geometry().width(),
                                     self.camera_view_mini.geometry().height(),
                                     QtCore.Qt.KeepAspectRatio)
        return QPixmap.fromImage(convert)

    def update_image(self, cv_img):
        """Updates the image_label with a new opencv image"""
        qt_img = self.convert_cv_qt(cv_img)
        qt_img_s = self.convert_cv_qt(cv_img, scaled=True)
        self.camera_view.setPixmap(qt_img)
        self.camera_view_mini.setPixmap(qt_img_s)

    def fill_data(self, data):
        chunks = []
        start = 0
        found = False
        for i in range(len(data)):
            if np.isnan(data[i]) and not found:
                found = True
                start = i
            elif not np.isnan(data[i]) and found:
                found = False
                chunks.append([start, i - 1])
        if found is True:
            chunks.append([start, len(data) - 1])
        for chunk in chunks:
            if chunk[0] > 0 and chunk[1] < len(data) - 1:
                slope = (data[chunk[1] + 1] - data[chunk[0] - 1]) / ((chunk[1] + 1) - (chunk[0] - 1))
                for i in range(chunk[0], chunk[1] + 1):
                    data[i] = data[i - 1] + slope
            elif chunk[0] == 0 or chunk[1] == len(data) - 1:
                for i in range(chunk[0], chunk[1] + 1):
                    data[i] = 0
        return data

    def update_plot(self, plot, data):
        self.plot_original(plot, np.copy(data))
        self.plot_sg(plot, np.copy(data))
        self.update_data_label(plot, np.copy(data))
        if plot == 0:
            self.update_z_plot()

    def plot_sg(self, plot, data):
        data = self.fill_data(data.flat)
        data = savgol_filter(data, 15, 3)
        x = np.arange(start=(len(data) / 10 + 1), stop=1, step=-0.1)
        self.plots[plot].setData(x, data, pen=self.plot_pen)
        self.plots_mini[plot].setData(x, data, connect="finite", pen=self.plot_pen)

    def plot_original(self, plot, data):
        self.plotsa[plot].setData(np.arange(start=(len(data.flat) / 10 + 1), stop=1, step=-0.1), data.flat,
                                  connect="finite", pen=pg.mkPen('r', width=1))

    def update_data_label(self, label_index, data):
        if type(data) is np.ndarray:
            last_val = data.flat[-1]
        else:
            last_val = data[-1]
        if not np.isnan(last_val):
            lookup = ['X', 'Y', 'Z', 'A']
            if label_index == 0:
                self.x_val = last_val
            elif label_index == 1:
                self.y_val = last_val
            elif label_index == 2:
                self.z_val = last_val
            elif label_index == 3:
                self.a_val = last_val
            text = '{0}: {1:+.4f}'.format(lookup[label_index], last_val)
            self.data_labels[label_index].setText(text)

    def button_click(self):
        current_state = self.thread.get_state()
        _translate = QtCore.QCoreApplication.translate
        if current_state:
            self.command_button.setText(_translate("MainWindow", "Pause Analysis"))
        else:
            self.command_button.setText(_translate("MainWindow", "Pause Analysis"))
        self.thread.set_state(not current_state)

    def update_z_plot(self):
        val = self.ranger.read()
        self.all_z_data.append(val)
        if len(self.all_z_data) > 300:
            self.all_z_data.pop(0)
        self.update_data_label(2, self.all_z_data)
        p1 = np.arange(start=(len(self.all_z_data) / 10 + 1), stop=1, step=-0.1)
        p2 = p1
        if len(p1) > len(self.all_z_data):
            p2 = p1[:-1].copy()
        self.plotsa[2].setData(p2, self.all_z_data, connect="finite", pen=pg.mkPen('r', width=1))
        data = savgol_filter(self.all_z_data, 21, 4)
        x = np.arange(start=(len(data) / 10 + 1), stop=1, step=-0.1)
        self.plots[2].setData(p2, data, pen=self.plot_pen)
        self.plots_mini[2].setData(p2, data, connect="finite", pen=self.plot_pen)


class Display:
    def __init__(self, args):
        super().__init__()

        app = QtWidgets.QApplication(sys.argv)
        main = QtWidgets.QMainWindow()
        ui = Ui_MainWindow(main, args)
        main.show()

        sys.exit(app.exec_())
