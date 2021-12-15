import sys
import numpy as np

def Main():
    # load
    with open(sys.argv[1], 'r') as f:
        one_string_in = f.read().split()
    gen_one_string_in = iter(one_string_in)
    n = int(next(gen_one_string_in))
    bs = np.empty((4, ), np.float32)
    for i in range(4):
        bs[i] = next(gen_one_string_in)
    prdw_matrix = np.empty((n, 4), np.int64)
    for i in range(n):
        for j in range(4): 
            prdw_matrix[i][j] = next(gen_one_string_in)
    prdw_matrix = prdw_matrix.transpose()
    ps = prdw_matrix[0]
    rs = prdw_matrix[1]
    ds = prdw_matrix[2]
    ws = prdw_matrix[3]
    og_ps = ps
    og_rs = rs
    og_ds = ds
    og_ws = ws
    # compute
    # argsort over rs
    sorted_ids = np.argsort(rs)
    original_ids = np.arange(n)
    original_ids = original_ids[sorted_ids]
    ps = ps[sorted_ids]
    rs = rs[sorted_ids]
    ds = ds[sorted_ids]
    ws = ws[sorted_ids]
    # init
    c_mem = np.full((4), fill_value=0, dtype=np.float32)
    clock = 0
    obj = 0
    schedule = list()
    for i in range(4):
        schedule.append(list())
    # schedule
    for i in range(n):
        machine = 0
        # choose machine
        while True:
            is_break = False
            # check if able to schedule ith task with no
            # lateness, and if yes schedule at least 
            # powerful machine
            for j in range(4):
                c_i = rs[i] + ps[i] / bs[j]
                if c_i <= ds[i] and c_mem[j] <= clock and rs[i] <= clock:
                    machine = j
                    is_break = True
                    break
            # update and go to next task
            if is_break:
                schedule[machine].append(i)
                c_mem[machine] = max(clock, rs[i]) + ps[i] / bs[machine]
                break
            # check if able to schedule ith task at all,
            # and if yes schedule at least powerful machine
            for j in range(4):
                c_i = rs[i] + ps[i] / bs[j]
                if c_mem[j] <= clock and rs[i] <= clock:
                    machine = j
                    is_break = True
                    break
            # update and go to next task
            if is_break:
                schedule[machine].append(i)
                c_mem[machine] = max(clock, rs[i]) + ps[i] / bs[machine]
                break
            # cannot schedule with or without lateness
            # either all machines are computing or
            # no task is available 
            # increment clock == wait
            else:
                # increment clock in such way, that
                # it increases to the moment
                # when next feasible action occurs
                inc = max(min(c_mem), rs[i])
                clock += inc
    for i in range(4):
        for j in range(len(schedule[i])):
            schedule[i][j] = np.where(sorted_ids == schedule[i][j])[0][0]
    ps = og_ps
    rs = og_rs
    ds = og_ds
    ws = og_ws
    for i in range(4):
        clock = 0
        for task_id in schedule[i]:
            clock = max(clock, rs[task_id])
            scaled_pi = ps[task_id] / bs[i]
            completion = clock + scaled_pi
            if completion > ds[task_id]:
                obj += ws[task_id]
            clock += scaled_pi
    to_string = lambda x : [str(el) for el in x]
    for i in range(len(schedule)):
        schedule[i] = ' '.join(to_string(schedule[i]))
    with open(sys.argv[2], 'w') as f:
        f.write(str(obj))
        f.write('\n')
        for i in range(4):
            f.write(schedule[i] + ' ')
            f.write('\n')

if __name__ == '__main__':
    Main()
