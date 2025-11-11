from colorama import Fore, Back, Style, init
from termcolor import colored, cprint
from tabulate import tabulate
import cyc_sched

wel_mes = colored("WELCOME TO SCHEDULI CLI!\n", "yellow")
sub_mes = colored("A command line tool for your scheduling needs\nCurrently limited to two-consecutive day-offs scheduling :)\n")
print(wel_mes)
print(sub_mes)

while True:
    day_count_ques = colored("How many days does your week have?: ", "yellow")
    day_count = input(day_count_ques)
    if not day_count:
        day_count = 7 

    req_hrs_dis = [["Day no."], ["Req. hrs:"]]
    for i in range(1, int(day_count)+1):
        day_hrs_ques = colored(f"How many required hours in day {i}? ", "yellow")
        day_hrs = input(day_hrs_ques)
        req_hrs_dis[0].append(f"{i}")
        req_hrs_dis[1].append(int(day_hrs))
    req_hrs_table = tabulate(req_hrs_dis)

    print("")
    print(req_hrs_table)
    print("")
    req_hrs_con = input(colored("Is your table correct? [Y/n]: ", "yellow"))
    if req_hrs_dis == "n" or req_hrs_dis == "N":
        continue 
    req_hrs_ext = req_hrs_dis[1][1:]
    req_hrs = [(1, h) for h in req_hrs_ext]
    user_sched = cyc_sched.schedule(req_hrs)
    sched_sizes = cyc_sched.find_ideal_sizes(user_sched)
    print("")
    cyc_sched.present_table_sched(user_sched, sched_sizes)

        