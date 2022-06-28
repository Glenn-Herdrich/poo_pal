import psutil
import sys
from subprocess import Popen


while True:
    active = 0
    for process in psutil.process_iter():
        if process.cmdline() == ['python', '/home/unknown/Documents/poo_pal/door_management.py']:
            active = 1
    
    if active == 0:
        Popen(['python', '/home/unknown/Documents/poo_pal/door_management.py'])

#check if TF is running TFLite_detection_stream.py --modeldir=Sample_TFLite_model
