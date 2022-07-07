import RPi.GPIO as GPIO
import time
import os
import datetime
from configparser import ConfigParser
import logging
import multiprocessing

config_file = os.path.join(os.path.dirname(__file__), 'status.ini')
config = ConfigParser()
config.read(config_file)

OPEN = (config.getint('GPIO', 'OPEN'))
CLOSE = (config.getint('GPIO', 'CLOSE'))
POWER = (config.getint('GPIO', 'POWER'))
POWER_LIGHT = (config.getint('GPIO', 'POWER_LIGHT'))
STEP = (config.getint('GPIO', 'STEP'))
DIR = (config.getint('GPIO', 'DIR'))
EN = (config.getint('GPIO', 'EN'))
TOP_LIMIT = (config.getint('GPIO', 'TOP_LIMIT'))
BOT_LIMIT = (config.getint('GPIO', 'BOT_LIMIT'))
TRIGGER = (config.getint('GPIO', 'TRIGGER'))
ECHO = (config.getint('GPIO', 'ECHO'))
min_distance = (config.getint('DOOR', 'min_distance'))

GPIO.setmode(GPIO.BOARD)
GPIO.setup(OPEN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(CLOSE, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(POWER, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(POWER_LIGHT, GPIO.OUT)
GPIO.setup(STEP, GPIO.OUT)
GPIO.setup(DIR, GPIO.OUT)
GPIO.setup(EN, GPIO.OUT)
GPIO.setup(TOP_LIMIT, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BOT_LIMIT, GPIO.IN, pull_up_down=GPIO.PUD_UP)   
GPIO.setup(TRIGGER, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

#Door closure time range

GPIO.output(POWER_LIGHT,1)

def manual_control():
    if not GPIO.input(OPEN):
        logging.info("Open button triggered")
        config.set('DOOR', 'override', '1')
        action_door(1)               
    elif not GPIO.input(CLOSE):
        logging.info("Close button triggered")
        config.set('DOOR', 'override', '1')
        action_door(0)
    elif not GPIO.input(POWER):
        logging.info("Power button triggered")
        if GPIO.input(EN):
            GPIO.output(EN,0)
            GPIO.output(POWER_LIGHT,0)
        else: 
            GPIO.output(EN,1) 
            GPIO.output(POWER_LIGHT,1) 

def path_check():
    GPIO.output(TRIGGER, True)
    time.sleep(0.05)
    GPIO.output(TRIGGER, False)
    pulse_start = 0
    pulse_end = 0
    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()      
    while GPIO.input(ECHO) == 1: # Need error control if stuck in loop
        pulse_end = time.time()
    return True if ((pulse_end - pulse_start)  * 17150) < min_distance else False

def path_status():
    while True:
        if path_check():
            logging.info("Path disruption detected")
            GPIO.output(DIR,1)
            break
        elif not path_check():
            config.set('DOOR', 'path_status', '0')
    with open(config_file, 'w') as config_write:
        config.write(config_write)

def door_status():
    top_button = GPIO.input(TOP_LIMIT)
    bot_button = GPIO.input(BOT_LIMIT)    
    if not top_button or not bot_button:
        logging.info("Door open" if not top_button else "Door closed")
        #Door is Open or Close
        return True
    elif bot_button and top_button:
        logging.info("Door is in motion or broken")
        return False

def action_door(direction):
    GPIO.output(EN,1)
    GPIO.output(DIR,direction)
    logging.info("Opening Door" if direction else "Closing Door")
    p1 = multiprocessing.Process(target=path_status)
    p1.start()
    while True:
        config.read(config_file)
        if (GPIO.input(DIR) and not GPIO.input(TOP_LIMIT)) or (not GPIO.input(DIR) and not GPIO.input(BOT_LIMIT)) or (not GPIO.input(POWER)) or config.getboolean('DOOR', 'path_status') or config.getboolean('DOOR', 'ai_status'):           
            break         
        else:
            GPIO.output(STEP,GPIO.HIGH)
            time.sleep(.001) 
            GPIO.output(STEP,GPIO.LOW)
            time.sleep(.001) 
    with open(config_file, 'w') as config_write:
        config.write(config_write)

def main():
    level = logging.INFO
    fmt = '[%(levelname)s] %(asctime)s - %(message)s'
    logging.basicConfig(level=level, format=fmt)
    logging.info("Door management started")    

    while True:
        manual_control()

if __name__ == '__main__':
    main()
