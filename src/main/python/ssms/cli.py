
import argparse

from ssms import SSMS
from ssms import utils


def cli():
    """
    The entry point to SSMS.
    """
    parser = argparse.ArgumentParser(description='Perform strain measurement calculations using computer vision.')
    parser.add_argument('cmd', help='the command to run')
    args = parser.parse_args()

    if args.cmd == 'list':
        _list()
    elif args.cmd == 'run':
        _run()


def _list():
    utils.list_cameras()


def _run():
    print("Starting analysis on device 0.")
    ssms = SSMS.SSMS()
