import RPi.GPIO as GPIO
from time import sleep
import pinout

STEP = pinout.STEP
DIR = pinout.DIR
EN = pinout.EN
POWER = pinout.POWER
TRIGGER = pinout.GPIO_TRIGGER
ECHO = pinout.GPIO_ECHO
TOP_LIMIT = pinout.TOP_LIMIT
BOT_LIMIT = pinout.BOT_LIMIT
GPIO.setmode(GPIO.BOARD)
GPIO.setup(EN, GPIO.OUT)
GPIO.setup(STEP, GPIO.OUT)
GPIO.setup(DIR, GPIO.OUT)
GPIO.setup(TRIGGER, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.setup(TOP_LIMIT, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BOT_LIMIT, GPIO.IN, pull_up_down=GPIO.PUD_UP)   
GPIO.setup(POWER, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def door_status():
    top_button = GPIO.input(TOP_LIMIT)
    bot_button = GPIO.input(BOT_LIMIT)    
    if top_button == 0 or bot_button == 0:
        #Door is Open or Close
        return True
    if bot_button == 1 and top_button == 1:
        #Door is in motion or broken :(
        return False

def path_status():
    GPIO.output(TRIGGER, True)
    time.sleep(0.00001)
    GPIO.output(TRIGGER, False)
    StartTime = time.time()
    StopTime = time.time()
 
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
        
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    TimeElapsed = StopTime - StartTime
    distance = (TimeElapsed * 34300) / 2
    return distance    
    
def motor_status():
    
    motor_en = GPIO.input(EN)
    if motor_en == 0:      
        GPIO.output(EN,1)
        print("Motor enabled.")
    
    if motor_en == 1:
        GPIO.output(EN,0)
        print("Motor disabled.")

def action_door(action):
    GPIO.output(EN,1)

    if action == 1:
        print("Opening Door")
        GPIO.output(DIR,1)
    if action == 0:
        print("Closing Door")
        GPIO.output(DIR,0)
      
    while True:
        top_button = GPIO.input(TOP_LIMIT)
        bot_button = GPIO.input(BOT_LIMIT)
        power_buttom = GPIO.input(POWER)

        if action == 1 and top_button == 0:
            print("Door Open")
            break
        if action == 0 and bot_button == 0:
            print("Door Close")
            break
        if power_buttom == 0:
            GPIO.output(EN,0)
            break
        GPIO.output(STEP,GPIO.HIGH)
        sleep(.001) 
        GPIO.output(STEP,GPIO.LOW)
        sleep(.001) 
#GPIO.cleanup()
