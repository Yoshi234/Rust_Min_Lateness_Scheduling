# key - assignment name -> time -> deadline
import os
from datetime import datetime
import random

class day:
    def __init__(self, name:str, hours:int, splits):
        self.name = name
        self.hours = hours
        self.splits = splits
# global variables
total = 43
#       M  T  W  TH F  SA SU
days = [day("Monday", 5, splits=[9.5,10.5,11.5,20,21]), 
        day("Tuesday", 4, splits=[9.5,10.5,20,21]),
        day("Wednesday", 6, splits=[9.5,10.5,11.5,17,20,21]),
        day("Thursday", 4, splits=[9.5,10.5,20,21]),
        day("Friday", 7, splits=[9.5,10.5,11.5,14,15.5,17,20,21]),
        day("Saturday", 8, splits=[9.66,10.82,12,14.33,15.66,17,20,21]),
        day("Sunday", 7, splits=[10.82,12,14.33,15.66,17,20,21])]

def time_to_hour(days:list, hour:int, day_idx:int):
    '''
    hour is an integer from 0 to 23
    day is the integer index of the day desired
    '''
    hour_idx = 1
    if hour > days[day_idx].splits[-1]:
        return len(days[day_idx].splits)
    while hour > days[day_idx].splits[hour_idx-1]:
        hour_idx +=1
    return hour_idx 

def get_hour_dif(days:list, time_dif:int, prev_day:int, current_day:int, prev_hour:int, current_hour:int):
    '''
    time_dif is the number of days difference between two days
    prev_hour is the hour of the previous date
    current_hour is the hour at the current date
    prev_hour must be <= current_hour if time_dif is 0
    '''
    # if time_dif == 0 and (prev_hour > current_hour): 
    #     print("Error - the time entered is before the previous date")
    #     return None
    current_hour = time_to_hour(days, current_hour, current_day)
    prev_hour = time_to_hour(days, prev_hour, prev_day)
    if time_dif == 0:
        return current_hour - prev_hour
    
    n = len(days)
    sum = (time_dif//n)*total
    remain = time_dif%n
    while remain != 0:
        sum += days[current_day].hours
        current_day -= 1
        remain -= 1
    sum += (days[prev_day].hours - prev_hour)
    sum -= (days[current_day].hours - current_hour)
    return sum

# today = 0
def find_time_del(days:list, time_dif:int, current:int = 0, total:int=43):
    n = len(days)
    sum = (time_dif // n)*total
    remain = time_dif%n
    while remain != 0:
        sum += days[current].hours
        current -= 1
        remain -= 1
    return sum

# thursday at the 4th work hour - time_dif=4, deadline_hour=4
def find_deadline(days:list, time_dif:int, start_hour:int=0, deadline_hour:int = 0, current:int = 0, total:int=43):
    n = len(days)
    sum = (time_dif//n)*total
    remain = time_dif%n
    while remain != 0:
        sum += days[current].hours
        current += 1
        remain -= 1
    sum += (deadline_hour - start_hour)
    return sum

def get_new_assignments(days:list, current:datetime):
    current_date = current
    start_hour = time_to_hour(days, current_date.hour, current_date.weekday())
    new_assignments = []
    get = True
    while get == True:
        stop = input("Enter 'stop' to end input:\t")
        if stop == "stop":
            get = False
            break

        name = input("Please enter assignment name (str):\t")
        duration = int(input("Enter the assignment duration in hours:\t"))
        deadline_date = input("Enter the date of the assignment in format 2020-10-09 (ex):\t")
        deadline_hour = int(input("Enter the hour of the deadline (0-24)"))
        
        date1=None
        try:
            date1 = datetime.strptime(deadline_date, '%Y-%m-%d')
        except:
            print("You entered the date incorrectly. Please try again with the correct format")
            continue

        deadline_hour = time_to_hour(days, deadline_hour, date1.weekday())
        time_diff = (date1.day-current_date.day)
        if date1.date() == current_date.date():
            time_diff=0
        else:
            time_diff=(date1-current_date).days
        
        final_deadline = find_deadline(days, time_diff, start_hour, deadline_hour, current_date.weekday(), 41)
        new_assign = Assign(name=name, duration=duration, deadline=final_deadline)
        new_assignments.append(new_assign)
    return new_assignments

def write_assignments(assignments:list, file:str, current_date:datetime=None):
    if current_date == None:
        with open(file, "a") as f:
            for i in range(len(assignments)): 
                f.write(f"{assignments[i].name};{assignments[i].duration};{assignments[i].deadline}\n")
    else:
        with open(file, "w") as f:
            f.write(f"{current_date.strftime('%Y-%m-%d')};{current_date.hour}\n")
            for i in range(len(assignments)):
                f.write(f"{assignments[i].name};{assignments[i].duration};{assignments[i].deadline}\n")

class Assign: 
    def __init__(self, name, duration:float, deadline:float):
        self.name = name
        self.duration = duration
        self.deadline = deadline

    def __str__(self):
        return f"{self.name} -> dur: {self.duration} -> deadline: {self.deadline}"

if __name__ == "__main__":
    # these times were set on 10/8/23 - make sure to iteratively subtract from each 
    # deadline the number of days which have passed leading up to the most recent
    # update point
    current_date = datetime.now()
    all_assignments = get_new_assignments(days, current_date)
    # all_assignments = [
    #     Assign("Data Challenge Outline - timeline work", 2, 144), 
    #     Assign("Delphi Model Validation", 3, 24),
    #     Assign("Delphi Model Latency", 3, 24),
    #     Assign("Delphi Model Throughput", 3, 24),
    #     Assign("CSE 3500 PS3 - p1", 1, 45), 
    #     Assign("CSE 3500 PS3 - p2", 1, 45), 
    #     Assign("CSE 3500 PS3 - p3", 1, 45),
    #     Assign("CSE 3500 PS3 - p5", 1, 45),
    #     Assign("STAT 3515 Weakness Identification", 1, -15), 
    #     Assign("STAT 3515 EP1 - One-Way Fixed Effects", 1, 9), 
    #     Assign("STAT 3515 EP2 - One Way Random Effects", 1, 9),
    #     Assign("STAT 3515 EP3 - Randomized Complete Block Design", 1, 9),
    #     Assign("STAT 3515 EP4 - Incomplete Block Design (Latin Squares)", 1, 9),
    #     Assign("STAT 3515 EP5 - Incomplete Block Design (Greco Latin Squares)", 1, 9),
    #     Assign("STAT 3515 EP5 - Two-Way factorial Completely randomized Fixed WEffects", 1, 8),
    #     Assign("STAT 3515 EP7 - Three-Way Factorial Completely ranomized Fixed Effects", 1, 8),
    #     Assign("STAT 3515 Homework", 3, 22), 
    #     Assign("STAT 3675 Homework", 3, 23), 
    #     Assign("Fill out Honors Plan + Submit", 1, 144), 
    #     Assign("Put together Poster Presentation for Fall Frontiers", 5, 38),
    #     Assign("Print Poster Presentation for Fall Frontiers", 2, 45), 
    #     Assign("Apply for NVIDIA Internships of Interest", 1, 2),
    #     Assign("Register for Data Science Day Poster Session", 0.5, 13),
    #     Assign("Compile and print notes for Test", 2, 19), 
    #     Assign("Compile Class Notes - 10/9 + 10/10", 2, 19), 
    #     Assign("Compile Class Notes - 10/11 + 10/12 + 10/13", 3, 38)
    # ]
    random.shuffle(all_assignments)

    if not "assignments.txt" in os.listdir():
        with open("assignments.txt", "w") as f:
            f.write(f"{current_date.strftime('%Y-%m-%d')};{current_date.hour}\n")
        write_assignments(all_assignments, "assignments.txt", None)
    else:
        old_assignments = []
        with open("assignments.txt", "r") as f:
            lines = f.readlines()
            line1 = lines[0].strip("\n")
            line1 = line1.split(";")
            old_date = datetime.strptime(line1[0], '%Y-%m-%d')
            old_date_hour = int(line1[1])
            for i in range(1, len(lines)):
                x = lines[i].strip("\n")
                x = x.split(";")
                assignment = Assign(x[0], float(x[1]), float(x[2]))
                old_assignments.append(assignment)
            dif = get_hour_dif(days, time_dif=(current_date - old_date).days, 
                               prev_day=old_date.weekday(),
                               current_day=current_date.weekday(), 
                               prev_hour=int(old_date_hour),
                               current_hour=current_date.hour)
            if dif > 0:
                for assign in old_assignments:
                    assign.deadline -= dif
            else: 
                for assign in old_assignments:
                    assign.deadline += dif
        all_assignments = all_assignments + old_assignments
        write_assignments(all_assignments, "assignments.txt", current_date)

    with open("schedule.txt", "w") as f:
        time = 0
        sorted_data = sorted(all_assignments, key=lambda item: item.deadline)
        for i in range(len(sorted_data)):
            f.write(f"{i} {sorted_data[i]}\n")
            f.write(f"\t at time {time}\n")
            f.write(f"Lateness: {0 if sorted_data[i].deadline > time else sorted_data[i].deadline - (time+sorted_data[i].duration)}\n")
            f.write(100*"-")
            f.write("\n")
            time += sorted_data[i].duration