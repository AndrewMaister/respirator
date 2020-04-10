# -*- coding: utf-8 -*-
try:
    from pyfirmata import Arduino, util
except:
    import pip
    pip.main(['install', 'pyfirmata'])
    from pyfirmata import Arduino, util
import time

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

USB_SERIAL = "" # put the name of the usb serial connection (check your PCs control panel)

try:
    board = Arduino(USB_SERIAL)
except Exception as e:
    print("Error ocurred in USB connection: ")
    print e
    exit()

iterator = util.Iterator(board)
iterator.start()

time.sleep(1) # wait one second for Arduino to set up

P1 = board.get_pin('d:{}:i'.format(_PRESSURE_1_DPORT)) # digital, pin number, input (read)
P2 = board.get_pin('d:{}:i'.format(_PRESSURE_2_DPORT))
P3 = board.get_pin('d:{}:i'.format(_PRESSURE_3_DPORT))
P4 = board.get_pin('d:{}:i'.format(_PRESSURE_4_DPORT))

V1_1 = board.get_pin('d:{}:o'.format(_VALVE_1_1_DPORT)) # digital, pin number, output (write)
V1_2 = board.get_pin('d:{}:o'.format(_VALVE_1_2_DPORT))
V2 = board.get_pin('d:{}:o'.format(_VALVE_2_DPORT))
V3_1 = board.get_pin('d:{}:o'.format(_VALVE_3_1_DPORT))
V3_2 = board.get_pin('d:{}:o'.format(_VALVE_3_2_DPORT))


MOTOR = board.get_pin('d:{}:o'.format(_MOTOR_DPORT))

DIGITAL_OUTPUTS = [{"name":"Valve 1.1","pin": V1_1},
                   {"name": "Valve 1.2", "pin": V1_2},
                   {"name": "Valve 2", "pin": V2},
                   {"name": "Valve 3.1", "pin": V3_1},
                   {"name": "Valve 3.2", "pin": V3_2},
                   {"name": "Motor", "pin": MOTOR, "time_elapse": 30}]

DIGITAL_INPUTS = [{"name":"Sensor 1","pin": P1}, {"name":"Sensor 2","pin": P2}, {"name":"Sensor 3","pin": P3}, {"name":"Sensor 4","pin": P4}]


def test_digital_output_connection(pin, time_elapse, name):
    print("{}: Digital output testing write 1 for {} seconds".format(name, time_elapse))
    pin.write(1)
    time.sleep(time_elapse)
    print("Digital output testing end, write 0.".format(time_elapse))
    pin.write(0)


def test_digital_input_connection(pin, time_elapse, name):
    read = pin.read()
    print("{}: Digital input read: {}".format(name, read))
    time.sleep(time_elapse)


print("Always wait for the script to exit by itself to prevent malfunctioning..")

tests = 2
test_counter = 0
while test_counter <= tests:
    test_counter += 1
    print("TEST {}: Testing connections...".format(test_counter))

    for digital_input in DIGITAL_INPUTS:
        test_digital_input_connection(digital_input["pin"], 5, digital_input["name"])

    for digital_output in DIGITAL_OUTPUTS:
        time_elapse = 5
        if "time_elapse" in digital_output:
            time_elapse = digital_output["time_elapse"]
        test_digital_output_connection(digital_output["pin"], time_elapse, digital_output["name"])
    test_sleep = 8
    print("Will restart testing in {} seconds...".format(test_sleep))
    time.sleep(test_sleep)

board.exit()
exit()




