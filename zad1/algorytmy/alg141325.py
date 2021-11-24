from sys import argv
import math


def read_task(task):
    f = open(task, 'r')
    n = int(f.readline())
    data_prd = []
    data_s = []
    for i in range(n):
        line = f.readline()
        line = [int(x) for x in line.strip().split(' ')]
        line.append(i)
        data_prd.append(line)
    for i in range(n):
        line = f.readline()
        line = [int(x) for x in line.strip().split(' ')]
        data_s.append(line)
    f.close()
    return n, data_prd, data_s


def save_result(file, lmax, order):
    f = open(file, 'w')
    f.write(str(lmax))
    f.write('\n')
    f.write(" ".join([str(x) for x in order]))
    f.close()


def algorithm(n, data_prd, data_s):
    order = []
    time = 0
    s = 0
    last_process = None
    epsilon = 0.1 * min([p[0] for p in data_prd])
    for _ in range(n):
        chosen_p = None
        if last_process:
                data_prd.sort(key=(lambda x: ((x[2] * 20 + data_s[last_process[3]][x[3]]) * 10 + (x[2] - x[1] - x[0]) * 10) / 40))
        else:
                data_prd.sort(key=(lambda x: ((x[2] * 20 + (x[2] - x[1] - x[0]) * 10) / 30)))

        time = max(time, min([p[1] for p in data_prd]))
        for p in data_prd:
            if p[1] - epsilon <= time:
                chosen_p = p
                break
        if last_process:
            s = data_s[last_process[3]][chosen_p[3]]
        time = max(time, chosen_p[1])
        time += chosen_p[0] + s
        last_process = chosen_p
        order.append(chosen_p[3])
        data_prd.remove(last_process)
    return order


def find_lmax(data_prd, data_s, order):
    time = 0
    lmax = -math.inf
    for i in range(len(order)):
        if i != 0:
            time += data_s[order[i - 1]][order[i]]
        if time < data_prd[order[i]][1]:
            time = data_prd[order[i]][1]
        time += data_prd[order[i]][0]
        if time - data_prd[order[i]][2] > lmax:
            lmax = time - data_prd[order[i]][2]
    return lmax


def calculate(in_f, out_f):
    n, data_prd, data_s = read_task(in_f)
    data_prd_copy = data_prd.copy()
    order = algorithm(n, data_prd_copy, data_s)
    lmax = find_lmax(data_prd, data_s, order)
    save_result(out_f, lmax, order)


if __name__ == "__main__":
    calculate(argv[1], argv[2])
