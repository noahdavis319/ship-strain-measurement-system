
from PyQt5.QtWidgets import QApplication

from ssms import Analysis
from ssms import Display


class SSMS:
    """
    Uses computer vision to perform strain measurement calculations.
    """
    def __init__(self):
        print('Creating analysis object.')
        # self.analysis = Analysis.Analysis()
        app = QApplication([])
        self.display = Display.Display()
        self.display.show()
        app.exec_()
