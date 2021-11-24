import os
import math
import sys


def search(params, setup):
    res_keys = []
    time = 0
    ratio_dict = {}
    n = len(params)
    for i in range(len(params)):
        ratio_dict.clear()
        sum_p = 0
        sum_r = 0
        sum_d = 0
        for k, v in params.items():
            sum_p += v[0]
            sum_r += v[1] - time
            sum_d += v[2] - time
        avg_p = sum_p / len(params)
        avg_r = sum_r / len(params)
        avg_d = sum_d / len(params)
        multi_p = math.sqrt(abs(avg_p) / (avg_r * avg_d if avg_r * avg_d > 0 else 1))
        multi_r = math.sqrt(abs(avg_r) / (avg_d * avg_p if avg_d * avg_p > 0 else 1))
        multi_d = math.sqrt(abs(avg_d) / (avg_r * avg_p if avg_r * avg_p > 0 else 1))
        for k, v in params.items():
            ratio_dict[k] = multi_p * (v[0] - avg_p) + multi_r * (v[1] - avg_r) + multi_d * (v[2] - avg_d)
        ratio_dict = dict(sorted(ratio_dict.items(), key=lambda item: item[1]))
        counter = math.ceil(len(params) / 10)
        top_picks = []
        for k, v in ratio_dict.items():
            if counter > 0:
                top_picks.append([k, v])
                counter -= 1
            else:
                break
        if len(res_keys) > 0:
            for i in range(len(top_picks)):
                top_picks[i][1] += setup[res_keys[-1]][top_picks[i][0]]
            top_picks.sort(key=lambda item: item[1])
        key_to_pop = top_picks[0][0]
        res_keys.append(key_to_pop)
        if time < params[key_to_pop][1]:
            time = params[key_to_pop][1] + params[key_to_pop][0]
            if len(res_keys) < n:
                time += setup[res_keys[-1]][key_to_pop]
        else:
            time += params[key_to_pop][0]
            if len(res_keys) < n:
                time += setup[res_keys[-1]][key_to_pop]
        params.pop(key_to_pop)
    return res_keys


f = open(sys.argv[1], "r+")
content = f.read().split("\n")
n = int(content[0])
gen_tab = []
setup_times = []
for i in range(1, n + 1):
    row = []
    for j in content[i].split(" "):
        if j != '':
            row.append(int(j))
    gen_tab.append(row)
for i in range(n + 1, 2 * n + 1):
    row = []
    for j in content[i].split(" "):
        if j != '':
            row.append(int(j))
    setup_times.append(row)
f.close()
gen_dict = {}
counter = 0
for i in gen_tab:
    gen_dict[counter] = i
    counter += 1

res = search(gen_dict, setup_times)

time = 0
l_tab = []
order_tab = res

counter = 1
for i in order_tab:
    if counter == n:
        if time < gen_tab[i][1]:
            time = gen_tab[i][1]
        time += gen_tab[i][0]
        fin_time = time
    else:
        if time < gen_tab[i][1]:
            time = gen_tab[i][1]
        time += gen_tab[i][0]
        fin_time = time
        time += setup_times[order_tab[counter - 1]][order_tab[counter]]
    counter += 1

    l_tab.append(fin_time - gen_tab[i][2])

f = open(sys.argv[2], "w+")
f.write(f'{max(l_tab)}\n')
for i in res:
    f.write(f'{i} ')
f.close()
