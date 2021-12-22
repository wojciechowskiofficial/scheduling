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
    data = np.empty(shape=(n, 7), dtype=np.int64)
    for i in range(n):
        for j in range(7):
            data[i, j] = int(next(gen_one_string_in))
    # m are the completion times of the previous tasks
    m = np.zeros(shape=4, dtype=np.int64)
    # load the scheduling output file
    with open(sys.argv[2], 'r') as f:
        one_string_in = f.read().split()
    gen_one_string_in = iter(one_string_in)
    obj_given = int(next(gen_one_string_in))
    sch = np.empty(shape=n, dtype=np.int64)
    for i in range(n):
        sch[i] = int(next(gen_one_string_in))
    # validate
    obj_computed = 0
    m[0] = data[sch[0], 0]
    for i in range(1, 4, 1):
        m[i] = m[i - 1] + data[sch[0], i]
    obj_computed += compute_singular_obj(m[3], data[sch[0], 4], data[sch[0], 5], data[sch[0], 6])
    for i in range(1, n, 1):
        m[0] += data[sch[i], 0]
        for j in range(1, 4, 1):
            m[j] = max(m[j - 1], m[j]) + data[sch[i], j]
        obj_computed += compute_singular_obj(m[3], data[sch[i], 4], data[sch[i], 5], data[sch[i], 6])
    print(obj_computed)

if __name__ == '__main__':
    Main()
