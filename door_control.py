import RPi.GPIO as GPIO
from time import sleep
import pinout



STEP = pinout.STEP
DIR = pinout.DIR
EN = pinout.EN
POWER = pinout.POWER
TOP_LIMIT = pinout.TOP_LIMIT
BOT_LIMIT = pinout.BOT_LIMIT
GPIO.setmode(GPIO.BOARD)
GPIO.setup(EN, GPIO.OUT)
GPIO.setup(STEP, GPIO.OUT)
GPIO.setup(DIR, GPIO.OUT)
GPIO.setup(TOP_LIMIT, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BOT_LIMIT, GPIO.IN, pull_up_down=GPIO.PUD_UP)   
GPIO.setup(POWER, GPIO.IN, pull_up_down=GPIO.PUD_UP)


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
