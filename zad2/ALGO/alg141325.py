import sys
import numpy as np

def read_task(task):
    f = open(task, 'r')
    n = int(f.readline())
    b_list = [float(b) for b in f.readline().strip().split(' ')]
    prdw_list = []
    for i in range(n):
        line = f.readline()
        line = [int(x) for x in line.strip().split(' ')]
        prdw_list.append(line)
    return n, b_list, prdw_list

def save_result(file, sum_uw, order):
    f = open(file, 'w')
    f.write(str(sum_uw))
    f.write('\n')
    for i in range(4):
        f.write(" ".join([str(x) for x in order[i]]))
        f.write('\n')
    f.close()

def is_delayed(task, times):
    if task[2] < min(times):
        return True
    else:
        return False

def algorithm(n, b_list, data_prdw):
    order = [[],[],[],[]]
    times = [0, 0, 0, 0]
    ps = [p[0] for p in data_prdw]
    epsilon = 0.05 * np.mean(ps)
    data_prdw_copy = data_prdw.copy()
    tasks_weights = sorted(list(set([x[3] for x in data_prdw])), reverse=True)
    priorities = dict((task_weight,[]) for task_weight in tasks_weights)
    delayed = []
    for key in priorities.keys():
        for task in data_prdw:
            if task[3] == key:
                priorities[key].append(task)
    for priority in priorities.values():
        priority.sort(key=(lambda x: ((x[2] * 4 + x[0]) / 5)))
    for i in range(n):
        m = times.index(min(times))
        chosen_p = None
        if len(data_prdw) == 0:
            chosen_p = delayed.pop(0)
        else:
            times[m] = max(times[m], min([p[1] for p in data_prdw]))
            for priority in priorities.values():
                for idx, p in enumerate(priority):
                    if p[1] - (epsilon / b_list[m]) <= times[m]:
                        chosen_p = p
                        priority.pop(idx)
                        break
                if chosen_p:
                    data_prdw.remove(chosen_p)
                    break
        times[m] = max(times[m], chosen_p[1])
        times[m] += chosen_p[0] / b_list[m]
        order[m].append(data_prdw_copy.index(chosen_p))
        for priority in priorities.values():
            for p in priority:
                if is_delayed(p, times):
                    delayed.append(p)
                    priority.remove(p)
                    data_prdw.remove(p)
    return order

def find_sum_uw(n, b_list, prdw_list, tasks_on_machines):
    uw = 0
    for i in range(4):
        run_time = 0
        for task in tasks_on_machines[i]:
            run_time = max(run_time, prdw_list[task][1]) + prdw_list[task][0] / b_list[i]
            if run_time > prdw_list[task][2]:
                uw += prdw_list[task][3]
    return uw

def calculate(in_f, out_f):
    n, b_list, prdw_list = read_task(in_f)
    order = algorithm(n, b_list, prdw_list.copy())
    sum_uw = find_sum_uw(n, b_list, prdw_list, order)
    save_result(out_f, sum_uw, order)

if __name__ == '__main__':
    calculate(sys.argv[1], sys.argv[2])
