
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
    parser.add_argument("-c", "--com", required=True, type=str, default="com1", help="LIDAR COM port")
    args = vars(parser.parse_args())

    _run(args)


def _list():
    utils.list_cameras()


def _run(args):
    print("Starting analysis on device 0.")
    ssms = SSMS.SSMS(args)


if __name__ == "__main__":
    cli()
