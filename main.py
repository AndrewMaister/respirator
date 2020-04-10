from pyfirmata import Arduino, util
import time

board = Arduino('/dev/tty.usbserial-A6008rIF')
it = util.Iterator(board)
it.start()

# PORTS: A prefix means analog, D prefix means digital
_PRESSURE_1_APORT = 1 # SYSTEM PRESSURE
_PRESSURE_2_APORT = 2 # PATIENT PRESSURE
_PRESSURE_3_APORT = 3 # ??????? PRESSURE

# valve value convention: 1 open, 0 close
_VALVE_1_DPORT = 1
_VALVE_2_DPORT = 2
_ALARM_DPORT = 3 # VISUAL ALARM PORT
_MOTOR_DPORT = 4 #


def switch_valves():
    valve_1 = board.digital[_VALVE_1_DPORT].read()
    valve_2 = board.digital[_VALVE_2_DPORT].read()
    board.digital[_VALVE_1_DPORT].write(1 if valve_1 == 0 else 0)
    board.digital[_VALVE_2_DPORT].write(1 if valve_2 == 0 else 0)


def initial_settings():
    # valve 1 position closed, valve 2 position open
    board.digital[_MOTOR_DPORT].write(0)
    board.digital[_ALARM_DPORT].write(1)
    board.digital[_VALVE_1_DPORT].write(0)
    board.digital[_VALVE_2_DPORT].write(1)


def pressure_alarm():
    # this should be always running
    pressure_1 = board.analog[_PRESSURE_1_APORT].enable_reporting().read()
    if pressure_1 > "30cmH20":
        board.digital[_ALARM_DPORT].write(1)
    else:
        board.digital[_ALARM_DPORT].write(0)


def exhale(pressure_2):
    start_time = time.time()
    switch_valves()
    pressure_3 = board.analog[_PRESSURE_3_APORT].enable_reporting().read()
    while pressure_3 < "5cmH20" or time.time() - start_time >= 3:
        pass
    inhale(pressure_2)


def inhale(pressure_2):
    switch_valves()
    while pressure_2 < "30cmH20":
        board.digital[_MOTOR_DPORT].write(1)
    board.digital[_MOTOR_DPORT].write(0)
    time.sleep(1) # seconds
    exhale(pressure_2)


def start_cycle(pressure_2):
    inhale(pressure_2)


def breathe():
    # Arduino loop
    pressure_2 = board.analog[_PRESSURE_2_APORT].enable_reporting().read()
    if pressure_2 < "1atm":
        start_cycle(pressure_2)


    # ------- PRESSURE CONTROL
    # INITIAL STATUS ON
    # read pressure sensor 1. (sensors alarm in value or we read data stream constantly and evaluate?)
    # if system pressure > 30cmH20 send visual alarm
    # --------
    # ------- BREATHING
    # BREATHING MODE ON
    # read pressure sensor 2. if pressure sensor 2 drops from 1 atm (how much?): INHALATION MODE ON
    # INHALATION MODE: switch valves, turn on motor.
    # when pressure sensor 2 is 30cmH20. turn off motor for 1 second (10 cycle per min cycle)
    # EXHALATION MODE ON
    # EXHALATION MODE: switch valves. read pressure sensor 3. (no motor activity?)
    # if pressure sensor 3 < 5cmH20 or valve_condition.elapse() > 3 seconds.
    # INHALATION MODE ON
    # --------

initial_settings()
while True:
    breathe()


