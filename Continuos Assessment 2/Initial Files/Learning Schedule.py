import schedule
import datetime,time

alarm_reason = ""
def alarm_notify(alarm_reason):
    print(alarm_reason)

def alarm_notify_once(alarm_reason):
    print(alarm_reason)
    return schedule.CancelJob
    quit()


    
def create_alarm():
    alarm_reason = input("Enter the reason for the alarm: ")
    print("What would you like to be the regularity of the alarm")
    alarm_frequency = input("Enter second, minute, hourly,daily,weekly or one off: ")
    if alarm_frequency == "second":
        regularity = int(input("Enter how many seconds you want between each alarm: "))
        schedule.every(regularity).seconds.do(alarm_notify,alarm_reason)
    if alarm_frequency == "minute":
        regularity = int(input("How many minutes do you want between each alarm: "))
        schedule.every(regularity).minutes.do(alarm_notify,alarm_reason)
    elif alarm_frequency == "hourly":
        regularity = int(input("How many hours do you want between each alarm: "))
        schedule.every().hour.do(alarm_notify,alarm_reason)
    elif alarm_frequency == "daily":
        alarm_time = input("Enter the time of each alarm: ")
        schedule.every().day.at(alarm_time).do(alarm_notify,alarm_reason)
    elif alarm_frequency == "one off":
        alarm_time = input("Enter the time of the alarm: ")
        schedule.every().day.at(alarm_time).do(alarm_notify_once,alarm_reason)
        
    while True:
       schedule.run_pending()
       time.sleep(1)
            
    
create_alarm()

    
        
        
    


