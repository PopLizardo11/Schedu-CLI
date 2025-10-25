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

def parse_columns(list, no_tup=False):
    # only works on same size lists
    # this assumes that the input is an nxn matrix
    columns = [[] for i in range(len(list[0]))]

    for hrs in list:
        for i, h in enumerate(hrs):
            columns[i].append(h) if no_tup else columns[i].append(h[0])
 
    return columns

def eval_sched(usable_hrs, init_hrs):
    hrs_sum = []
    for hrs in usable_hrs:
        hrs_sum.append(sum(hrs))
    return True if hrs_sum == init_hrs else False

def schedule(hrs):
    sched = []
    columns = []
    for i in range(7):
        hrs = assign_day_offs(hrs)
        sched.append(hrs)
        hrs = [minus_step(h) for h in hrs]
    return sched

def present_sched(sched):
    for hrs in sched:
        stf = ""
        for h in hrs:
            if h[0] == 0:
                stf += (f"{h[1]}* ")
                continue
            stf += (f"{h[1]} ")
        print(stf)


# print(assign_day_offs(sample))
new_sched = schedule(sample)
# present_sched(new_sched) 