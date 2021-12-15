import sys
import numpy as np

def main(in_file, out_file):
    count, machines, tasks = load_data(in_file=in_file)
    delay_weight, order = process(count, machines, tasks)
    save_data(out_file, delay_weight, order)


def test(in_file, out_file):
    count, _, _ = load_data(in_file=in_file)
    x = count // 4
    ch = 0
    order = [[], [], [], []]
    for ii in range(4):
        for i in range(ch, x + ch):
            order[ii].append(i)
        ch += x
    for i in range(ch, count):
        order[3].append(i)
    save_data(out_file, 0, order)



def process(count, machines, tasks: np.ndarray):
    delay_weight = 0
    order = [[],[],[],[]]
    late = []
    current = [0,0,0,0]
    task_ids = np.array(range(count))
    while(tasks.shape[0] > 0):
        #sys.stderr.write(str(current)+"\n")
        to_del = []
        for i in range(tasks.shape[0]):
            if all([get_late(current[n], tasks[i][1], tasks[i][0], machines[n], tasks[i][2]) for n in [0,1,2,3]]):
                late.append([tasks[i], task_ids[i]])
                to_del.append(i)
        tasks = np.delete(tasks, to_del, 0) # all not late
        task_ids = np.delete(task_ids, to_del, 0) # all not late
        to_del = []
        if tasks.shape[0] == 0:
            break
            
        #norm = np.linalg.norm(tasks[:, 3])
        #norm_weights = tasks[:, 3] / norm * 10
        remains = np.array([sum((tasks[i][2] - current[j]) * machines[j] for j in range(4))/(4*tasks[i][3]) for i in range(tasks.shape[0])])

        most_urgent_index = np.where(remains == np.amin(remains))
        most_urgent = np.array(tasks[most_urgent_index])

        heaviest_index = np.where(most_urgent[:,3] == np.amax(most_urgent[:,3]))
        heaviest = np.array(most_urgent[heaviest_index]) # get heaviest

        shortest_index = np.where(heaviest[:,0] == np.amin(heaviest[:,0]))  #v1
        shortest = np.array(heaviest[shortest_index]) # get shortest

        to_del.append(most_urgent_index[0][heaviest_index[0][shortest_index[0][0]]])  # v1
        expected = np.array([get_new_time(current[i], shortest[0][1], shortest[0][0], machines[i]) for i in range(4)])
        least = [-1, 0]
        for i in range(4):
            if least[0] == -1 and expected[i] <= shortest[0][2]:
                least = [expected[i], i]
                #sys.stderr.write("something \n")
            #sys.stderr.write(str(get_late(current[i], shortest[0][1], shortest[0][0], machines[i], shortest[0][2])) + " -> ")
            if expected[i] > least[0] and expected[i] <= shortest[0][2]:
                least = [expected[i], i]
                #sys.stderr.write(str(task_ids[most_urgent_index[0][heaviest_index[0][ shortest_index[0][0]]]])+" on "+str(i)+" : "+str(expected[i]) + " <= " + str(shortest[0][2]) + "\n")
            elif expected[i] == least[0] and machines[i] < machines[least[1]]:
                #sys.stderr.write(str(task_ids[most_urgent_index[0][heaviest_index[0][ shortest_index[0][0]]]])+": "+str(expected[i]) + " == " + str(least[0]) + "\n")
                least = [expected[i], i]

        #sys.stderr.write("\n")
        current[least[1]] = least[0] 
        order[least[1]].append(task_ids[most_urgent_index[0][heaviest_index[0][ shortest_index[0][0]]]])
        tasks = np.delete(tasks, to_del, 0) # all not done
        task_ids = np.delete(task_ids, to_del, 0) # all not late

    #sys.stderr.write("\n")
    for i in late:
        #sys.stderr.write(str(i[1]) + ", ")
        delay_weight += i[0][3]
        order[0].append(i[1])
    #sys.stderr.write("\n\n")
    return delay_weight, order


def get_new_time(current, start, processing, speed):
    time = current
    if time < start:
        time = start
    return time + float(processing)/float(speed)
    

def get_late(current, start, processing, speed, deadline):
    new_t = get_new_time(current, start, processing, speed)
    if new_t > deadline:
        return True
    return False


def load_data(in_file):
    with open(in_file, "r") as f:
        data = f.readlines()
        count = int(data[0])
        machines = np.array(data[1].rstrip().split(), dtype=float)
        tasks = np.array([np.array(x.rstrip().split(), dtype=int) for x in data[2:(count+2)]])
    return count, machines, tasks


def save_data(out_file, delay_weight, order):
    with open(out_file, "w") as f:
        print(int(delay_weight), file=f)
        for i in range(4):
            print(*order[i], file=f)


if __name__ == "__main__":
    main(in_file=sys.argv[1], out_file=sys.argv[2])
    #test(in_file=sys.argv[1], out_file=sys.argv[2])