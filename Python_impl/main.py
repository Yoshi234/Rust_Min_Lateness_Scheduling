# key - assignment name -> time -> deadline

total = 43
days = [7, 7, 4, 6, 4, 7, 8]
# today = 0
def find_time_del(days:list, time_dif:int, current:int = 0, total:int=43):
    n = len(days)
    sum = (time_dif // n)*total
    remain = time_dif%n
    while remain != 0:
        sum += days[current]
        current -= 1
        remain -= 1
    return sum

# thursday at the 4th work hour - time_dif=4, deadline_hour=4
def find_deadline(days:list, time_dif:int, start_hour:int=0, deadline_hour:int = 0, current:int = 0, total:int=43):
    n = len(days)
    sum = (time_dif//n)*total
    remain = time_dif%n
    while remain != 0:
        sum += days[current]
        current += 1
        remain -= 1
    sum += deadline_hour - start_hour
    return sum
    
import random

class Assign: 
    def __init__(self, name, duration, deadline):
        self.name = name
        self.duration = duration
        self.deadline = deadline

    def __str__(self):
        return f"{self.name} -> dur: {self.duration} -> deadline: {self.deadline}"

if __name__ == "__main__":
    # these times were set on 10/8/23 - make sure to iteratively subtract from each 
    # deadline the number of days which have passed leading up to the most recent
    # update point
    Assignments = [
        Assign("Data Challenge Outline - timeline work", 2, 43), 
        Assign("Delphi Model Validation", 3, 24),
        Assign("Delphi Model Latency", 3, 24),
        Assign("Delphi Model Throughput", 3, 24),
        Assign("CSE 3500 PS3 - p1", 1, 45), 
        Assign("CSE 3500 PS3 - p2", 1, 45), 
        Assign("CSE 3500 PS3 - p3", 1, 45),
        Assign("CSE 3500 PS3 - p5", 1, 45),
        Assign("STAT 3515 Weakness Identification", 2, -15), 
        Assign("STAT 3515 EP1 - One-Way Fixed Effects", 2, 9), 
        Assign("STAT 3515 EP2 - One Way Random Effects", 2, 9),
        Assign("STAT 3515 EP3 - Randomized Complete Block Design", 2, 9),
        Assign("STAT 3515 EP4 - Incomplete Block Design (Latin Squares)", 2, 9),
        Assign("STAT 3515 EP5 - Incomplete Block Design (Greco Latin Squares)", 2, 9),
        Assign("STAT 3515 EP5 - Two-Way factorial Completely randomized Fixed WEffects", 2, 8),
        Assign("STAT 3515 EP7 - Three-Way Factorial Completely ranomized Fixed Effects", 2, 8),
        Assign("STAT 3515 Homework", 3, 22), 
        Assign("STAT 3675 Homework", 3, 23), 
        Assign("Fill out Honors Plan + Submit", 1, 144), 
        Assign("Put together Poster Presentation for Fall Frontiers", 5, 38),
        Assign("Print Poster Presentation for Fall Frontiers", 2, 45), 
        Assign("Apply for NVIDIA Internships of Interest", 3, 2),
        Assign("Register for Data Science Day Poster Session", 0.5, 13)

    ]
    random.shuffle(Assignments)

    time = 0
    sorted_data = sorted(Assignments, key=lambda item: item.deadline)
    for i in range(len(sorted_data)):
        print(i, sorted_data[i])
        print(f"\t at time {time}")
        print(f"Lateness: {0 if sorted_data[i].deadline > time else sorted_data[i].deadline - (time+sorted_data[i].duration)}")
        print(100*"-")
        time += sorted_data[i].duration