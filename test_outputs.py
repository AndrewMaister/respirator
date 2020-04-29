# -*- coding: utf-8 -*-
try:
    from pyfirmata import Arduino, util
except Exception as e:
    print e
    import pip
    pip.main(['install', 'pyfirmata'])
    from pyfirmata import Arduino, util
import time
import sys, argparse


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


def go_to_sleep(seconds):
    print("Going to sleep for {}".format(seconds))
    time.sleep(seconds)


def go_to_sleep(seconds):
    time.sleep(seconds)
    print("Waiting {} seconds..".format(seconds))


def main(args):
    args = parse_args(args)
    if args.usb is None:
        print("Please enter usb serial")
        exit()
    print("")
    BOARD = Arduino(args.usb)
    output_d_pins = [8, 9 ,10 ,11 ,12 ,13]
    print("Starting outputs test in 15 seconds.. ")
    go_to_sleep(15)
    for d_pin in output_d_pins:
        print("Pin {} set to 1 for 10 seconds..".format(d_pin))
        pin = BOARD.get_pin('d:{}:o'.format(d_pin))
        pin.write(1)
        go_to_sleep(10)


def run():
    main(sys.argv[1:])


if __name__ == "__main__":
    run()