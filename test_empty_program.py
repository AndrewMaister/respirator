# -*- coding: utf-8 -*-
try:
    from pyfirmata import Arduino, util
except Exception as e:
    print e
    import pip
    pip.main(['install', 'pyfirmata'])
    from pyfirmata import Arduino, util
import sys, argparse
import time


def parse_args(args):
    parser = argparse.ArgumentParser(description="Test mode")
    parser.add_argument(
        '-usb',
        '--usb-serial',
        dest="usb",
        help="The name of the USB serial",
        action='store',
        type=str
    )
    return parser.parse_args(args)


def main(args):
    args = parse_args(args)
    if args.usb is None:
        print("Please enter usb serial")
        exit()
    board = Arduino(args.usb)
    print("Testing empty program... going to sleep for 60 seconds")
    time.sleep(60)


def run():
    main(sys.argv[1:])


if __name__ == "__main__":
    run()