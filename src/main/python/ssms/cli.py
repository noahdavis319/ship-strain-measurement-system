
import sys
import argparse

from ssms import SSMS
from ssms import utils


def cli():
    """
    The entry point to SSMS.
    """
    parser = argparse.ArgumentParser(description='Perform strain measurement calculations using computer vision.')
    parser.add_argument("-i", "--image", required=True, help="The image to analyze")
    parser.add_argument("-t_min", "--triangle-min", required=False, type=int, default=0,
                        help="The minimum triangle area")
    parser.add_argument("-t_max", "--triangle-max", required=False, type=int, default=sys.maxsize,
                        help="The maximum triangle area")
    parser.add_argument("-p_min", "--plus-min", required=False, type=int, default=0, help="The minimum plus area")
    parser.add_argument("-p_max", "--plus-max", required=False, type=int, default=sys.maxsize,
                        help="The maximum plus area")
    parser.add_argument("-s", "--scale", required=False, type=int, default=50, help="Scaled image size")
    parser.add_argument("-c", "--com", required=True, type=str, help="LIDAR COM port")
    parser.add_argument("-b", "--baud", required=False, type=int, default=115200, help="LIDAR COM baudrate")
    parser.add_argument("-ps", "--plus-stroke", required=True, type=float, help="Plus target stroke")
    parser.add_argument("-pw", "--plus-width", required=True, type=float, help="Plus target width")
    parser.add_argument("-rmin", "--range-min", required=False, type=float, default=0,
                        help="Minimum range value for plotting (cm)")
    parser.add_argument("-rmax", "--range-max", required=False, type=float, default=100,
                        help="Maximum range value for plotting (cm)")
    args = vars(parser.parse_args())

    _run(args)


def _list():
    utils.list_cameras()


def _run(args):
    print("Starting analysis on device 0.")
    ssms = SSMS.SSMS(args)


if __name__ == "__main__":
    cli()
