from random import randrange
from random import uniform
from random import shuffle
from numpy import floor
from numpy import ceil
import sys
from math import sqrt

MY_INDEX = 136761
NUMBER_OF_MACHINES = 4

class Job:
    def __init__(self, p = 0, r = 0, d = 0, w = 0, id = 0):
        self.p = p
        self.r = r
        self.d = d
        self.w = w
        self.id = id

class Machine:
    def __init__(self, id = -1, speed = 0.0):
        self.id = id
        self.speed = speed

class Instance:
    def __init__(self):
        self.author = ''
        self.n = 0
        self.jobs = []
        self.machines = []

    def read(self, fileName):
        #index autora instancji:
        separate = fileName.split("_")
        self.author = separate[1]

        #otwieranie instancji:
        file = open(fileName, "r")
    
        #lines zawiera wersy instancji
        lines = file.readlines()
    
        #rozmiar instancji to n:
        self.n = int(lines[0])

        #maszyny:
        stripped = lines[1].rstrip()
        machinesSpeedsLine = stripped.split(' ')
        machineId = 0
        for machineSpeedStr in machinesSpeedsLine:
            machineSpeed = float(machineSpeedStr)
            self.machines.append(Machine(machineId, machineSpeed))
            machineId += 1

        #prace:
        jobId = 0
        for jobLine in lines[2:2 + self.n]:
            jobLine.rstrip()
            jobParametersStr = jobLine.split(' ')
            p = int(jobParametersStr[0])
            r = int(jobParametersStr[1])
            d = int(jobParametersStr[2])
            w = int(jobParametersStr[3])
            self.jobs.append(Job(p, r, d, w, jobId))
            jobId += 1
            #print(jobId)
        #print(len(self.jobs))
        #sys.exit()

    def print(self):
        print('size:', self.n)
        print('machines:')
        for machine in self.machines:
            print('   id:', machine.id, '| speed:', machine.speed)
        print('jobs:')
        for job in self.jobs:
            print('   id:', job.id, '| p:', job.p, '| r:', job.r, '| d:', job.d, '| w:', job.w)

'''
def solveTest(fileName, outFile, display = False):
    instance = Instance()
    instance.read(fileName)
    if display:
        instance.print()

    global MY_INDEX
    file = None
    if outFile == '':
        file = open('out_' + fileName[3:9] + '_' + str(MY_INDEX) + '_' + str(instance.n) + '.txt', 'w+')
    else:
        file = open(outFile, 'w+')

    file.write(str(0))

    global NUMBER_OF_MACHINES
    jobsPerMachine = instance.n // NUMBER_OF_MACHINES
    lastMachineAdditional = instance.n - jobsPerMachine * NUMBER_OF_MACHINES

    currentJobId = 0
    for i in range(0, NUMBER_OF_MACHINES):
        file.write('\n')
        if i != NUMBER_OF_MACHINES - 1:
            for j in range(0, jobsPerMachine):
                file.write(str(currentJobId))
                currentJobId += 1
                if j != jobsPerMachine - 1:
                    file.write(' ')
        else:
            for j in range(0, jobsPerMachine + lastMachineAdditional):
                file.write(str(currentJobId))
                currentJobId += 1
                if j != jobsPerMachine + lastMachineAdditional - 1:
                    file.write(' ')

    file.close()

def solve(fileName, outFile, display = False):
    global NUMBER_OF_MACHINES
    global MY_INDEX

    instance = Instance()
    instance.read(fileName)
    if display:
        instance.print()

    file = None
    if outFile == '':
        #file = open('out_' + fileName[3:9] + '_' + str(MY_INDEX) + '_' + str(instance.n) + '.txt', 'w+')
        file = open('out_' + instance.author + '_' + str(MY_INDEX) + '_' + str(instance.n) + '.txt', 'w+')
    else:
        file = open(outFile, 'w+')

    currentJobId = 0
    for i in range(0, NUMBER_OF_MACHINES):
        file.write('\n')
        if i != NUMBER_OF_MACHINES - 1:
            for j in range(0, jobsPerMachine):
                file.write(str(currentJobId))
                currentJobId += 1
                if j != jobsPerMachine - 1:
                    file.write(' ')
        else:
            for j in range(0, jobsPerMachine + lastMachineAdditional):
                file.write(str(currentJobId))
                currentJobId += 1
                if j != jobsPerMachine + lastMachineAdditional - 1:
                    file.write(' ')

    jobsLeft = instance.jobs
    sigma = 0
    timestamps = {}
    speeds = {}
    orders = {}
    for machine in instance.machines:
        speeds[machine.id] = machine.speed
        timestamps[machine.id] = 0
        orders[machine.id] = []

    while len(jobsLeft) > 0:
        scores = {}
        for job in jobsLeft:
            score = job.w * job.p / job.d
            scores[job] = score

        bestScoreJob = max(scores, key=scores.get)

        endTimes = {}
        for id in timestamps:
            endTimes[id] = max(timestamps[id], bestScoreJob.r) + (bestScoreJob.p / speeds[id])

        minEndTimeMachineId = min(endTimes, key=endTimes.get)

        timestamps[minEndTimeMachineId] = endTimes[minEndTimeMachineId]

        if timestamps[minEndTimeMachineId] > bestScoreJob.d:
            sigma += bestScoreJob.w

        orders[minEndTimeMachineId].append(bestScoreJob)

        jobsLeft.remove(bestScoreJob)

    file.write(str(sigma))

    for id in orders:
        file.write('\n')
        for x in range(0, len(orders[id])):
            if x == len(orders[id]) - 1:
                file.write(str(orders[id][x].id))
            else:
                file.write(str(orders[id][x].id) + ' ')

    file.close()

def solve2(fileName, outFile, display = False):
    global NUMBER_OF_MACHINES
    global MY_INDEX

    instance = Instance()
    instance.read(fileName)
    if display:
        instance.print()

    file = None
    if outFile == '':
        #file = open('out_' + fileName[3:9] + '_' + str(MY_INDEX) + '_' + str(instance.n) + '.txt', 'w+')
        file = open('out_' + instance.author + '_' + str(MY_INDEX) + '_' + str(instance.n) + '.txt', 'w+')
    else:
        file = open(outFile, 'w+')

    jobsLeft = instance.jobs
    sigma = 0
    timestamps = {}
    speeds = {}
    orders = {}
    for machine in instance.machines:
        speeds[machine.id] = machine.speed
        timestamps[machine.id] = 0
        orders[machine.id] = []

### MAIN LOOP ######################################################################################
    while len(jobsLeft) > 0: #n - lvl 1
        #tworzenie listy prac, które nie są jeszcze spóźnione oraz listy jakie zadania na jakich
        #maszynach nie są jeszcze spóźnione:
        notLateJobs = []
        notLate = {} #---> {Job(): [1, 3, 5], Job(): [2, 3]}
        for job in jobsLeft: #n - lvl 2
            late = 0
            notLate[job] = []
            for id in timestamps: #4 - lvl 2
                notLate[job].append(id)
                if timestamps[id] + job.p / speeds[id] > job.d:
                    late += 1
                    notLate[job].remove(id)
            if late < 4:
                notLateJobs.append(job)
            else:
                notLate.pop(job, None)

        #jeśli wszystkie są spóźnione to wszystko jedno jak uszeregujemy:
        if len(notLateJobs) == 0:
            #print(len(jobsLeft), sigma)
            #sys.exit()
            bestMachine = max(speeds, key=speeds.get)
            for job in jobsLeft: #n = lvl 2
                sigma += job.w
            orders[bestMachine] += jobsLeft
            break

        #szukamy jaka jest najmniejsza ilość maszyn, na których praca nie jest jeszcze spóźniona
        minLength = NUMBER_OF_MACHINES
        for job in notLate: #n = lvl 2
            if len(notLate[job]) < minLength:
                minLength = len(notLate[job])

        #print(minLength)
        
        #prace, które mają minimalną ilość maszyn, na których nie są już spóźnione:
        minimallyNotLate = []
        for job in notLate: #n = lvl 2
            if len(notLate[job]) == minLength:
                minimallyNotLate.append(job)

        scores = {}
        for job in minimallyNotLate:
            scores[job] = job.w / job.d
            #scores[job] = job.w
            #scores[job] = -job.d

        bestJob = max(scores, key=scores.get)
        #print(bestJob.id, notLate[bestJob])

        machinesIds = notLate[bestJob]
        endTimes = {}
        for id in machinesIds:
            endTimes[id] = max(bestJob.r, timestamps[id]) + bestJob.p / speeds[id]
            
        #print(endTimes)

        bestMachine = min(endTimes, key=endTimes.get)

        timestamps[bestMachine] = max(timestamps[bestMachine], bestJob.r) + bestJob.p / speeds[bestMachine]
        if timestamps[bestMachine] > bestJob.d:
            sigma += bestJob.w

        orders[bestMachine].append(bestJob)

        jobsLeft.remove(bestJob)

####################################################################################################

    file.write(str(sigma))

    for id in orders:
        file.write('\n')
        for x in range(0, len(orders[id])):
            if x == len(orders[id]) - 1:
                file.write(str(orders[id][x].id))
            else:
                file.write(str(orders[id][x].id) + ' ')

    file.close()

def solve3(fileName, outFile, display = False):
    global NUMBER_OF_MACHINES
    global MY_INDEX

    instance = Instance()
    instance.read(fileName)
    if display:
        instance.print()

    file = None
    if outFile == '':
        #file = open('out_' + fileName[3:9] + '_' + str(MY_INDEX) + '_' + str(instance.n) + '.txt', 'w+')
        file = open('out_' + instance.author + '_' + str(MY_INDEX) + '_' + str(instance.n) + '.txt', 'w+')
    else:
        file = open(outFile, 'w+')

    jobsLeft = instance.jobs
    sigma = 0
    timestamps = {}
    speeds = {}
    orders = {}
    for machine in instance.machines:
        speeds[machine.id] = machine.speed
        timestamps[machine.id] = 0
        orders[machine.id] = []

### MAIN LOOP ######################################################################################
    while len(jobsLeft) > 0: #n - lvl 1
        #tworzenie listy prac, które nie są jeszcze spóźnione oraz listy jakie zadania na jakich
        #maszynach nie są jeszcze spóźnione:
        notLateJobs = []
        notLate = {} #---> {Job(): [1, 3, 5], Job(): [2, 3]}
        for job in jobsLeft: #n - lvl 2
            late = 0
            notLate[job] = []
            for id in timestamps: #4 - lvl 2
                notLate[job].append(id)
                if timestamps[id] + job.p / speeds[id] > job.d:
                    late += 1
                    notLate[job].remove(id)
            if late < 4:
                notLateJobs.append(job)
            else:
                notLate.pop(job, None)

        #jeśli wszystkie są spóźnione to wszystko jedno jak uszeregujemy:
        if len(notLateJobs) == 0:
            #print(len(jobsLeft), sigma)
            #sys.exit()
            bestMachine = max(speeds, key=speeds.get)
            for job in jobsLeft: #n = lvl 2
                sigma += job.w
            orders[bestMachine] += jobsLeft
            break

        #szukamy jaka jest najmniejsza ilość maszyn, na których praca nie jest jeszcze spóźniona
        minLength = NUMBER_OF_MACHINES
        for job in notLate: #n = lvl 2
            if len(notLate[job]) < minLength:
                minLength = len(notLate[job])
        
        #prace, które mają minimalną ilość maszyn, na których nie są już spóźnione:
        minimallyNotLate = []
        for job in notLate: #n = lvl 2
            if len(notLate[job]) == minLength:
                minimallyNotLate.append(job)

        averageTimestamp = 0
        for id in timestamps:
            timestamp = timestamps[id]
            averageTimestamp += timestamp
        averageTimestamp /= NUMBER_OF_MACHINES

        #szukamy największych wag:
        maxWeight = 0
        for job in notLate: #n = lvl 2
            if job.w > maxWeight:
                maxWeight = job.w

        threshold = 0.4
        biggestWeights = []
        for job in notLate: #n = lvl 2
            if job.w >= float(maxWeight) * threshold:
                biggestWeights.append(job)

        
        scores = {}
        for job in biggestWeights:
            if job.d - averageTimestamp != 0:
                scores[job] = job.w / (job.d - averageTimestamp)
                #scores[job] = job.w / (averageTimestamp - job.d)
            else:
                scores[job] = job.w / 0.00000000000000001
            #scores[job] = job.w
            #scores[job] = -job.

        for job in minimallyNotLate:
            #break
            if job.d - averageTimestamp != 0:
                scores[job] = job.w / (job.d - averageTimestamp)
                #scores[job] = job.w / (averageTimestamp - job.d)
            else:
                scores[job] = job.w / 0.00000000000000001
            #scores[job] = job.w
            #scores[job] = -job.d

        bestJob = max(scores, key=scores.get)
        #print(bestJob.id, notLate[bestJob])

        machinesIds = notLate[bestJob]
        endTimes = {}
        for id in machinesIds:
            endTimes[id] = max(bestJob.r, timestamps[id]) + bestJob.p / speeds[id]
            
        #print(endTimes)

        bestMachine = min(endTimes, key=endTimes.get)

        timestamps[bestMachine] = max(timestamps[bestMachine], bestJob.r) + bestJob.p / speeds[bestMachine]
        if timestamps[bestMachine] > bestJob.d:
            sigma += bestJob.w

        orders[bestMachine].append(bestJob)

        jobsLeft.remove(bestJob)

####################################################################################################

    file.write(str(sigma))

    for id in orders:
        file.write('\n')
        for x in range(0, len(orders[id])):
            if x == len(orders[id]) - 1:
                file.write(str(orders[id][x].id))
            else:
                file.write(str(orders[id][x].id) + ' ')

    file.close()
    '''

def solve4(fileName, outFile, display = False):
    global NUMBER_OF_MACHINES
    global MY_INDEX

    instance = Instance()
    instance.read(fileName)
    if display:
        instance.print()

    file = None
    if outFile == '':
        file = open('out_' + instance.author + '_' + str(MY_INDEX) + '_' + str(instance.n) + '.txt', 'w+')
    else:
        file = open(outFile, 'w+')

    jobsLeft = instance.jobs
    sigma = 0
    timestamps = {}
    speeds = {}
    orders = {}
    for machine in instance.machines:
        speeds[machine.id] = machine.speed
        timestamps[machine.id] = 0
        orders[machine.id] = []

    while len(jobsLeft) > 0: #n - lvl 1
        #tworzenie listy jakie zadania na jakich
        #maszynach nie są jeszcze spóźnione:
        notLateJobs = 0
        notLate = {}
        for job in jobsLeft: #n - lvl 2
            late = 0
            notLate[job] = []
            for id in timestamps: #4 - lvl 2
                notLate[job].append(id)
                if timestamps[id] + job.p / speeds[id] > job.d:
                    late += 1
                    notLate[job].remove(id)
            if late < 4:
                notLateJobs += 1
            else:
                notLate.pop(job, None)

        #jeśli wszystkie są już spóźnione to wszystko jedno jak uszeregujemy, wrzucamy wszystko na najszybszą maszynę:
        if notLateJobs == 0:
            bestMachine = max(speeds, key=speeds.get)
            for job in jobsLeft: #n - lvl 2
                sigma += job.w
            orders[bestMachine] += jobsLeft
            break

        #średni timestamp na wszystkich maszynach:
        averageTimestamp = 0
        for id in timestamps: #4 - lvl 2
            timestamp = timestamps[id]
            averageTimestamp += timestamp
        averageTimestamp /= NUMBER_OF_MACHINES
        
        #kryterium dla każdego zadania:
        scores = {}
        for job in notLate: #n - lvl 2
            if job.d - averageTimestamp != 0:
                scores[job] = job.w / (job.d - averageTimestamp)
            else:
                scores[job] = 99999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999

        #najwyższy score:
        bestScore = scores[max(scores, key=scores.get)]

        #prace z najwyższym score:
        bestJobs = []
        for job in notLate: #n - lvl 2
            if scores[job] == bestScore:
                bestJobs.append(job)

        #praca z najlepszym kryterium:
        bestJob = None
        if len(bestJobs) == 1:
            #bestJob = max(scores, key=scores.get)
            bestJob = bestJobs[0]
        else:
            highestW = 0
            for job in bestJobs:
                if job.w > highestW:
                    highestW = job.w
            bestJobs = [x for x in bestJobs if x.w == highestW]
        
            if len(bestJobs) == 1:
                #bestJob = max(scores, key=scores.get)
                bestJob = bestJobs[0]
            else:
                lowestD = 99999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
                for job in bestJobs:
                    if job.d < lowestD:
                        lowestD = job.d
                bestJobs = [x for x in bestJobs if x.d == lowestD]
                bestJob = bestJobs[0]

        #wybór maszyny, na której zadanie się najszybciej skończy:
        machinesIds = notLate[bestJob]
        endTimes = {}
        for id in machinesIds: #4 - lvl 2
            endTimes[id] = max(bestJob.r, timestamps[id]) + bestJob.p / speeds[id]
        bestMachine = min(endTimes, key=endTimes.get)

        #aktualizacja timestampa:
        timestamps[bestMachine] = max(timestamps[bestMachine], bestJob.r) + bestJob.p / speeds[bestMachine]
        if timestamps[bestMachine] > bestJob.d:
            sigma += bestJob.w

        #dodawania pracy na maszynę:
        orders[bestMachine].append(bestJob)

        #usuwanie pracy z pozostałych:
        jobsLeft.remove(bestJob)

    file.write(str(sigma))

    for id in orders:
        file.write('\n')
        for x in range(0, len(orders[id])):
            if x == len(orders[id]) - 1:
                file.write(str(orders[id][x].id))
            else:
                file.write(str(orders[id][x].id) + ' ')

    file.close()

def main():
    fileName = sys.argv[1]
    outFile = ''
    if len(sys.argv) == 3:
        outFile = sys.argv[2]
    solve4(fileName, outFile)
    
if __name__ == '__main__':
    main()