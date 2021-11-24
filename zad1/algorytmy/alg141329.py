import numpy as np
import sys

INDEX = '141329'


class Process:
    def __init__(self, p, r, d, s):
        self.p = p
        self.r = r
        self.d = d if r + p < d else np.round(r + p + np.random.uniform(100)).astype(int)
        self.s = s
        self.finish = -1


def get_processes(f):
    n = int(f.readline())
    ps = []
    for _ in range(n):
        p, r, d = [int(i) for i in f.readline().split()]
        ps.append(Process(p, r, d, []))

    for i in ps:
        i.s = [int(i) for i in f.readline().split()]

    return ps


def run1(in_fname, out_fname):
    in_f = open(in_fname)
    out_f = open(out_fname, 'w')

    ps = get_processes(in_f)
    n = len(ps)
    ps_dict = dict(zip(list(range(n)), ps))

    time = 0
    lmax = np.inf
    order = []
    while len(ps_dict) >= 1:
        el = min(ps_dict.items(), key=lambda x: x[1].d)

        if el[1].r > time:
            time = el[1].r

        time += el[1].p

        if lmax < time - el[1].d:
            lmax = time - el[1].d

        ps_dict.pop(el[0])
        order.append(el[0])

    out_f.write(f'{lmax}\n')
    out_f.write(f'{" ".join([str(c) for c in order])}')

    in_f.close()
    out_f.close()


def run2(in_fname, out_fname):
    in_f = open(in_fname)
    out_f = open(out_fname, 'w')

    ps = get_processes(in_f)
    n = len(ps)
    ps_dict = dict(zip(list(range(n)), ps))

    time = 0
    lmax = -np.inf
    order = []
    last = Process(0, 0, 0, [0] * n)
    for _ in range(n):
        table = [[0]] * n
        for i, process in ps_dict.items():
            start_time = max(time + last.s[i], process.r)
            finish_time = start_time + process.p
            curr_lmax = finish_time - process.d
            table[i] = (i, start_time, finish_time, curr_lmax, 0 if curr_lmax > lmax else 1)
        table.sort(key=lambda x: (x[4], x[2]) if len(x) > 1 else (1, np.inf))
        min_item = min(table, key=lambda x: x[1] if len(x) > 1 else np.inf)
        if table[0][1] > min_item[2]:
            idx, start, finish, new_lmax, _ = min_item
        else:
            idx, start, finish, new_lmax, _ = table[0]

        lmax = max(new_lmax, lmax)

        order.append(idx)
        last = ps_dict.pop(idx)
        time = finish

    out_f.write(f'{lmax}\n')
    out_f.write(f'{" ".join([str(c) for c in order])}')

    in_f.close()
    out_f.close()


def run3(in_fname, out_fname):
    in_f = open(in_fname)
    out_f = open(out_fname, 'w')

    ps = get_processes(in_f)
    n = len(ps)
    ps = list(zip(list(range(n)), ps))

    time = 0
    lmax = -np.inf
    order = []
    last = Process(0, 0, 0, [0] * n)
    for _ in range(n):
        time_cp = max(time, min([j.r for i, j in ps]))
        ps_cp = [(i, j) for (i, j) in ps if j.r <= time_cp]
        # if not ps_cp:
        #     ps_cp = ps[:]
        ps_cp.sort(key=lambda x: x[1].d + last.s[x[0]])

        i, j = ps_cp[0]

        time += last.s[i]

        if j.r > time:
            time = j.r

        time += j.p

        lmax = max(lmax, time - j.d)
        ps.remove((i, j))
        order.append(i)
        last = j

    out_f.write(f'{lmax}\n')
    out_f.write(f'{" ".join([str(c) for c in order])}')

    in_f.close()
    out_f.close()
    return 0


if __name__ == '__main__':
    run3(sys.argv[1], sys.argv[2])
