import copy
import sys
import random
import os
def algo(instancja, algo_output):
    o = open(algo_output, "w")
    a = open(instancja, "r")
    n = int(a.readline())
    b = a.readline().split(" ")
    b = b[0:4]
    b = [float(i) for i in b]
    inpt = []  # p r d w i
    for j in range(n):
        inpt.append(a.readline().strip("\n").split(" "))
        inpt[j] = inpt[j][0:4]
        inpt[j] = [int(k) for k in inpt[j]]
        inpt[j].append(j)
    a.close()
    ewu = 0
    m = [[], [], [], []]
    time = [0, 0, 0, 0]
    times = [0, 0, 0, 0]
    i_copy = copy.copy(inpt)
    i_copy = sorted(i_copy, key=lambda x: x[1], reverse=True)
    wsk = []
    later = []
    for a in i_copy:
        wsk.append([(a[0] + a[1] + a[2])/(a[3]), a[4]])
    wsk = sorted(wsk, key=lambda x: x[0])
    wsk = [w[1] for w in wsk]
    for w in wsk:
        time_temp = copy.copy(time)
        for i in range(4):
            if time_temp[i] >= inpt[w][2]:
                time_temp[i] += (inpt[w][0]) / b[i]
            else:
                diff = inpt[w][1] - time_temp[i]
                time_temp[i] += diff + (inpt[w][0]) / b[i]
        min_time = min(time_temp)
        k = time_temp.index(min_time)
        m[k].append(w)
        time[k] += min_time
        times_copy = copy.copy(times)

        if times[k] >= inpt[w][1]:
            times[k] += (inpt[w][0]) / b[k]
            if times[k] > inpt[w][2]:
                m[k].pop()
                later.append(w)
                times[k] = times_copy[k]
        else:
            diff = inpt[w][1] - times[k]
            times[k] += diff + (inpt[w][0]) / b[k]
            if times[k] > inpt[w][2]:
                m[k].pop()
                later.append(w)
                times[k] = times_copy[k]
    for l in later:
        m[0].append(l)
    time = [0, 0, 0, 0]

    for k in range(0, 4):
        for i in m[k]:
            # print(inpt[i])
            if time[k] >= inpt[i][1]:
                time[k] += (inpt[i][0]) / b[k]
                if time[k] > inpt[i][2]:
                    ewu += inpt[i][3]
            else:
                diff = inpt[i][1] - time[k]
                time[k] += diff + (inpt[i][0]) / b[k]
                if time[k] > inpt[i][2]:
                    ewu += inpt[i][3]

    o.write(str(ewu) + "\n")
    for j in m:
        for t in j:
            if t == j[-1]:
                o.write(str(t))
            else:
                o.write(str(t) + " ")
        if j != m[-1]:
            o.write("\n")

    o.close()
    
if __name__ == '__main__':
    first_arg = sys.argv[1]
    second_arg = sys.argv[2]
    algo(first_arg, second_arg)