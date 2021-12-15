import os
import sys

#klasa Job zawiera p, r, d, number - liczba reprezentująca, która to praca z kolei:
class Job:
    def __init__(self, p = 0, r = 0, d = 0, number = -1):
        self.p = p
        self.r = r
        self.d = d
        self.number = number
        
    def __str__(self):
        return "p: " + str(self.p) + ", r: " + str(self.r) + ", d: " + str(self.d) + ", nr: " + str(self.number) + "\n"
        
def maximum(a, b):
    if a >= b:
        return a
    return b

#naiwny/sztuczny algorytm:
def solveNaive(fileName):
    separate = fileName.split("_")
    index = separate[1]

    file = open(fileName, "r")
    lines = file.readlines()
    
    n = int(lines[0])

    result = open("out_" + index + "_" + str(n) + ".txt", "w+")
    result.write(str(0))
    result.write("\n")
    
    for i in range(n - 1):
        result.write(str(i) + " ")
    result.write(str(n - 1))
    
    result.close()
    
#algorytm:
def solve(fileName):
    #liczenie indeksu:
    separate = fileName.split("_")
    index = separate[1]

    #otwieranie instancji:
    file = open(fileName, "r")
    
    #lines zawiera wersy instancji
    lines = file.readlines()
    
    #rozmiar instancji to n:
    n = int(lines[0])
    
    #lista prac i czytanie z pliku:
    jobs = []
    for i in range(n):
        line = lines[i + 1].split(" ")
        p = int(line[0])
        r = int(line[1])
        d = int(line[2])
        jobs.append(Job(p, r, d, i))
        
    #macierz przezbrojeń i czytanie z pliku:
    rearmings = []
    for i in range(n + 1, n + n + 1):
        line = lines[i].split(" ")
        times = []
        for j in range(n):
            times.append(int(line[j]))
        rearmings.append(times)
        
    #
    order = []
    delays = []
    lmax = 0
    timestamp = 0
    for i in range(n):
        #print("LEN:", len(order))
        #first element:
        if i == 0:
            #start is timestamp in which job starts:
            start = maximum(timestamp, jobs[0].r)
            #minimum here is max(0, delay it creates if it starts at start):
            minimum = maximum(0, start + jobs[0].p - jobs[0].d)
            #list of all minimum delay jobs:
            minimumValues = []
            #finding minimum:
            for j in range(1, len(jobs)):
                start = maximum(timestamp, jobs[j].r)
                delay = maximum(0, start + jobs[j].p - jobs[j].d)
                if delay < minimum:
                    minimum = delay
            #adding jobs with minimum delay to minimumValues:
            for j in range(len(jobs)):
                start = maximum(timestamp, jobs[j].r)
                delay = maximum(0, start + jobs[j].p - jobs[j].d)
                if delay == minimum:
                    minimumValues.append(jobs[j])
            #now from all the jobs in minimumValues we have to find the one that ends the earliest:
            start = maximum(timestamp, minimumValues[0].r)
            minimum = start + minimumValues[0].p
            minimumJob = minimumValues[0]
            for j in range(1, len(minimumValues)):
                start = maximum(timestamp, minimumValues[j].r)
                endTime = start + minimumValues[0].p
                if endTime < minimum:
                    minimum = endTime
            for j in range(len(minimumValues)):
                start = maximum(timestamp, minimumValues[j].r)
                endTime = start + minimumValues[0].p
                if endTime == minimum:
                    minimumJob = minimumValues[j]
                    break
            #updating timestamp:
            start = maximum(timestamp, minimumJob.r)
            #adding the job:
            order.append(minimumJob)
            timestamp = start + minimumJob.p
            #remove job from jobs:
            jobs.remove(minimumJob)
            #add delay to delays:
            delay = start + minimumJob.p - minimumJob.d
            delays.append(maximum(0, delay))
            #print("start:", start, "ts:", timestamp, "delay:", delay, "p:", minimumJob.p, "d:", minimumJob.d)
            #print(minimumJob.p, minimumJob.r, minimumJob.d, minimumJob.number)
        #case when there are already jobs in order, so we can refer to the previous job:
        else:
            #start is timestamp in which job starts:
            start = maximum(timestamp + rearmings[order[len(order) - 1].number][jobs[0].number], jobs[0].r)
            #minimum here is max(0, delay it creates if it starts at start):
            minimum = maximum(0, start + jobs[0].p - jobs[0].d)
            #list of all minimum delay jobs:
            minimumValues = []
            #finding minimum:
            for j in range(1, len(jobs)):
                start = maximum(timestamp + rearmings[order[len(order) - 1].number][jobs[j].number], jobs[j].r)
                delay = maximum(0, start + jobs[j].p - jobs[j].d)
                if delay < minimum:
                    minimum = delay
            #adding jobs with minimum delay to minimumValues:
            for j in range(len(jobs)):
                start = maximum(timestamp + rearmings[order[len(order) - 1].number][jobs[j].number], jobs[j].r)
                delay = maximum(0, start + jobs[j].p - jobs[j].d)
                if delay == minimum:
                    minimumValues.append(jobs[j])
            #now from all the jobs in minimumValues we have to find the one that ends the earliest:
            start = maximum(timestamp + rearmings[order[len(order) - 1].number][minimumValues[0].number], minimumValues[0].r)
            minimum = start + minimumValues[0].p
            minimumJob = minimumValues[0]
            for j in range(1, len(minimumValues)):
                start = maximum(timestamp + rearmings[order[len(order) - 1].number][minimumValues[j].number], minimumValues[j].r)
                endTime = start + minimumValues[0].p
                if endTime < minimum:
                    minimum = endTime
            for j in range(len(minimumValues)):
                start = maximum(timestamp + rearmings[order[len(order) - 1].number][minimumValues[j].number], minimumValues[j].r)
                endTime = start + minimumValues[0].p
                if endTime == minimum:
                    minimumJob = minimumValues[j]
                    break
            #updating timestamp:
            #print(order[len(order) - 1].number)
            #print(minimumJob.number)
            start = maximum(timestamp + rearmings[order[len(order) - 1].number][minimumJob.number], minimumJob.r)
            #adding the job:
            order.append(minimumJob)
            timestamp = start + minimumJob.p
            #remove job from jobs:
            jobs.remove(minimumJob)
            #add delay to delays:
            delay = start + minimumJob.p - minimumJob.d
            delays.append(maximum(0, delay))
            #print("start:", start, "ts:", timestamp, "delay:", delay, "p:", minimumJob.p, "d:", minimumJob.d)
            #print(minimumJob.p, minimumJob.r, minimumJob.d, minimumJob.number)

    #print(delays)

    #plik wynikowy:
    result = open("out_" + index + "_" + str(n) + ".txt", "w+")
    result.write(str(max(delays)))
    result.write("\n")
    for i in range(len(order) - 1):
        result.write(str(order[i].number) + " ")
    result.write(str(order[len(order) - 1].number))
    result.close()

def getD(job):
    return job.d

def solveD(fileName):
    #liczenie indeksu:
    separate = fileName.split("_")
    index = separate[1]

    #otwieranie instancji:
    file = open(fileName, "r")
    
    #lines zawiera wersy instancji
    lines = file.readlines()
    
    #rozmiar instancji to n:
    n = int(lines[0])
    
    #lista prac i czytanie z pliku:
    jobs = []
    for i in range(n):
        line = lines[i + 1].split(" ")
        p = int(line[0])
        r = int(line[1])
        d = int(line[2])
        jobs.append(Job(p, r, d, i))
        
    #macierz przezbrojeń i czytanie z pliku:
    rearmings = []
    for i in range(n + 1, n + n + 1):
        line = lines[i].split(" ")
        times = []
        for j in range(n):
            times.append(int(line[j]))
        rearmings.append(times)
        
    #
    jobs.sort(key = getD)

    #plik wynikowy:
    result = open("out_" + index + "_" + str(n) + ".txt", "w+")
    result.write("0")
    result.write("\n")
    for i in range(len(jobs) - 1):
        result.write(str(jobs[i].number) + " ")
    result.write(str(jobs[len(jobs) - 1].number))
    result.close()

timestamp = 0
order = []
rearmings = []

def keyD(job):
    return job.d
    
def keyL(job):
    global timestamp
    global order
    global rearmings
    start = 0
    if len(order) == 0:
        start = maximum(timestamp, job.r)
    else:
        start = maximum(timestamp + rearmings[order[len(order) - 1].number][job.number], job.r) 
    delay = start + job.p - job.d
    return delay
    
def keyEnd(job):
    global timestamp
    global order
    global rearmings
    start = 0
    if len(order) == 0:
        start = maximum(timestamp, job.r)
    else:
        start = maximum(timestamp + rearmings[order[len(order) - 1].number][job.number], job.r)
    end = start + job.p
    return end

def solveThree(fileName):
    #liczenie indeksu:
    separate = fileName.split("_")
    index = separate[1]

    #otwieranie instancji:
    file = open(fileName, "r")
    
    #lines zawiera wersy instancji
    lines = file.readlines()
    
    #rozmiar instancji to n:
    n = int(lines[0])
    
    #lista prac i czytanie z pliku:
    jobs = []
    for i in range(n):
        line = lines[i + 1].split(" ")
        p = int(line[0])
        r = int(line[1])
        d = int(line[2])
        jobs.append(Job(p, r, d, i))
        
    #macierz przezbrojeń i czytanie z pliku:
    global rearmings
    for i in range(n + 1, n + n + 1):
        line = lines[i].split(" ")
        times = []
        for j in range(n):
            times.append(int(line[j]))
        rearmings.append(times)
        
    #
    global order
    Lmax = 0
    for i in range(n):
        sortedD = sorted(jobs, key = keyD)
        #sortedL = sorted(jobs, key = keyL, reverse = False)
        #for x in range(len(sortedL)):
            #print(sortedL[x].p + sortedL[x].r - sortedL[x].d)
        #sys.exit()
        sortedEnd = sorted(jobs, key = keyEnd)
        #if i == 0:
            #print(*sortedD)
            #print(*sortedL)
            #print(*sortedEnd)
            
        scores = {}
        for j in range(len(jobs)):
            scores[jobs[j]] = 1
            
        for j in range(len(jobs)):
            scores[sortedD[j]] *= (j + 1)
            #scores[sortedL[j]] *= (j + 1)
            scores[sortedEnd[j]] *= (j + 1)
            
        lowestScoreJob = min(scores, key = scores.get)
            
        global timestamp
        start = 0
        if len(order) == 0:
            start = maximum(timestamp, lowestScoreJob.r)
        else:
            start = maximum(timestamp + rearmings[order[len(order) - 1].number][lowestScoreJob.number], lowestScoreJob.r)
        timestamp = start + lowestScoreJob.p
        delay = timestamp - lowestScoreJob.d
        if i == 0:
            Lmax = delay
        else:
            if delay > Lmax:
                Lmax = delay
        
        order.append(lowestScoreJob)
        jobs.remove(lowestScoreJob)
        
    #print(*order)
    
    result = open("out_" + index + "_" + "136761" + "_" + str(n) + ".txt", "w+")
    result.write(str(Lmax))
    result.write("\n")
    for i in range(len(order) - 1):
        result.write(str(order[i].number) + " ")
    result.write(str(order[len(order) - 1].number))
    result.close()

def main():
    #path = os.path.dirname(os.path.realpath(__file__))
    
    #for file in os.listdir(path):
        #if file.endswith(".txt") and file.startswith("in_"):
            #print("processing file: ", os.path.join(path, file))
            #print("processing file: " + file)
            #testSolve(file)
            
    fileName = sys.argv[1]
    #print("processing file: " + fileName)
    #solveNaive(fileName)
    #solve(fileName)
    #solveD(fileName)
    solveThree(fileName)
    
main()