import RPi.GPIO as GPIO
import time
import pinout
from configparser import ConfigParser

config = ConfigParser()
STEP = pinout.STEP
DIR = pinout.DIR
EN = pinout.EN
POWER = pinout.POWER
TOP_LIMIT = pinout.TOP_LIMIT
BOT_LIMIT = pinout.BOT_LIMIT
GPIO.setmode(GPIO.BOARD)
GPIO.setup(STEP, GPIO.OUT)
GPIO.setup(DIR, GPIO.OUT)
GPIO.setup(EN, GPIO.OUT)
GPIO.setup(POWER, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(TOP_LIMIT, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BOT_LIMIT, GPIO.IN, pull_up_down=GPIO.PUD_UP)   

  
def action_door(direction):
    GPIO.output(EN,1)
    GPIO.output(DIR,direction)
    config.read('status.ini')
    message = "Opening Door" if direction else "Closing Door"
    print(message)
    
    while True:
        if (direction and not GPIO.input(TOP_LIMIT)) or (not direction and not GPIO.input(BOT_LIMIT)) or (not GPIO.input(POWER)) or (config.getboolean('door', 'path_status')) or (config.getboolean('door', 'path_status')): break          
        #Additional option for Power and path status failures might be needed -- door open
        else:
            GPIO.output(STEP,GPIO.HIGH)
            time.sleep(.001) 
            GPIO.output(STEP,GPIO.LOW)
            time.sleep(.001) 
