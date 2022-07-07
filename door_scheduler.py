from datetime import datetime, time
from door_management import action_door, door_status
import logging
import os
import schedule
from configparser import ConfigParser

config_file = os.path.join(os.path.dirname(__file__), 'status.ini')
config = ConfigParser()
config.read(config_file)

def check_time(begin_time, end_time, check_time=None):  
    logging.debug("Door schedule running")
    check_time = check_time or datetime.now().time()
    if begin_time < end_time:
        return check_time >= begin_time and check_time <= end_time
    else:
        return check_time >= begin_time or check_time <= end_time

def door_schedule_actions():
    logging.info("Checking schedules") 
    scheduled_times = {1 : {"begin_time" : time(22,00), "end_time" : time(5,00)}} #10PM - 5AM
    override = (config.getint('DOOR', 'override'))

    for i in scheduled_times.items():
        begin_time = scheduled_times[1].get("begin_time")
        end_time = scheduled_times[1].get("end_time")
        checked_time = check_time(begin_time, end_time)

        if (checked_time and door_status() and not override):
            logging.info("Checking schedules - Close Door") 
            action_door(0) 
        if (not checked_time and door_status() and not override):
            logging.info("Checking schedules - Open Door") 
            action_door(1) 

def main():
    level = logging.INFO
    fmt = '[%(levelname)s] %(asctime)s - %(message)s'
    logging.basicConfig(level=level, format=fmt)
    logging.info("Door scheduler started")    
    
    schedule.every(1).minute.do(door_schedule_actions)

    while True:
        schedule.run_pending()
        logging.debug("Door schedule check") 

if __name__ == '__main__':
    main()
