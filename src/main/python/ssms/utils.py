
import cv2


def list_cameras(n=8):
    """
    Tries 0->n camera indexes (default 8) to determine if they're accessible
    """
    found = []

    for i in range(n):
        cap = cv2.VideoCapture(i)
        try:
            cap.read()
            if cap is not None and cap.isOpened():
                found.append(i)
        except Exception:
            cap.release()
            pass

    ret = ''
    for cam in found:
        ret += cam

    print(ret)
    return ret
