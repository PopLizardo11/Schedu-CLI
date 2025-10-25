# update the algorithm from time to time
# function for cyclical scheduling (two consecutive days)

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
    (1,40),
    (1,40),
    (1,32),
    (1,32),
    (1,24),
    (1,16),
    (1,8),
]


to_columns = [
    [1,2,3,4,5],
    [1,2,3,4,5],
    [1,2,3,4,5],
    [1,2,3,4,5],
    [1,2,3,4,5],
    [1,2,3,4,5],
]

def mark_day(day, h, day_off):
    return (0, h[1]) if day in day_off else (1, h[1])

def minus_step(h):
    return (h[0], h[1]-1) if (h[0] == 1 and h[1] != 0) else (h[0], h[1])

def assign_day_offs(hrs):
    day_count = len(hrs)
    least = hrs[0][1] + hrs[1][1]
    day_off = (0, 1)
    for i in range(day_count):
        curr = hrs[i][1] + hrs[(i+1) if i+1 != day_count else 0][1]
        if curr < least:
            least = curr
            day_off = (i, (i+1) if i+1 != day_count else 0)
        if (i+1) == len(hrs):
            hrs = [mark_day(day, h, day_off) for day, h in enumerate(hrs)]
    return hrs

def parse_columns(list):
    # only works on same size lists
    # this assumes that the input is an nxn matrix
    columns = [[] for i in range(len(list[0]))]

    for hrs in list:
        for i, h in enumerate(hrs):
            columns[i].append(h) 
 
    return columns

def extract_hrs(list):
    extracted_hrs = [[] for i in range(len(list))]
    for i, hrs in enumerate(list):
        for h in hrs:
            if h[1] != 0:
                extracted_hrs[i].append(h[0]) 
            continue
    
    return extracted_hrs

# print(parse_columns(sample_list))
# print(extract_hrs(parse_columns(sample_list)))

def eval_sched(extracted_hrs, req_hrs):
    hrs_sum = []
    for hrs in extracted_hrs:
        hrs_sum.append(sum(hrs))
    return True if hrs_sum == req_hrs else False

def schedule(hrs):
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


# print(assign_day_offs(sample))
new_sched = schedule(sample)
sched_2 = schedule(sample_2)
sched_3 = schedule(sample_3)
# present_sched(new_sched) 
present_sched(sched_3, sample_3)