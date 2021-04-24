
import serial
import queue
import threading
import time
import numpy

class Range:
    def __init__(self, args):
        self.arduinoSerialData = serial.Serial(args['com'], args['baud'])

        while self.arduinoSerialData.inWaiting() <= 0:
            if self.arduinoSerialData.inWaiting() > 0:
                pass

        self.q = queue.Queue()
        self.t = threading.Thread(target=self._reader)
        self.t.daemon = True
        self.t.start()
        self.val = numpy.nan

    def _reader(self):
        while True:
            try:
                self.val = float(self.arduinoSerialData.readline()) / 2.54
            except ValueError:
                pass

    def read(self):
        return self.val
