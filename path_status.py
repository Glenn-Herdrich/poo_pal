import RPi.GPIO as GPIO
import time
from configparser import ConfigParser

config = ConfigParser()
config.read('status.ini')

TRIGGER =(config.getint('GPIO', 'TRIGGER'))
ECHO = (config.getint('GPIO', 'ECHO'))
min_distance = (config.getint('DOOR', 'min_distance'))
GPIO.setmode(GPIO.BOARD)
GPIO.setup(TRIGGER, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

def path_status():
    GPIO.output(TRIGGER, True)
    time.sleep(0.05)
    GPIO.output(TRIGGER, False)

    while GPIO.input(ECHO) == 0:
        pulse_start = time.perf_counter()      
    while GPIO.input(ECHO) == 1: # Need error control if stuck in loop
        pulse_end = time.perf_counter()

    return True if ((pulse_end - pulse_start)  * 17150) < min_distance else False


def main():
    while True:
        if path_status():
            config.set('DOOR', 'path_status', '1')
        elif not path_status():
            config.set('DOOR', 'path_status', '0')

if __name__ == '__main__':
    main()
