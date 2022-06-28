import RPi.GPIO as GPIO
from time import sleep
import pinout
import os
import subprocess
from door_control import action_door, motor_status
import datetime

#Door closure time range
begin_time = datetime.time(23,00)
end_time = datetime.time(3,00)

OPEN = pinout.OPEN
CLOSE = pinout.CLOSE
POWER = pinout.POWER

def setup():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(OPEN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(CLOSE, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(POWER, GPIO.IN, pull_up_down=GPIO.PUD_UP) 

def manual_control():
    
    open_button = GPIO.input(OPEN)
    close_button = GPIO.input(CLOSE)
    power_buttom = GPIO.input(POWER)
    
    if open_button == 0:
        print("Open")
        action = 1
        action_door(action)               
        
    if close_button == 0:
        print("Close")
        action = 0
        action_door(action)

    if power_buttom == 0:
        print("Power")
        motor_status()

def schedule_control(begin_time, end_time, check_time=None):
    check_time = datetime.time()
    if begin_time < end_time:
        return check_time >= begin_time and check_time <= end_time
    else: # crosses midnight
        return check_time >= begin_time or check_time <= end_time

setup()

while True:
    #GPIO.output(EN,1)
    manual_control()
    #if schedule_control(begin_time,end_time):
    #    action_door(0)
    #ai_control()
