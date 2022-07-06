import psutil
import sys
from subprocess import Popen


while True:
    management_active = 0
    scheduler_active = 0
    for process in psutil.process_iter():
        if process.cmdline() == ['python', '/home/unknown/Documents/poo_pal/door_management.py']:
            management_active = 1
        if process.cmdline() == ['python', '/home/unknown/Documents/poo_pal/door_scheduler.py']:
            scheduler_active = 1       

    if management_active == 0:
        Popen(['python', '/home/unknown/Documents/poo_pal/door_management.py'])
    
    if scheduler_active == 0:
        Popen(['python', '/home/unknown/Documents/poo_pal/door_scheduler.py'])        
