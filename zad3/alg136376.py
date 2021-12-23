import sys
import numpy as np

def compute_singular_obj(c, d, a, b) -> int:
    return a * max(0, d - c) + b* max(0, c - d)


def Main():
    # load the data
    with open(sys.argv[1], 'r') as f:
        one_string_in = f.read().split()
    gen_one_string_in = iter(one_string_in)
    n = int(next(gen_one_string_in))
    data = np.empty(shape=(n, 8), dtype=np.int64)
    for i in range(n):
        for j in range(7):
            data[i, j] = int(next(gen_one_string_in))
    # compute mean operation duration
    mean_op = int(np.mean(np.sum(data[:,:4], axis=1)))
    #   add ids as last column
    for i in range(n):
        data[i,-1] = i
    # assign initial task
    #   choose first task
    task_list = list()
    for i in range(n):
        task_list.append(data[i])
    min_d = task_list[0][4]
    min_i = 0
    for i in range(n):
        if task_list[i][4] < min_d:
            min_d = task_list[i][4]
            min_i = i
    #   m are the completion times of the previous tasks
    m = np.zeros(shape=4, dtype=np.int64)
    #   fill up inital m values with task_list[min_i] values
    m[0] = task_list[min_i][0]
    m[1] = m[0] + task_list[min_i][1]
    m[2] = m[1] + task_list[min_i][2]
    m[3] = m[2] + task_list[min_i][3]
    #   add initial task to scheduling
    scheduling = list()
    scheduling.append(min_i)
    #   del initial task from remaining tasks
    del task_list[min_i]
    # schedule
    #                                                       PAMIETAJ O TYM ZEBY PAMIETAC O TYM ZE W PEWNYM MOMENCIE ZADNE ZADANIE NIE POZOSTANIE PO MI PRZED D
    for i in range(n - 1):
        #   sieve prioritized
        prioritized = list()
        neglectable = list()
        for j in range(len(task_list)):
            m_curr = np.zeros(shape=4, dtype=np.int64)
            for k in range(4):
                m_curr[k] = m[k]
            m_curr[0] += task_list[j][0]
            for k in range(1, 4, 1):
                m_curr[k] = max(m_curr[k - 1], m_curr[k]) + task_list[j][k]
            #   if after adding mean_op still befor it's d add to neglectable
            if m_curr[3] + mean_op < task_list[j][4]:
                # print(m_curr[3] + mean_op, task_list[j][4])
                neglectable.append(task_list[j])
            #   if after adding mean_op task goes from being to early 
            #   to being to late add to prioritized
            else:
                prioritized.append(task_list[j])
        #   if after adding mean_op no task would be late
        if len(prioritized) > 0:
            max_obj = 0
            max_j = 0
            max_m = None
            #   find least early task
            for j in range(len(prioritized)):
                m_curr = np.zeros(shape=4, dtype=np.int64)
                for k in range(4):
                    m_curr[k] = m[k]
                m_curr[0] += prioritized[j][0]
                for k in range(1, 4, 1):
                    m_curr[k] = max(m[k - 1], m_curr[k]) + prioritized[j][k]
                if compute_singular_obj(m_curr[3], prioritized[j][4], prioritized[j][5], prioritized[j][6]) > max_obj:
                    max_obj = compute_singular_obj(m_curr[3], prioritized[j][4], prioritized[j][5], prioritized[j][6]) > max_obj
                    max_j = j
                    max_m = m_curr
            scheduling.append(prioritized.pop(max_j)[-1])
            m = max_m
        else:
            min_obj = 0
            min_j = 0
            min_m = None
            #   find least early task
            for j in range(len(neglectable)):
                m_curr = np.zeros(shape=4, dtype=np.int64)
                for k in range(4):
                    m_curr[k] = m[k]
                m_curr[0] += neglectable[j][0]
                for k in range(1, 4, 1):
                    m_curr[k] = min(m[k - 1], m_curr[k]) + neglectable[j][k]
                if compute_singular_obj(m_curr[3], neglectable[j][4], neglectable[j][5], neglectable[j][6]) > min_obj:
                    min_obj = compute_singular_obj(m_curr[3], neglectable[j][4], neglectable[j][5], neglectable[j][6]) > min_obj
                    min_j = j
                    min_m = m_curr
            scheduling.append(neglectable.pop(min_j)[-1])
            m = min_m
        task_list = prioritized + neglectable
    # compute_obj
    obj_computed = 0
    m = np.zeros(shape=4, dtype=np.int64)
    m[0] = data[scheduling[0], 0]
    for i in range(1, 4, 1):
        m[i] = m[i - 1] + data[scheduling[0], i]
    obj_computed += compute_singular_obj(m[3], data[scheduling[0], 4], data[scheduling[0], 5], data[scheduling[0], 6])
    for i in range(1, n, 1):
        m[0] += data[scheduling[i], 0]
        for j in range(1, 4, 1):
            m[j] = max(m[j - 1], m[j]) + data[scheduling[i], j]
        obj_computed += compute_singular_obj(m[3], data[scheduling[i], 4], data[scheduling[i], 5], data[scheduling[i], 6])
    print(obj_computed)

if __name__ == '__main__':
    Main()
