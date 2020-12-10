import schedule
import datetime,time
import win32com.client as wincl

alarm_reason = ""
def alarm_notify(alarm_reason):
    notification_list = []
    array_section = []
    print(alarm_reason)
    array_section.append(alarm_reason)
    array_section.append(datetime.datetime.now())
    notification_list.append(array_section)
    speak = wincl.Dispatch("SAPI.SpVoice")
    speak.Speak(alarm_reason)

def alarm_notify_once(alarm_reason):
    notification_list = []
    array_section = []
    print(alarm_reason)
    array_section.append(alarm_reason)
    array_section.append(datetime.datetime.now())
    notification_list.append(array_section)
    speak = wincl.Dispatch("SAPI.SpVoice")
    speak.Speak(alarm_reason)
    return schedule.CancelJob
    quit()

def create_alarm():
    alarm_file = open("schedule_file.txt","w")
    create_enough = None
    while create_enough != True:
        print("Would you like to create an alarm? ")
        create_choice = input("Enter yes or no: ")
        if create_choice == "yes":
            alarm_reason = input("Enter the reason for the alarm: ")
            alarm_file.write("\n")
            alarm_file.write(alarm_reason)
            alarm_file.write(",")
            print("What would you like to be the regularity of the alarm")
            alarm_frequency = input("Enter second, minute, hourly,daily,weekly or one off: ")
            if alarm_frequency == "second":
                regularity = input("Enter how many seconds you want between each alarm: ")
                alarm_file.write(alarm_frequency)
                alarm_file.write(",")
                alarm_file.write(regularity)               
            if alarm_frequency == "minute":
                regularity = input("How many minutes do you want between each alarm: ")
                alarm_file.write(alarm_frequency)
                alarm_file.write(",")
                alarm_file.write(regularity)
            elif alarm_frequency == "hourly":
                regularity = input("How many hours do you want between each alarm: ")
                alarm_file.write(alarm_frequency)
                alarm_file.write(",")
                alarm_file.write(regularity)
            elif alarm_frequency == "daily":
                alarm_time = input("Enter the time of each alarm: ")
                alarm_file.write(alarm_frequency)
                alarm_file.write(",")
                alarm_file.write(alarm_time)
            elif alarm_frequency == "one off":
                alarm_time = input("Enter the time of the alarm: ")
                alarm_file.write(alarm_frequency)
                alarm_file.write(",")
                alarm_file.write(alarm_time)
            alarm_file.write("\n")
        elif create_choice == "no":
            create_enough = True
        else:
            print("Error: You can only enter yes or no")
    alarm_file.close()

#create_alarm()

def alarm_formation():
    alarm_schedule = []
    schedule_section = []
    element_string = ""
    alarm_file = open("schedule_file.txt","r")
    for line in alarm_file:
        analyse_list = list(line)
        if analyse_list[0] == "\n":
            pass
        else:
            for list_element in line:
                if list_element == "," or list_element == "\n":
                    schedule_section.append(element_string)
                    element_string = ""
                else:
                    element_string = element_string + list_element
            alarm_schedule.append(schedule_section)
            schedule_section = []
    print(alarm_schedule)

    for inner_list in alarm_schedule:
        alarm_reason = inner_list[0]
        alarm_frequency = inner_list[1]
        if alarm_frequency == "second":
            regularity = int(inner_list[2])
            schedule.every(regularity).seconds.do(alarm_notify,alarm_reason)
        elif alarm_frequency == "minute":
            reguarlity = int(inner_list[2])
            schedule.every(regularity).minutes.do(alarm_notify,alarm_reason)
        elif alarm_frequency == "hourly":
            regularity = int(inner_list[2])
            schedule.every(regularity).hours.do(alarm_notify,alarm_reason)
        elif alarm_frequency == "daily":
            alarm_time = inner_list[2]
            schedule.every().day.at(alarm_time).do(alarm_notify,alarm_reason)
        elif alarm_frequency == "one off":
            alarm_time = inner_list[2]
            schedule.every().day.at(alarm_time).do(alarm_notify_once,alarm_reason)

        while True:
            schedule.run_pending()
            time.sleep(1)
        
alarm_formation()
        

def cancel_alarm():
    alarm_schedule = []
    schedule_section = []
    element_string = ""
    alarm_file = open("schedule_file.txt","r")
    for line in alarm_file:
        analyse_list = list(line)
        if analyse_list[0] == "\n":
            pass
        else:
            for list_element in line:
                if list_element == "," or list_element == "\n":
                    schedule_section.append(element_string)
                    element_string = ""
                else:
                    element_string = element_string + list_element
            alarm_schedule.append(schedule_section)
            schedule_section = []
    alarm_file.close()

    cancel_enough = None
    while cancel_enough != True:
        cancel_choice = input("Would you look to like to cancel an alarm: ")
        if cancel_choice.lower() == "yes":
            print("Here is your current alarm schedule: ")
            print(alarm_schedule)
            cancel_reason = input("Enter the reason of the alarm you would like to cancel: ")
            cancel_frequency = input("Enter the frequency of the alarm you would like to cancel: ")
            
            for inside_list in alarm_schedule:
                if cancel_reason == inside_list[0] and cancel_frequency == inside_list[1]:
                    alarm_schedule.remove(inside_list)
                    print("Alarm Removed")
                else:
                    print("Alarm Not Recognised")

            alarm_file = open("schedule_file.txt","w")
            for internal_list in alarm_schedule:
                alarm_file.write("\n")
                for list_position in internal_list:
                    alarm_file.write(list_position)
                    alarm_file.write(",")
        
        elif cancel_choice.lower() == "no":
            cancel_enough = True

#cancel_alarm()
        
        

    


