# -*- coding: utf-8 -*-
try:
    from pyfirmata import Arduino, util
except:
    import pip
    pip.main(['install', 'pyfirmata'])
    from pyfirmata import Arduino, util
import time
import sys, argparse
# PORTS: A prefix means analog, D prefix means digital
_PRESSURE_1_DPORT = 2
_PRESSURE_2_DPORT = 3
_PRESSURE_3_DPORT = 4
_PRESSURE_4_DPORT = 5


# valve value convention: 1 open, 0 close
_VALVE_1_1_DPORT = 12
_VALVE_1_2_DPORT = 11
_VALVE_2_DPORT = 10
_VALVE_3_1_DPORT = 9
_VALVE_3_2_DPORT = 8

_MOTOR_DPORT = 13

def set_digital_outputs_to_zero(digital_outputs, motor):
    print("Setting all digital outputs to zero on setup.. ")
    for digital_output in digital_outputs:
	pin = digital_output["pin"]
        pin.write(0)
    motor.write(0)
	


def setup_arduino(USB_SERIAL):
    try:
        BOARD = Arduino(USB_SERIAL)
    except Exception as e:
        print("Error ocurred in USB connection: ")
        print e
        exit()

    iterator = util.Iterator(BOARD)
    iterator.start()
    print("Waiting three seconds for Arduino to set up")
    time.sleep(3)  # wait one second for Arduino to set up

    P1 = BOARD.get_pin('d:{}:i'.format(_PRESSURE_1_DPORT))  # digital, pin number, input (read)
    P2 = BOARD.get_pin('d:{}:i'.format(_PRESSURE_2_DPORT))
    P3 = BOARD.get_pin('d:{}:i'.format(_PRESSURE_3_DPORT))
    P4 = BOARD.get_pin('d:{}:i'.format(_PRESSURE_4_DPORT))

    V1_1 = BOARD.get_pin('d:{}:o'.format(_VALVE_1_1_DPORT))  # digital, pin number, output (write)
    V1_2 = BOARD.get_pin('d:{}:o'.format(_VALVE_1_2_DPORT))
    V2 = BOARD.get_pin('d:{}:o'.format(_VALVE_2_DPORT))
    V3_1 = BOARD.get_pin('d:{}:o'.format(_VALVE_3_1_DPORT))
    V3_2 = BOARD.get_pin('d:{}:o'.format(_VALVE_3_2_DPORT))

    MOTOR = BOARD.get_pin('d:{}:o'.format(_MOTOR_DPORT))

    DIGITAL_OUTPUTS = [{"name": "Valve 1.1", "pin": V1_1},
                       {"name": "Valve 1.2", "pin": V1_2},
                       {"name": "Valve 2", "pin": V2},
                       {"name": "Valve 3.1", "pin": V3_1},
                       {"name": "Valve 3.2", "pin": V3_2}]

    DIGITAL_INPUTS = [{"name": "Sensor 1", "pin": P1}, {"name": "Sensor 2", "pin": P2}, {"name": "Sensor 3", "pin": P3},
                      {"name": "Sensor 4", "pin": P4}]
    set_digital_outputs_to_zero(DIGITAL_OUTPUTS, MOTOR)
    return [MOTOR, DIGITAL_OUTPUTS, DIGITAL_INPUTS, BOARD]


def test_digital_output_connection(pin, time_elapse, name):
    print("{}: Digital output testing write 1 for {} seconds".format(name, time_elapse))
    pin.write(1)
    time.sleep(time_elapse)
    print("Digital output testing end, write 0.".format(time_elapse))
    pin.write(0)


def test_digital_input_connection(pin, time_elapse, name):
    print("Testing {} digital input read. Will wait 8 seconds for digital input estimulation.".format(name))
    time.sleep(8)
    read = pin.read()
    print("{}: Digital input read: {}".format(name, read))
    time.sleep(time_elapse)


def run_valves_and_sensor_test(digital_inputs, digital_outputs):
    print("Always wait for the script to exit by itself to prevent malfunctioning..")
    for digital_input in digital_inputs:
        test_digital_input_connection(digital_input["pin"], 10, digital_input["name"])
    for digital_output in digital_outputs:
        test_digital_output_connection(digital_output["pin"], 10, digital_output["name"])


def run_motor_test(time_elapse, motor):
    test_digital_output_connection(motor, time_elapse, "MOTOR")


def parse_args(args):
    parser = argparse.ArgumentParser(description="Test mode")
    parser.add_argument(
        '-time',
        '--motor',
        dest="time",
        help="Time the motor should be turned on",
        action='store',
        type=str
    )
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
    time_arg = args.time
    usb_serial = args.usb
    if not usb_serial:
        print("You have to insert usb serial name under the -usb tag")
        exit()
    # returns list(MOTOR, DOs, DIs, BOARD)
    pins_and_board = setup_arduino(usb_serial)
    board = pins_and_board[3]
    if time_arg is None:
        print("VALVES AND SENSORS TEST")
        digital_inputs = pins_and_board[2]
        digital_outputs = pins_and_board[1]
        run_valves_and_sensor_test(digital_inputs, digital_outputs)
    else:
        print("MOTORS TEST")
        time_arg = int(time_arg)
        motor = pins_and_board[0]
        run_motor_test(time, motor)
    print("Exiting board.. you can plug out now..")
    board.exit()


def run():
    main(sys.argv[1:])


if __name__ == "__main__":
    run()



