
import cv2
import queue
import threading
import time


class BufferedCamera:
    def __init__(self, name):
        self.name = int(name) if name.isnumeric else name
        self.isfile = True if type(self.name) is str else False
        self.cap = cv2.VideoCapture(self.name)
        if not self.isfile:
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        print(self.isfile)
        print(self.cap)
        self.q = queue.Queue()
        self.t = threading.Thread(target=self._reader)
        self.t.daemon = True
        self.t.start()

    # read frames as soon as they are available, keeping only most recent one
    def _reader(self):
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break
            if not self.q.empty():
                try:
                    self.q.get_nowait()   # discard previous (unprocessed) frame
                except queue.Empty:
                    pass
            self.q.put(frame)
            if self.isfile:
                time.sleep(0.024)

    def read(self):
        return self.q.get()
