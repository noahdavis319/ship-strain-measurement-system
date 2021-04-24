import sys
import time
from enum import Enum
from itertools import combinations

import cv2
import imutils
import numpy as np
from PyQt5.QtCore import pyqtSignal, QThread

from ssms.BufferedCamera import BufferedCamera
from ssms.timing import timer, print_timing_results

times = {
    'tri-filt': [],
    'dod-filt': [],
    'clck-ord': [],
    'sqr-test': [],
    'ang-test': [],
    'pnt-cntn': []
}

sum_times = {
    'tri-filt': [],
    'dod-filt': [],
    'clck-ord': [],
    'sqr-test': [],
    'ang-test': [],
    'pnt-cntn': []
}

frame_times = []

all_delta_x = np.empty((1, 3000, ))
all_delta_x[:] = np.nan
all_delta_y = np.empty((1, 3000, ))
all_delta_y[:] = np.nan
all_delta_a = np.empty((1, 3000, ))
all_delta_a[:] = np.nan


class Shape(Enum):
    TRIANGLE = 1
    PLUS = 2


@timer
class ContourObject:
    def __init__(self, contour):
        self.contour = contour
        (self.shape, self.approx) = detect_shape(self.contour)
        self.verts = len(self.approx)
        self.moment, self.cX, self.cY = calc_contour_center(self.contour)
        self.valid = False if self.moment is False else True
        self.area = self.min_rect = self.box = self.angle = None

    @timer
    def calc(self):
        self.area = cv2.contourArea(self.contour)
        self.min_rect = cv2.minAreaRect(self.contour)
        self.box = np.intp(cv2.boxPoints(self.min_rect))
        self.angle = ((float(self.min_rect[2]) - 45) * - 1)


@timer
def calc_contour_center(contour):
    m = cv2.moments(contour)

    try:
        cx = int((m["m10"] / m["m00"]))
        cy = int((m["m01"] / m["m00"]))
    except ZeroDivisionError:
        return False, False, False

    return m, cx, cy


@timer
def detect_shape(c):
    shape = None
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.03 * peri, True)  # Ramer-Douglas-Peucker algorithm
    if len(approx) == 3:
        shape = Shape.TRIANGLE
    elif len(approx) == 12:
        shape = Shape.PLUS

    return shape, approx


@timer
def get_bounding_box_of_contours(contours):
    points = []
    for c in contours:
        for p in c.approx:
            points.append([p[0][0], p[0][1]])
    points = np.array(points, np.int32)
    mar = cv2.minAreaRect(points)
    box = cv2.boxPoints(mar)
    box = np.intp(box)

    return box


@timer
def create_box_from_contours(contours):
    box = []
    for co in contours:
        box.append([co.cX, co.cY])

    box = np.intp(box)

    return box


@timer
def calc_movement(box, l_origin, r_origin, angle, ps, pw):
    # a = 16 + 2.950354609929078  # these values should come from a configuration file
    a = ps + pw

    area = cv2.contourArea(box)
    diag_dist = np.sqrt(2 * area)
    cval = float(a) / diag_dist
    box_moments = cv2.moments(box)
    new_origin_px = (int((box_moments["m10"] / box_moments["m00"])), int((box_moments["m01"] / box_moments["m00"])))

    new_r_origin_x = r_origin[0]
    new_r_origin_y = r_origin[1]
    ret_text = ''
    if l_origin is not None:
        delta_x = -1 * (l_origin[0] - new_origin_px[0]) * cval
        delta_y = (l_origin[1] - new_origin_px[1]) * cval
        new_r_origin_x = r_origin[0] + delta_x
        new_r_origin_y = r_origin[1] + delta_y

        global all_delta_x
        global all_delta_y
        global all_delta_a
        all_delta_x = np.insert(all_delta_x, all_delta_x.size, new_r_origin_x, axis=1)
        all_delta_x = np.delete(all_delta_x, 0, axis=1)
        all_delta_y = np.insert(all_delta_y, all_delta_y.size, new_r_origin_y, axis=1)
        all_delta_y = np.delete(all_delta_y, 0, axis=1)
        all_delta_a = np.insert(all_delta_a, all_delta_a.size, angle, axis=1)
        all_delta_a = np.delete(all_delta_a, 0, axis=1)

        ret_text = 'x: {:<+8.4f} y: {:<+8.4f} a: {:<+8.4f} c: {:>.4f}/{:<.4f}'.format(round(new_r_origin_x, 4),
                                                                                      round(new_r_origin_y, 4),
                                                                                      angle, cval, 1.0 / cval)

    return new_origin_px, (new_r_origin_x, new_r_origin_y, angle), ret_text


def order_triangles_old(triangles, image_size):
    lookup = [(0, 0),  # top left
              (image_size[0] - 1, 0),  # top right
              (image_size[0] - 1, image_size[1] - 1),  # bottom right
              (0, image_size[1] - 1)]  # bottom left
    ordered_triangles = triangles.copy()
    for i in [0, 1, 2, 3]:
        for j in [0, 1, 2, 3]:
            if calc_distance(lookup[i], (triangles[j].cX, triangles[j].cY)) < calc_distance(lookup[i], (
                    ordered_triangles[i].cX, ordered_triangles[i].cY)):
                ordered_triangles[i] = triangles[j]

    return ordered_triangles


@timer
def order_triangles(triangles):
    ordered = [None, None, None, None]

    center = [(triangles[0].cX + triangles[1].cX + triangles[2].cX + triangles[3].cX) / 4,
              (triangles[0].cY + triangles[1].cY + triangles[2].cY + triangles[3].cY) / 4]

    for t in triangles:
        if t.cX <= center[0] and t.cY <= center[1]:
            ordered[0] = t
        if t.cX <= center[0] and t.cY >= center[1]:
            ordered[3] = t
        if t.cX >= center[0] and t.cY <= center[1]:
            ordered[1] = t
        if t.cX >= center[0] and t.cY >= center[1]:
            ordered[2] = t

    return ordered if not None in ordered else None


@timer
def is_target_found(plus, triangles):
    print('-----')
    found = do_contours_make_square(triangles, tolerance=0.1) and \
	        do_contours_align_to(triangles, plus, tolerance=16.0) and \
            does_plus_lie_in_triangles(plus, triangles) 
    if found:
        print("TARGET FOUND!")
    return found

@timer
def does_plus_lie_in_triangles(plus, triangles):
    triangles_box = create_box_from_contours(triangles)

    a = is_plus_centered(plus, triangles_box) and \
           is_contour_in_box(plus, triangles_box) and \
           is_contour_in_box(plus, get_bounding_box_of_contours(triangles))
	   
    if a:
        print("Plus lies within")
    else:
        print("Plus does not lie")
		
    return a

@timer
def is_plus_centered(plus, triangles_box):
    M, cX, cY = calc_contour_center(triangles_box)
    return val_close_to(cX, plus.cX, 0.1) and val_close_to(cY, plus.cY, 0.1)


@timer
def is_contour_in_box(contour, box):
    for point in contour.approx:
        if cv2.pointPolygonTest(box, tuple(point[0]), measureDist=False) != 1:
            return False

    return True


@timer
def is_contour_plus(contour):
    segments = []
    for i in [0, 4, 8]:
        segment_lengths = []
        for ia in [1, 2, 3]:
            segment_lengths.append(calc_distance(contour.approx[i + ia - 1], contour.approx[i + ia]))
        segment_lengths.sort()
        segments.append(segment_lengths)

    master_segment = segments[0]
    for ia in [1, 2]:
        test_segment = segments[ia]
        for ib in [0, 1, 2]:
            if not val_close_to(master_segment[ib], test_segment[ib], vtol=0.1):
                return False

    return True


@timer
def is_contour_isosceles_right_triangle(contour):
    lengths = [
        calc_distance(contour.approx[0], contour.approx[1]),
        calc_distance(contour.approx[1], contour.approx[2]),
        calc_distance(contour.approx[2], contour.approx[0])
    ]
    lengths.sort()

    return val_close_to(np.hypot(lengths[0], lengths[1]), lengths[2], 0.1)


@timer
def calc_distance(pointA, pointB):
    return np.linalg.norm(np.array(pointA) - np.array(pointB))


@timer
def calc_hypotenuse(x):
    return np.sqrt(x ** 2 + x ** 2)


@timer
def val_close_to(valA, valB, ptol=0.05, vtol=0):
    return ((valB * (1 - ptol)) < valA < (valB * (1 + ptol))) or ((valB - vtol) < valA < (valB + vtol))


@timer
def do_contours_make_square(contours, tolerance=0.05):
    if len(contours) > 4:
        print('This function does not support more than 4 contours')
        sys.exit(1)

    centers = []
    for co in contours:
        centers.append([co.cX, co.cY])

    d1 = calc_distance(centers[0], centers[1])  # top left & top right
    d2 = calc_distance(centers[0], centers[2])  # top left & bottom right
    d3 = calc_distance(centers[0], centers[3])  # top left & bottom left

    if val_close_to(d1, d3, tolerance) and \
            val_close_to(d2, calc_hypotenuse(d1), tolerance) and \
            val_close_to(d2, calc_hypotenuse(d3), tolerance):
        print("Contours make square")
        return True
    print("Contours do not make square")
    return False


@timer
def do_contours_align_to(contours, contour, tolerance=8.0):
    angles = []
    for co in contours:
        angles.append((co.angle - contour.angle) % 45)
    for angle in angles:
        if not (angle <= tolerance or 45 - angle <= tolerance):
            print("Out of alignment")
            return False
    print("In alignment")
    return True


def draw_text_with_snow(img, text, row=0):
    cv2.putText(img, text, (4, 16 * (row + 1)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(img, text, (4, 16 * (row + 1)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)


def draw_target_angle_lines(img, co, theta):
    tan = np.tan(np.deg2rad(theta))
    tan2 = np.tan(np.deg2rad(-1 * theta))

    top_diff = int(tan * co.cY)
    bot_diff = int(tan * (img.shape[0] - 1 - co.cY))
    start = (int(co.cX - top_diff), 0)
    stop = (int(co.cX + bot_diff), img.shape[0] - 1)
    cv2.line(img, start, (co.cX, co.cY), (255, 255, 0), 1)
    cv2.line(img, stop, (co.cX, co.cY), (255, 255, 0), 1)

    top_diff2 = int(tan2 * co.cX)
    bot_diff2 = int(tan2 * (img.shape[1] - 1 * co.cX))
    start2 = (0, int(co.cY - top_diff2))
    stop2 = (img.shape[1] - 1, int(co.cY + bot_diff2))
    cv2.line(img, start2, (co.cX, co.cY), (255, 255, 0), 1)
    cv2.line(img, stop2, (co.cX, co.cY), (255, 255, 0), 1)


def draw_box(img, box):
    cv2.drawContours(img, [box], 0, (127, 127, 255), 1)


def draw_target_outline(img, contours):
    cv2.drawContours(img, [get_bounding_box_of_contours(contours)], 0, (127, 127, 255), 1)


def draw_vertex_points(img, co):
    for vert in co.approx:
        cv2.circle(img, (vert[0][0], vert[0][1]), radius=2, color=(0, 0, 255), thickness=-1)


def draw_contour_outline(img, co):
    cv2.drawContours(img, [co.approx], -1, (0, 255, 0), 2)
    cv2.putText(img, str(co.verts), (co.cX, co.cY), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)


def draw_contour_rect(img, box):
    cv2.drawContours(img, [box], 0, (255, 0, 0), 1)


@timer
def get_image(capture_device, scale_percent=50):
    src = capture_device.read()

    if len(src) == 2:
        src = src[1]

    try:
        # calculate the 50 percent of original dimensions
        width = int(src.shape[1] * scale_percent / 100)
        height = int(src.shape[0] * scale_percent / 100)

        # dsize
        dsize = (width, height)

        # resize image
        image = cv2.resize(src, dsize)
    except AttributeError:
        image = src

    return image


@timer
def get_contours(image):
    if image is not None:
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        lower = np.array([0, 0, 00], np.uint8)  # 0 0 80 - black (0,0,0 for blue) 
        upper = np.array([179, 66, 255], np.uint8) # (179,255,255 for black) (179,66,255 for blue)
        mask = cv2.inRange(hsv, lower, upper)
        blur = cv2.GaussianBlur(mask, (5, 5), 0)
        thresh = cv2.threshold(blur, 100, 255, cv2.THRESH_BINARY_INV)[1]
        contours, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        # contours = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        contours = imutils.grab_contours((contours, hierarchy))

        return True, contours, image, cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)

    return False, None, None, None


@timer
def fast_contour_filter(contour, last_contours, r=4.0):
    for lcontour in last_contours:
        dist = calc_distance((contour.cX, contour.cY), (lcontour.cX, lcontour.cY))
        # print(dist, r, contour.verts, lcontour.verts, contour.cX, contour.cY, lcontour.cX, lcontour.cY)
        if dist < r:
            return True

    return False


class Analysis(QThread):
    """
    Performs computer vision analysis.

    Uses the first camera device detected by OpenCV.
    """

    change_image_signal = pyqtSignal(np.ndarray)
    change_plot_signal = pyqtSignal(int, np.ndarray)

    def __init__(self, args):
        super().__init__()
        self.args = args
        self.device = BufferedCamera(args['image'])  # cv2.VideoCapture(args['image'])  # BufferedCamera(args['image'])
        self._run_flag = True
        self.tdata = []
        self.frame_num = 0
        self.o_start = None
        self.last_origin_px = None
        self.running_origin = (0, 0, 0)
        self.area_map = {
            3: [args['triangle_min'], args['triangle_max']],
            12: [args['plus_min'], args['plus_max']]
        }
        self.frame_time = 0
        self.start_pos = [258, 258]
        self.last_contours = []
        self.out = cv2.VideoWriter('out.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 60, (1920, 1080))

    def run(self):
        print("Starting")
        self.o_start = time.time()
        while True:
            if self._run_flag:
                self.perf_analysis()
            # else:
            #    self.send_frame()

    def set_state(self, state):
        self._run_flag = state

    def get_state(self):
        return self._run_flag

    def stop(self):
        self._run_flag = False
        self.wait()

    def send_frame(self):
        self.frame_num = self.frame_num + 1
        ret, contours, image, mask = get_contours(get_image(self.device, self.args['scale']))
        self.change_image_signal.emit(image)

    @timer
    def perf_analysis(self):
        self.frame_num = self.frame_num + 1
        ret, contours, image, mask = get_contours(get_image(self.device, self.args['scale']))
        start = time.time()
        if ret and (image is not None) and (len(contours) > 0):
            image2 = image.copy()

            draw_on = [image2]

            triangles = []
            pluses = []

            rr = 4
            fast_filter = []
            all_co = []
            for c in contours:
                co = ContourObject(c)
                #draw_contour_outline(image2, co)
                if co.valid:
                    all_co.append(co)
                    if len(self.last_contours) > 0:
                        fc = fast_contour_filter(co, self.last_contours, r=rr)
                        if fc:
                            fast_filter.append(co)
            filter_test = len(fast_filter) == 5
            if not filter_test:
                for co in all_co:
                    # determine if shape is triangle or plus and meets the area requirements
                    if co.verts in self.area_map:
                        co.calc()  # calc additional variables only for shapes that are triangles or pluses
                        if self.area_map[co.verts][0] < co.area < self.area_map[co.verts][1]:
                            if co.verts == 3: # and is_contour_isosceles_right_triangle(co):
                                triangles.append(co)
                                draw_contour_outline(image2, co)
                            elif co.verts == 12: # and is_contour_plus(co):
                                pluses.append(co)
                                draw_contour_outline(image2, co)
            else:
                for co in fast_filter:
                    co.calc()
                    if co.verts == 3:
                        triangles.append(co)
                    elif co.verts == 12:
                        pluses.append(co)

            target_found = False
            for plus in pluses:
                combs = combinations(triangles, 4)
                for comb in combs:
                    comb_triangles = order_triangles(list(comb))
                    try:
                        if comb_triangles is not None:
                            if is_target_found(plus, comb_triangles):
                                frame_time = (time.time() - start) * 1000
                                frame_times.append(frame_time)
                                all_contours = comb_triangles + [plus]

                                last_contours = all_contours.copy()

                                for co in last_contours:
                                    for img in draw_on:
                                        cv2.circle(img, (co.cX, co.cY), radius=rr, color=(0, 0, 255), thickness=-1)

                                for co in all_contours:
                                    for img in draw_on:
                                        try:
                                            draw_contour_outline(img, co)  # green
                                            draw_vertex_points(img, co)  # red
                                            # draw_target_angle_lines(img, co, co.angle)  # teal
                                            draw_contour_rect(img, co.box)  # blue
                                            draw_target_outline(img, all_contours)  # salmon

                                            if co.shape == Shape.PLUS:
                                                self.last_origin_px, \
                                                self.running_origin, \
                                                ret_text = calc_movement(co.box,
                                                                         self.last_origin_px,
                                                                         self.running_origin,
                                                                         co.angle,
                                                                         self.args['plus_width'],
                                                                         self.args['plus_stroke'])
                                                self.tdata.append('{0},{1},{2},{3}'.format(self.frame_num,
                                                                                           self.running_origin[0],
                                                                                           self.running_origin[1],
                                                                                           self.running_origin[2]))
                                                draw_text_with_snow(img, '{0}'.format(ret_text), row=0)
                                                # draw_text_with_snow(img, 'algo-time: {:<.4f} ms'.format(frame_time),
                                                #                     row=1)
                                                # draw_text_with_snow(img, 'offset: ({0}, {1}) px'.format(
                                                #     plus.cX - self.start_pos[0], plus.cY - self.start_pos[1]), row=2)

                                        except Exception as e:
                                            print(e)

                                target_found = True
                                break  # found the target board, no need to try the rest of the combinations

                    except ZeroDivisionError as zde:
                        print("ZDE")
                        pass  # ignore ZDE errors
                    except Exception as e:
                        print(e)

                    if target_found:
                        break
                if target_found:
                    break

            if not target_found:
                global all_delta_x
                global all_delta_y
                global all_delta_a
                all_delta_x = np.insert(all_delta_x, all_delta_x.size, np.nan, axis=1)
                all_delta_x = np.delete(all_delta_x, 0, axis=1)
                all_delta_y = np.insert(all_delta_y, all_delta_y.size, np.nan, axis=1)
                all_delta_y = np.delete(all_delta_y, 0, axis=1)
                all_delta_a = np.insert(all_delta_a, all_delta_a.size, np.nan, axis=1)
                all_delta_a = np.delete(all_delta_a, 0, axis=1)

            # end = time.time() - start
            # print(end * 1000)

            self.out.write(image2)

            for p in times.keys():
                sum_frame = np.sum(times[p])
                sum_times[p].append(sum_frame)
                times[p] = []

            # send Qt signal to display
            # self.change_image_signal.emit(mask2, 4)
            self.change_image_signal.emit(image2)
            self.change_plot_signal.emit(0, all_delta_x)
            self.change_plot_signal.emit(1, all_delta_y)
            self.change_plot_signal.emit(3, all_delta_a)

        # try:
        #     # print_timing_results()
        #     print('\nAverage frame-time: {0}'.format(np.average(frame_times)))
        #     print('Minimum frame-time: {0}'.format(np.min(frame_times)))
        #     print('Maximum frame-time: {0}'.format(np.max(frame_times)))
        # except ValueError:
        #     pass

        # show the output image
        # cv2.imshow("Image", image2)
        # key = cv2.waitKey(100)
        # if key == 27:
        #    return
