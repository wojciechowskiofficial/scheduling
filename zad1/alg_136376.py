import argparse
import numpy as np

class Task:
    pass

def Main():
    # argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--in_name', type=str)
    parser.add_argument('--out_name', type=str)
    args = parser.parse_args()
    # load
    with open(args.in_name, 'r') as f:
        one_string_in = f.read().split()
    gen_one_string_in = iter(one_string_in)
    n = int(next(gen_one_string_in))
    prd_matrix = np.empty((n, 3), np.int64)
    for i in range(n):
        for j in range(3): 
            prd_matrix[i][j] = next(gen_one_string_in)
    s_matrix = np.empty((n, n), np.int64)
    for i in range(n):
        for j in range(n):
            s_matrix[i][j] = next(gen_one_string_in)
    # start scheduling
    curr_t = np.zeros(n)
    scheduling = list()
    p_transposed = prd_matrix[:, 0].transpose()
    r_transposed = prd_matrix[:, 1].transpose()
    d_transposed = prd_matrix[:, 2].transpose()
    ids = np.arange(n)
    next_task = -1
    l_max = 0
    for i in range(n):
        r_transposed_og = r_transposed
        if i != 0:
            print(curr_t.shape, s_matrix.shape)
            curr_t += s_matrix[next_task][:]
        r_transposed = np.where(r_transposed < curr_t, curr_t, r_transposed)
        lateness = r_transposed + p_transposed - d_transposed
        r_transposed = r_transposed_og
        if i != 0:
            p_transposed = np.delete(p_transposed, next_task)
            r_transposed = np.delete(r_transposed, next_task)
            d_transposed = np.delete(d_transposed, next_task)
            ids = np.delete(ids, next_task)
            s_matrix = np.delete(s_matrix, next_task, 0)
            s_matrix = np.delete(s_matrix, next_task, 1)
            lateness = np.delete(lateness, next_task)
        next_task = np.argmax(lateness)
        if l_max < lateness[next_task]:
            l_max = lateness[next_task]
        print(f'id: {ids[next_task]} lateness: {lateness[next_task]} curr_t: {curr_t[next_task]}')
        scheduling.append(ids[next_task])
        if i != 0:
            curr_t = np.full(shape=curr_t.shape[0] - 1, fill_value=curr_t[next_task])
        else:
            curr_t = np.full(shape=curr_t.shape, fill_value=curr_t[next_task])
        curr_t = r_transposed[next_task] + p_transposed[next_task]
        print(f'next curr_t {curr_t}')
    print(l_max)
    print(scheduling)
    exit(0)
        
    





    l_max = one_string_out[0]
    scheduling = np.empty((n, ), np.int64)
    for i in range(1, n + 1):
        scheduling[i - 1] = one_string_out[i]
    # verify
    max_late = 0
    now = 0
    for i in range(n):
        if now < prd_matrix[scheduling[i]][1]:
            now = prd_matrix[scheduling[i]][1]
        if max_late < now + prd_matrix[scheduling[i]][0] - prd_matrix[scheduling[i]][2]:
            max_late = now + prd_matrix[scheduling[i]][0] - prd_matrix[scheduling[i]][2]
        now += prd_matrix[scheduling[i]][0]
        if i != n - 1:
            now += s_matrix[scheduling[i]][scheduling[i + 1]]
    print(max_late)


if __name__ == '__main__':
    Main()
