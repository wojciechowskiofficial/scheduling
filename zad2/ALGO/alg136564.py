#!/usr/bin/python
import sys

PUT_INDEX = 136564


class Job:
    def __init__(self, p, r, d, w, id):
        self.p = p
        self.r = r
        self.d = d
        self.w = w
        self.u = -1
        self.c = -1
        self.id = id
        self.assigned = False

    def __repr__(self) -> str:
        return "(p: {0}, r: {1}, d: {2}, w: {3}, u: {4})".format(self.p, self.r, self.d, self.w, self.u)

    def calcC(self, prevC, machine):
        t = 0
        if prevC is not None:
            t = prevC
        if self.r > t:
            t += self.r - t
        t += self.p / machine.b
        return t

    def setC(self, prevC, machine):
        self.c = self.calcC(prevC, machine)
        return self.c

    def calcU(self):
        if self.c == -1:
            print("ERROR in job.setU - c was not set before")
            return
        if self.c > self.d:
            return 1
        else:
            return 0

    def calcCriterion(self, calculatedTime):
        if calculatedTime > self.d:
            return 1 * self.w
        else:
            return 0

    def setU(self):
        self.u = self.calcU()

    def getCriterion(self):
        return self.u * self.w


class Machine:
    def __init__(self, b):
        self.b = b
        self.jobs = []
        self.time = 0
        self.criterion = 0

    def __repr__(self) -> str:
        return "(b: {0}\njobs: {1})\n".format(self.b, self.jobs)

    def calculateTime(self, job):
        return job.calcC(self.time, self)

    def calculateTimeWith2Jobs(self, job1, job2):
        x = job1.calcC(self.time, self)
        return job2.calcC(x, self)

    def updateTime(self, job):
        self.time = job.setC(self.time, self)

    def calculateJobsCompletedTimeAndUParam(self):
        prevC = None
        for job in self.jobs:
            job.setC(prevC, self)
            job.setU()
            prevC = job.c

    def calculateMachineCriterion(self):
        tmp = 0
        for job in self.jobs:
            tmp += job.getCriterion()
        return tmp


def strArrayToInt(array):
    for i in range(len(array)):
        array[i] = int(array[i])
    return array


def strArrayToFloat(array):
    for i in range(len(array)):
        array[i] = float(array[i])
    return array


def getMachinesAndJobsFromInputFile(path):
    file = open(path)
    n = int(file.readline())
    jobs = []
    machines = []
    bArray = strArrayToFloat(file.readline().split())
    for i in range(4):
        machines.append(Machine(bArray[i]))

    for i in range(n):
        jobParams = strArrayToInt(file.readline().split())
        jobs.append(Job(jobParams[0], jobParams[1], jobParams[2], jobParams[3], i))

    file.close()
    return [jobs, machines]


def saveOutputFile(fname, Lmax, ordered):
    # fname = "out_" + str(index )+ "_" + str(len(ordered)) + ".txt"
    f = open(fname, "w")
    # print("Lmax: " + str(Lmax)) XD
    f.write("0\n")
    for job in ordered:
        f.write(str(job["id"]) + " ")
    f.close()
    return fname


def alg(jobs, machines):
    criterionSum = 0
    for i in jobs:
        minDjob = None
        selectedJob = None
        minCjob = None
        jobsAssigned = 0
        for j in jobs:
            if j.assigned:
                jobsAssigned += 1
                continue
            minDjob = calcMinD(j, minDjob)
            minCjob = calcMinC(machines, j, minCjob)

        minC = None
        maxC = None
        minMachine = None
        finalMachine = None
        fee = True

        #print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        if len(jobs) == jobsAssigned:
            break
        assignCjob = None
        for m in machines:
            minCjobBeforeMinDjobCalculatedTime = m.calculateTimeWith2Jobs(minCjob, minDjob)
            minCjobBeforeMinDjobCriterion = minDjob.calcCriterion(minCjobBeforeMinDjobCalculatedTime)

            minDjobBeforeMinCjobCalculateTime = m.calculateTime(minDjob)
            minDjobBeforeMinCjobCriterion = minCjob.calcCriterion(minDjobBeforeMinCjobCalculateTime)

            # print(minCjobBeforeMinDjobCalculatedTime, minDjobBeforeMinCjobCalculateTime)
            # print(minCjobBeforeMinDjobCriterion, minDjobBeforeMinCjobCriterion)

            tmp = None
            if minCjobBeforeMinDjobCalculatedTime <= minDjobBeforeMinCjobCalculateTime:
                # if minCjobBeforeMinDjobCalculatedTime <= minDjobBeforeMinCjobCalculateTime or minCjobBeforeMinDjobCalculatedTime - minDjobBeforeMinCjobCalculateTime < minCjob.p / 2 :
                tmp = m.calculateTime(minCjob)
                assignCjob = True
                finalJob = minCjob
            else:
                tmp = minDjobBeforeMinCjobCalculateTime
                assignCjob = False
                finalJob = minDjob

            # assignCjob = False
            # tmp = minDjobBeforeMinCjobCalculateTime#m.calculateTime(minCjob)

            if minC is None:
                minC = tmp
                finalMachine = m
            if minC >= tmp:
                minC = tmp
                finalMachine = m


        if assignCjob:
            finalMachine.updateTime(minCjob)
            finalMachine.jobs.append(minCjob)
            minCjob.setU()
            criterionSum += minCjob.getCriterion()
            minCjob.assigned = True
            # print("minCjob assigned, machineTime", minMachine.time)
        else:
            finalMachine.updateTime(minDjob)
            finalMachine.jobs.append(minDjob)
            minDjob.setU()
            criterionSum += minDjob.getCriterion()
            minDjob.assigned = True
    return criterionSum


def calcMinC(machines, job, minCjob):
    if minCjob is None:
        return job
    jobC = machines[0].calculateTime(job)
    minCjobC = machines[0].calculateTime(minCjob)
    if minCjobC > jobC:
        return job
    else:
        return minCjob


def calcSelectedJob(job, selectedJob):
    if selectedJob is None:
        return job
    jobX = job.d * job.w
    selectedJobX = selectedJob.d * selectedJob.w
    if selectedJobX > jobX:
        return job
    else:
        return selectedJob


def calcMinD(job, minDjob):
    if minDjob is None:
        return job
    if minDjob.d > job.d:
        return job
    else:
        return minDjob


def generateOutput(machines, criterionSum, n, outputFile):
    f = open(outputFile, "w")
    f.write(str(criterionSum) + "\n")
    for m in machines:
        for job in m.jobs:
            f.write(str(job.id) + " ")
        f.write("\n")
    f.close()


if len(sys.argv) > 2 and "in" in sys.argv[1]:
    inputFile = sys.argv[1]
    outputFile = sys.argv[2]
    jobs, machines = getMachinesAndJobsFromInputFile(inputFile)
    criterionSum = alg(jobs, machines)
    generateOutput(machines, criterionSum, len(jobs), outputFile)

if len(sys.argv) in (1, 2):
    print("NO args detected!")
