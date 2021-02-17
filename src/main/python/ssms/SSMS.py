
from PyQt5.QtWidgets import QApplication

from ssms import Analysis
from ssms import Display


class SSMS:
    """
    Uses computer vision to perform strain measurement calculations.
    """
    def __init__(self, args):
        print('Creating analysis object.')
        self.display = Display.Display(args)
