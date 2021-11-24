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
    with open(sys.argv[2], 'r') as f:
        one_string_out = f.read().split('\n')
    objective = one_string_out[0]
    true_obj = 0
    for i in range(1, 5, 1):
        scheduling = [int(value) for value in one_string_out[i].split(' ')[:-1]]
        curr_t = 0
        for task_id in scheduling:
            curr_t = max(curr_t, rs[task_id])
            scaled_pi = ps[task_id] / bs[i -1]
            completion = curr_t + scaled_pi
            if completion > ds[task_id]:
                true_obj += ws[task_id]
            curr_t += scaled_pi
    print(true_obj)

if __name__ == '__main__':
    Main()
