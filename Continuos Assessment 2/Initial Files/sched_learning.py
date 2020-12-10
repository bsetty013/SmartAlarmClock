import sched
from sched import scheduler
from datetime import datetime
from datetime import date
import time




def notify(output_reason,user_time,date):
    print(output_reason)
    print(user_time)
    print(date)

def formation():
    s = sched.scheduler(time.time, time.sleep)
    output_reason = "Hello"
    user_time = "12:00"
    date = "12-06-19"
    s.enter(5,1,notify,argument = (output_reason,user_time,date))
    s.enter(7,1,notify,argument = (output_reason,user_time,date))
    while s.empty() != True:
        s.cancel(s.queue[0])
    s.run()

formation()
    
    
