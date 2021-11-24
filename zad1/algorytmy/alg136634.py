import sys

def listowy(argv):
    filename = argv[0]
    infile = open(filename, "r")
    tasks = []
    S = []
    N = int(infile.readline())
    for _ in range(N):
        tasks.append(list(map(int, infile.readline().split())))
    for _ in range(N):
        S.append(list(map(int, infile.readline().split())))
    Order = []
    Lmax = -99999999999999999999999999999999
    StartTime = 0
    Index = 0
    for i in range(N):
        RevL = -999999999999999999999999999999999

        if i == 0:
            for n in range(N):
                score = (max(StartTime, tasks[n][1]) + tasks[n][0]) - tasks[n][2]
                taskFinTime = max(StartTime, tasks[n][1]) + tasks[n][0]
                taskStartTime = max(StartTime, tasks[n][1])
                if taskFinTime <= tasks[Index][1] or ((taskStartTime <= tasks[Index][1]+tasks[Index][0]) and (score > RevL)):
                    RevL = score
                    Index = n
            Lmax = max(Lmax, max(StartTime, tasks[Index][1]) + tasks[Index][0] - tasks[Index][2])
            StartTime = max(StartTime, tasks[Index][1]) + tasks[Index][0]
            Order.append(Index)

        else:
            nextStart = 999999999999999999999
            nextTime = 99999999999999999999
            for n in range(N):
                if n not in Order:
                    taskFinTime = max(StartTime + S[Order[-1]][n], tasks[n][1]) + tasks[n][0]
                    taskStartTime = max(StartTime + S[Order[-1]][n], tasks[n][1])
                    score = taskFinTime - tasks[n][2]
                    if taskFinTime <= nextStart or ((taskStartTime <= nextStart+nextTime) and (score > RevL)):
                        RevL = score
                        Index = n
                        nextStart = taskStartTime
                        nextTime = tasks[Index][0]
            Lmax = max(Lmax, nextStart+nextTime - tasks[Index][2])
            StartTime = max(StartTime + S[Order[-1]][Index], tasks[Index][1]) + tasks[Index][0]
            Order.append(Index)
    file = open(argv[1], "w")
    file.write(str(Lmax) + "\n")
    file.write(" ".join(str(item) for item in Order))


if __name__ == "__main__":
    listowy(sys.argv[1:])