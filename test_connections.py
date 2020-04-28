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
# PORTS: A prefix means analog, D prefix means digital
_PRESSURE_1_DPORT = 2 # default 1
_PRESSURE_2_DPORT = 3 # default 0
_PRESSURE_3_DPORT = 5 # patient's mouth default default 0
_PRESSURE_4_DPORT = 4 # default 0

# valve value convention: 1 open (air flow), 0 close (air doesn't flow)
_VALVE_1_1_DPORT = 12
_VALVE_1_2_DPORT = 11
_VALVE_2_DPORT = 8
_VALVE_3_1_DPORT = 10
_VALVE_3_2_DPORT = 9

# IMPORTANT NOTE
# motor should receive 1 only when valve 3.2 and valve 1.2 are 1

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
    VALVE_CONTROLLER = {"1.1": V1_1,
                       "1.2": V1_2,
                       "2":V2,
                       "3.1": V3_1,
                       "3.2": V3_2}

    DIGITAL_INPUTS = [{"name": "Sensor 1", "pin": P1}, {"name": "Sensor 2", "pin": P2}, {"name": "Sensor 3", "pin": P3},
                      {"name": "Sensor 4", "pin": P4}]
    set_digital_outputs_to_zero(DIGITAL_OUTPUTS, MOTOR)
    return [MOTOR, DIGITAL_OUTPUTS, DIGITAL_INPUTS, BOARD, VALVE_CONTROLLER]


def test_digital_output_connection(pin, time_elapse, name):
    print("{}: Digital output testing write 1 for {} seconds".format(name, time_elapse))
    pin.write(1)
    time.sleep(time_elapse)
    print("Digital output testing end, write 0.".format(time_elapse))
    pin.write(0)


def test_digital_input_connection(pin, time_elapse, name):
    print("Testing {} digital input read. Will wait 8 seconds for digital input trigger.".format(name))
    time.sleep(8)
    read = pin.read()
    print("{}: Digital input read: {}".format(name, read))
    time.sleep(time_elapse)


def run_valves_and_sensor_test(digital_inputs, digital_outputs):
    print("Always wait for the script to exit by itself to prevent malfunctioning..")
    print("TESTING DIGITAL INPUTS: ")
    for digital_input in digital_inputs:
        test_digital_input_connection(digital_input["pin"], 10, digital_input["name"])
    print("TESTING DIGITAL OUTPUTS: ")
    for digital_output in digital_outputs:
        test_digital_output_connection(digital_output["pin"], 10, digital_output["name"])


def go_to_sleep_for(seconds):
    time.sleep(seconds)
    print("Waiting {} seconds".format(seconds))


def run_motor_test(motor, valve_controller):
    print("Starting motor test. In 3 seconds valve 3.2 is going to open and test is going to start.. Hang tight..")
    time.sleep(3)
    d_pin_10 = valve_controller["3.2"]
    d_pin_10.write(1)
    print("Valve 3.2 opened..")
    go_to_sleep_for(5)
    d_pin_11 = valve_controller["1.2"]
    d_pin_11.write(1)
    print("Valve 1.2 opened..")
    go_to_sleep_for(15)
    print("Will turn on motor in..")
    for counter in range(3):
        print (3 - counter)
    motor.write(1)
    print("Motor turned on..")
    go_to_sleep_for(5)
    motor.write(0)
    print("Motor turned off")
    go_to_sleep_for(5)
    d_pin_10 = valve_controller["3.2"]
    d_pin_10.write(0)
    print("Valve 3.2 closed..")
    go_to_sleep_for(5)
    d_pin_11 = valve_controller["1.2"]
    d_pin_11.write(0)
    print("Valve 1.2 closed..")


def parse_args(args):
    parser = argparse.ArgumentParser(description="Test mode")
    parser.add_argument(
        '-motor-test',
        '--motor',
        dest="is_motor_test",
        help="Motor test",
        action='store',
        type=bool
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
    is_motor_test = args.is_motor_test
    usb_serial = args.usb
    if not usb_serial:
        print("You have to insert usb serial name under the -usb tag")
        exit()      #0    #1    #2    #3     #4
    # returns list(MOTOR, DOs, DIs, BOARD, VALVE_CONTROLLER)
    pins_and_board = setup_arduino(usb_serial)
    board = pins_and_board[3]
    if is_motor_test is None:
        print("VALVES AND SENSORS TEST")
        digital_inputs = pins_and_board[2]
        digital_outputs = pins_and_board[1]
        run_valves_and_sensor_test(digital_inputs, digital_outputs)
    else:
        print("MOTORS TEST")
        motor = pins_and_board[0]
        valve_controller = pins_and_board[4]
        run_motor_test(motor, valve_controller)
    print("Exiting board.. you can plug out now..")
    board.exit()


def run():
    main(sys.argv[1:])


if __name__ == "__main__":
    run()



