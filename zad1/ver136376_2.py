import sys
import numpy as np
import time
import os

def Main():
    # deploy the algorithm
    command = 'python ' + sys.argv[3] + ' ' + sys.argv[1] + ' ' + sys.argv[2]
    # start timing the algorithm
    start = time.time()
    os.system(command)
    stop = time.time()
    run_time = stop - start
    # read algorithm results
    with open(sys.argv[2], 'r') as f:
        results = f.read().split()[0]
    # load
    with open(sys.argv[1], 'r') as f:
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
    with open(sys.argv[2], 'r') as f:
        one_string_out = f.read().split()
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
    print(str(results) + '\t' + str(max_late) + '\t' + str(run_time))


if __name__ == '__main__':
    Main()
