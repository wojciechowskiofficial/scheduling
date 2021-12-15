import sys
from timeit import default_timer as timer

def goodInAnyOther(lider, new_fin, new_machine, start_time, machines):
    st = start_time.copy()
    st[new_machine] = new_fin
    for m in range(len(machines)):
        if max(st[m], lider[1])+(lider[0]/machines[m]) < lider[2]:
            return True
    return False

def canBeInOtherMachine(new_fin, limit, actual_machine):
    for i in range(len(new_fin)):
        if i == actual_machine:
            continue
        if new_fin[i] <= limit:
            return True
    return False

def listowy(argv):
    filename = argv[0]
    infile = open(filename, "r")
    tasks = []
    n = int(infile.readline())
    maszyny = list(map(float, infile.readline().split()))
    for _ in range(n):
        tasks.append(list(map(int, infile.readline().split())))

    fin_list = [[], [], [], []]
    kara = 0
    start_time = [0, 0, 0, 0]
    to_read = tasks.copy()
    for _ in range(n):
        lider = None
        lider_machine = None
        best_fin = 9999999999999999999999
        for index, t in enumerate(tasks):
            new_fin = []
            for m in range(4):
                new_fin.append(max(start_time[m], t[1])+(t[0]/maszyny[m]))
            nf = min(new_fin)
            nf_index = new_fin.index(nf)
            if (lider == None) or (nf_index!=lider_machine and nf < best_fin) or (nf < lider[1]) or (nf < best_fin and goodInAnyOther(lider, nf, nf_index, start_time, maszyny) == True and t[3] > lider[3]) or (nf < best_fin and goodInAnyOther(lider, nf, nf_index, start_time, maszyny) == False and t[3] < lider[3] and canBeInOtherMachine(new_fin, t[2], nf_index) == False):
                where = "a"
                best_fin = min(new_fin)
                lider = t
                lider_machine = nf_index

        start_time[lider_machine] = best_fin
        if best_fin>lider[2]:
            kara+=lider[3]
        fin_list[lider_machine].append(to_read.index(lider))
        tasks.remove(lider)
    file = open(argv[1], "w")
    file.write(str(kara) + "\n")
    for i in range(4):
        file.write(" ".join(str(item) for item in fin_list[i]))
        file.write("\n")



if __name__ == "__main__":
    listowy(sys.argv[1:])