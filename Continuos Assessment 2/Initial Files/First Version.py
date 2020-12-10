import datetime
import winsound

def create_alarm():
    create_enough = None
    while create_enough != True:
        print("Would you like to create an alarm")
        create_choice = input("Enter Yes or No: ")
        if create_choice.lower() == "yes":
            print("This alarm will be created according to a 24 hour clock")
            alarm_hour = input("Enter the hour of the alarm: ")
            alarm_minute = input("Enter the minute of the alarm: ")
            alarm_reason = input("Enter the reason for the alarm: ")
            alarm_file = open("schedule_file.txt","a+")
            alarm_file.write("\n")
            if len(alarm_hour) < 2 :
                alarm_file.write("0" + alarm_hour)
            else:
                alarm_file.write(alarm_hour)
            if len(alarm_minute) < 2:
                alarm_file.write("0" + alarm_minute)
            else:
                alarm_file.write(alarm_minute)
            alarm_file.write(alarm_reason)
            alarm_file.close()
        elif create_choice.lower() == "no":
            create_enough = True
        
        
    

def cancel_alarm(alarm_schedule,schedule_section):
    cancel_enough = None
    while cancel_enough != True:
        print("Would you like to cancel an alarm")
        cancel_choice = input("Enter Yes or No: ")
        if cancel_choice.lower() == "yes":
            alarm_file = open("schedule_file.txt","r")
            for row in alarm_file:
                analyse_list = list(row)
                if analyse_list[0] == "\n":
                    pass
                else:
                    reason_string = ""
                    schedule_section.append(analyse_list[0] + analyse_list[1])
                    schedule_section.append(analyse_list[2] + analyse_list[3])
                    for character in range(4,len(analyse_list)):
                        if analyse_list[character] == "\n":
                            pass
                        else:
                            reason_string = reason_string + analyse_list[character]
                    schedule_section.append(reason_string)
                    alarm_schedule.append(schedule_section)
                    schedule_section = []
            schedule_length = len(alarm_schedule)
            lists_searched = 0
            cancel_hour = input("Enter the hour of the alarm you would like to cancel: ")
            cancel_minute = input("Enter the minute of the alarm you would like to cancel: ")
            cancel_reason = input("Enter the reason of the alarm you would like to cancel: ")
            for inner_list in alarm_schedule:
                for list_element in inner_list:
                    if (inner_list[0] == cancel_hour) and (inner_list[1] == cancel_minute) and (inner_list[2] == cancel_reason):
                        alarm_schedule.remove(inner_list)
                        print("Alarm Cancelled")
                        break
                    else:
                        print(inner_list)
                        lists_searched = lists_searched + 1
                        if lists_searched == schedule_length:
                            print("Alarm Not Found")
                            break        
            alarm_file.close()
            alarm_file = open("schedule_file.txt","w")
            for inside_list in alarm_schedule:
                alarm_file.write("\n")
                for element in inside_list:
                    letter_list = list(element)
                    for letter in letter_list:
                        alarm_file.write(letter)
            alarm_file.close()
        elif cancel_choice.lower() == "no":
            cancel_enough = True
    
#Next To Do
#What is left of the alarm_schedule after cancelling an alarm, put that back onto the text file
#Effectively updating the schedule file

def alarm_notify():
    print("Here notifications occur when alarms ring")





def alarm_main():
    alarm_schedule = []
    schedule_section = []
    process_complete = None
    while process_complete != True:
        print("Would you like to create or cancel an alarm")
        print("Or would you like to quit the system")
        alarm_choice = input("Enter create, cancel or quit: ")
        if alarm_choice.lower() == "create":
            create_alarm()
        elif alarm_choice.lower() == "cancel":
            cancel_alarm(alarm_schedule,schedule_section)
        elif alarm_choice.lower() == "quit":
            process_complete = True
        else:
            print("Error: Input Not Recognised")

alarm_main()
