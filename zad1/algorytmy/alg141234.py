import sys
import numpy as np


def algo(instancja, algo_output):
    o = open(algo_output, "w")
    i = open(instancja, "r")
    n = int(i.readline())
    instancje = []  # 0 - p; 1 - r; 2 - d; 3 - index
    s = []

    for j in range(n):
        instancje.append(i.readline().strip("\n").split(" "))
        if len(instancje[j]) > 3:
            instancje[j] = instancje[j][0:3]
        instancje[j] = [int(k) for k in instancje[j]]
        instancje[j].append(j)
    for j in range(n):
        s.append(i.readline().strip("\n").split(" "))
    i.close()

    r = [int(inst[1]) for inst in instancje]
    d = [int(inst[2]) for inst in instancje]
    r_norm = np.linalg.norm(r)
    d_norm = np.linalg.norm(d)
    r_norm_arr = [j * 1000 / r_norm for j in r]
    d_norm_arr = [j * 1000 / d_norm for j in d]

    norm_sum = []
    for j in range(n):
        norm_sum.append(int(r_norm_arr[j] + 2 * d_norm_arr[j]))

    instancje = [x for _, x in sorted(zip(norm_sum, instancje))]

    l_max = -100000
    time = int(instancje[0][1] + instancje[0][0])  # ready + processing time

    for i in range(1, n):
        if int(instancje[i][1]) <= time:  # ready time <= time
            time += int(s[int(instancje[i - 1][3])][int(instancje[i][3])])
            time += int(instancje[i][0])
        else:
            time += int(s[int(instancje[i - 1][3])][int(instancje[i][3])])
            if int(instancje[i][1]) <= time:
                time += int(instancje[i][0])
            else:
                time += (int(instancje[i][0]) - time) + int(instancje[i][1])

        if time - int(instancje[i][2]) > l_max:
            l_max = time - int(instancje[i][2])
    # print(l_max)

    o.write(str(l_max) + "\n")
    for j in range(n):
        if j == n - 1:
            o.write(str(instancje[j][3]))
        else:
            o.write(str(instancje[j][3]) + " ")
    o.close()


if __name__ == '__main__':
    instancja = sys.argv[1]
    out_file_name = sys.argv[2]
    algo(instancja, out_file_name)