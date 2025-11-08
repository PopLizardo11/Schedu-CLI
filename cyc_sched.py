import time
from typing import *
from colorama import Fore, Back, Style, init
from tabulate import tabulate
from termcolor import colored, cprint


sample_list = [
    [
        (1,5),(1,6),(1,7),(1,5),(1,8),(1,9),(1,4),
],
    [
        (1,5),(1,6),(1,7),(1,5),(1,8),(1,9),(1,4),
],
    [
        (1,5),(1,6),(1,7),(1,5),(1,8),(1,9),(1,4),
],
]

sample = [
    (1,5),
    (1,6),
    (1,7),
    (1,5),
    (1,8),
    (1,9),
    (1,4),
]

sample_2 = [
    (1,4),
    (1,3),
    (1,2),
    (1,4),
    (1,7),
    (1,8),
    (1,5),
]

sample_3 = [
    (1,36),
    (1,54),
    (1,34),
    (1,47),
    (1,50),
    (1,40),
    (1,49),
]


to_columns = [
    [1,2,3,4,5],
    [1,2,3,4,5],
    [1,2,3,4,5],
    [1,2,3,4,5],
    [1,2,3,4,5],
    [1,2,3,4,5],
]

def mark_day(day: int, hour: int, day_off: tuple[int]) -> tuple[int]:
    return (0, hour) if day in day_off else (1, hour)

def minus_step(h_pair: tuple[int]) -> tuple[int]:
    is_minusable: bool = (h_pair[0] == 1 and h_pair[1] != 0)
    minused: tuple[int] = (h_pair[0], h_pair[1]-1) 
    return minused if is_minusable else h_pair

def assign_day_offs(hrs: list[tuple[int]]) -> list[tuple[int]]:
    day_count: int = len(hrs)
    least_sum: int = hrs[0][1] + hrs[1][1]
    day_off: tuple[int] = (0, 1)
    for i in range(day_count):
        curr_hr: int = hrs[i][1] 
        next_curr_hr: int = hrs[(i+1) if i+1 != day_count else 0][1] 
        curr_sum: int = curr_hr + next_curr_hr
        if curr_sum < least_sum:
            least_sum = curr_sum
            day_off = (i, (i+1) if i+1 != day_count else 0)
        if (i+1) == len(hrs):
            hrs = [mark_day(day, h_pair[1], day_off) for day, h_pair in enumerate(hrs)]
    return hrs

def parse_columns(matrix: list[list[any]]) -> list[list[any]]:
    # only works on an n x n matrix 
    columns: list[list[any]] = [[] for i in range(len(matrix[0]))]
    for row in matrix:
        for i, r in enumerate(row):
            columns[i].append(r) 
    return columns

def extract_hrs(matrix: list[list[tuple[int]]]) -> list[list[int]]:
    extracted_hrs: list[list[int]] = [[] for i in range(len(matrix))]
    for i, hrs in enumerate(matrix):
        for h in hrs:
            if h[1] != 0:
                extracted_hrs[i].append(h[0]) 
            continue
    
    return extracted_hrs

def eval_sched(extracted_hrs: list[list[int]], req_hrs: list[tuple[int]]) -> bool:
    hrs_sum: list[int] = []
    for hrs in extracted_hrs:
        hrs_sum.append(sum(hrs))
    return True if hrs_sum == req_hrs else False

def schedule(hrs: list[tuple[int]]) -> list[list[tuple[int]]]:
    req_hrs = [h[1] for h in hrs]
    sched = []
    while True:
        hrs = assign_day_offs(hrs)
        sched.append(hrs)
        curr_col = parse_columns(sched)
        extracted_hrs = extract_hrs(curr_col)
        if eval_sched(extracted_hrs, req_hrs):
            break
        hrs = [minus_step(h) for h in hrs]
    return sched

def present_sched(sched, hrs):
    req_hrs = [h[1] for h in hrs]
    print(f"{req_hrs} \n")
    for i, hrs in enumerate(sched):
        stf = f"Staff {i+1}: "
        for h in hrs:
            if h[0] == 0:
                stf += (f"[{h[1]}] ")
                continue
            stf += (f"{h[1]} ")
        print(stf)

def tabulate_sched(sched, hrs):
    req_hrs = ["" for h in hrs]
    req_hrs = ["Employee"] + req_hrs
    sched_hrs = [[] for h in sched]
    for i, hrs in enumerate(sched):
        sched_hrs[i].append(i+1)
        for h in hrs:
            sched_hrs[i].append(h[1])

    table = tabulate(
        sched_hrs,
        headers=req_hrs,
        tablefmt="pipe",
    )

    print(Fore.YELLOW + table)

def total_employees(sched: list[list[tuple[int]]]) -> int:
    return len(sched)

def expected_full_time(req_hrs: list[tuple[int]]) -> int:
    week_length = len(req_hrs)-2
    req_hrs_sum: int = 0
    for h in req_hrs:
        req_hrs_sum += h[1]
    return req_hrs_sum/week_length

def count_job_cat(sched: list[list[tuple[int]]]) -> dict[str, int]:
    extracted_rem_hrs: list[list[int]] = [[] for i in range(len(sched))]
    for i, hrs in enumerate(sched):
        for h in hrs:
            extracted_rem_hrs[i].append(h[1]) 
    
    job_cat: dict[str, int] = {"full_time": 0, "part_time": 0}
    for rem_hrs in extracted_rem_hrs:
        if all(rem_hrs):
            job_cat["full_time"] += 1
            continue
        job_cat["part_time"] += 1
    return job_cat


def find_ideal_sizes(sched: list[list[tuple[int]]]) -> list[int]:
    str_sched: list[list[tuple[int]]] = [[] for n in range(len(sched))]
    for i, hrs in enumerate(sched):
        for h in hrs:
            str_sched[i].append(len(str(h[1])))
    len_columns: list[list[int]] =  parse_columns(str_sched)
    
    # finding the largest length
    ideal_sizes: list[int] = []
    for sizes in len_columns:
        max_size = sizes[0]
        for size in sizes:
            max_size = size if size > max_size else max_size
        ideal_sizes.append(max_size)
    
    return ideal_sizes


def present_table_sched(sched: list[list[tuple[int]]], size: list[int], color: Optional[str]="red") -> None:
    per_name = "Employee"
    header: str = f"|   {per_name} |"
    bound_size = len(per_name) + 3
    header_bound: str = "|" + "-"*bound_size + ":|"
    body: list[str] = []
    body_count = len(sched)
    
    for s in size:
        header += " "*2 + " "*s + " |"
    for s in size:
        bnd_size = s + 2
        header_bound += "-"*bnd_size + ":" + "|"
    for b in range(body_count):
        adj_b = b + 1
        b_str_size = len(str(adj_b))
        space_size = bound_size - b_str_size
        body.append("|" + " "*space_size + f"{adj_b} " + "|")
    for i, hrs in enumerate(sched):
        for col_i, h in enumerate(hrs):
            h_str_size = len(str(h[1]))
            b_cell_factor = 2 + (size[col_i]-h_str_size)
            b_cell = " "*b_cell_factor + f"{h[1]} "
            body[i] += b_cell + "|" if h[0] == 1 else colored(b_cell, color) + "|"

    print(header)
    time.sleep(0.05)
    print(header_bound)
    for row in body:
        time.sleep(0.05)
        print(row)

# TEST

# print(find_ideal_sizes(sample_list))
# present_tab_sched(schedule(sample), sample)

sample_sched = schedule(sample)
sample_size = find_ideal_sizes(sample_sched)
present_table_sched(sample_sched, sample_size)
print(total_employees(sample_sched))
print(expected_full_time(sample))
print(count_job_cat(sample_sched))

# print(assign_day_offs(sample))
# new_sched = schedule(sample)
# sched_2 = schedule(sample_2)
# sched_3 = schedule(sample_3)
# # present_sched(new_sched) 
# present_sched(sched_2, sample_2)
# present_sched(sched_3, sample_3)

