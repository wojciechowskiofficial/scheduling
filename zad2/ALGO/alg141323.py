import os
import math
import sys
import time


def load_input(filename):
    f = open(f'{filename}', "r+")
    content = f.read().split("\n")
    n = int(content[0])
    machine_speeds = [float(x) for x in content[1].split(' ') if x != '']
    gen_tab = []
    for i in range(2, n + 2):
        gen_tab.append([int(x) for x in content[i].split(' ') if x != ''])
    return n, machine_speeds, gen_tab


def split_tasks(filename):
    n, machines_speeds, gen_tab = load_input(filename)
    results = ["", "", "", ""]
    times = [0, 0, 0, 0]
    free_tasks = [x for x in range(n)]
    surely_late = []
    lateness = 0
    while len(free_tasks) > 0:
        for i in free_tasks:
            flag = False
            for en, time in enumerate(times):
                t = time
                if time < gen_tab[i][1]:
                    t = gen_tab[i][1]
                if t + gen_tab[i][0]/machines_speeds[en] <= gen_tab[i][2]:
                    flag = True
                    break
            if not flag:
                surely_late.append(i)
                free_tasks.pop(free_tasks.index(i))
        if len(free_tasks) == 0:
            break
        data = []
        for i in free_tasks:
            shift = [time - gen_tab[i][1] for time in times]
            shift_abs = [abs(x) for x in shift]
            min_shift = min(shift_abs)
            min_id = shift_abs.index(min_shift)
            data.append([i, shift[min_id], min_id])

        weights = []
        for i in data:
            t = times[i[2]]
            if gen_tab[i[0]][1] > t:
                t = gen_tab[i[0]][1]
            if gen_tab[i[0]][0]/machines_speeds[i[2]] + t <= gen_tab[i[0]][2]:
                weights.append([i[0], gen_tab[i[0]][3], i[2]])
        if len(weights) > 0:
            max_w = max([x[1] for x in weights])

            for i in weights:
                if i[1] == max_w:
                    best_choice = i
                    break

        else:
            new_weights = []
            for i in data:
                new_weights.append([i[0], gen_tab[i[0]][3], i[2]])

            min_w = min([x[1] for x in new_weights])
            for i in new_weights:
                if i[1] == min_w:
                    best_choice = i
                    lateness += gen_tab[best_choice[0]][3]
                    break

        results[best_choice[2]] += str(best_choice[0]) + ' '
        if times[best_choice[2]] < gen_tab[best_choice[0]][1]:
            times[best_choice[2]] = gen_tab[best_choice[0]][1] + gen_tab[best_choice[0]][0]
        else:
            times[best_choice[2]] += gen_tab[best_choice[0]][0]
        free_tasks.pop(free_tasks.index(best_choice[0]))

    for i in surely_late:
        results[0] += str(i) + ' '
        lateness += gen_tab[i][3]
    return lateness, results


lateness, res = split_tasks(sys.argv[1])
f = open(sys.argv[2], "w+")
f.write(f'{lateness}\n')
for i in res:
    f.write(f'{i}\n')
f.close()
# file = open("times.csv", "w+")
# for i in os.listdir("in"):
#     start = time.time()
#     lateness, res = split_tasks(i)
#     end = time.time()
#     czas = str(round(end - start, 5))
#     new_czas = ""
#     for c in czas:
#         if c == '.':
#             new_czas += ','
#         else:
#             new_czas += c
#     file.write(f'{i};{new_czas}\n')
#     f = open(f'out\\out_{i[3:]}', "w+")
#     f.write(f'{lateness}\n')
#     for j in res:
#         f.write(f'{j}\n')
#     f.close()
