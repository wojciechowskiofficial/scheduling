#!/usr/bin/python
import sys

PUT_INDEX = 136564

def strArrayToInt(array):
    for i in range(len(array)):
        array[i] = int(array[i])
    return array

def getJobsParamsFromInputFile(path):
    file = open(path)
    n = int(file.readline())
    jobs = []
    for i in range(n):
        jobParams = strArrayToInt(file.readline().split())
        jobs.append(jobParams)
        
    setUps = []
    for i in range(n):
        setUpTimes = strArrayToInt(file.readline().split())
        setUps.append(setUpTimes)
        
    file.close()
    return [jobs, setUps]

def getFineJobs(jobs, setUps):
    fineJobs = []
    for i in range(len(jobs)):
        fineJob = {
            "id": i,
            "pi": jobs[i][0],
            "ri": jobs[i][1],
            "di": jobs[i][2],
            "sij": setUps[i]
        }
        fineJobs.append(fineJob)
    return fineJobs
 
def alg5(fineJobs):
    Lmax = -99999999
    t = 0
    previousJob = None
    for i in range(len(fineJobs)):
        jobToSwapId = -1
        jobToSwap = None
        diMin = None
        tmin = None
        Lmin = None
        fastestJobToDo = None
        fastestJobToDoId = -1
        tFastestJobToDo = None
        LFastestJob = None
        for j in range(i, len(fineJobs)):
            job = fineJobs[j]
            t1, L1 = calculateTiming(t, previousJob, job)
            if jobToSwap == None:
                jobToSwap = job
                jobToSwapId = j
                tmin = t1
                Lmin = L1
                diMin = job["di"]
                fastestJobToDo = job
                tFastestJobToDo = t1
                fastestJobToDoId = j
                LFastestJob = L1
            if job["di"] < diMin: 
                tmin = t1
                jobToSwapId = j
                jobToSwap = job
                Lmin = L1
                diMin = job["di"]
            if tFastestJobToDo > t1:
                tFastestJobToDo = t1
                fastestJobToDo = job
                LFastestJob = L1
                fastestJobToDoId = j
        
        tFastestBeforeSelected, LFastestBeforeSelected = calculateTiming(tFastestJobToDo, fastestJobToDo, jobToSwap)
        
        if LFastestBeforeSelected <= Lmin:
            jobToSwap = fastestJobToDo
            jobToSwapId = fastestJobToDoId
            tmin = tFastestJobToDo
            Lmin = LFastestJob
        
        t = tmin
        tmp = fineJobs[i]
        fineJobs[i] = fineJobs[jobToSwapId]
        fineJobs[jobToSwapId] = tmp
        Lmax = getLmax(Lmax, Lmin)
        previousJob = fineJobs[i]
    return Lmax


def calculateTiming(t, previousJob, job):
    Li = 0
    if previousJob == None or t == 0:
        t += job["ri"] + job["pi"]
        Li = t - job["di"]
    else:
        sij = previousJob["sij"][job["id"]]
        t += sij
        delta = job["ri"] - t
        if delta > 0:
            t += delta
        t += job["pi"]
        Li = t - job["di"]
    return [t, Li]
        
def getLmax(L1, L2):
    if L1 > L2:
        return L1
    else:
        return L2
    

def printJobsId(title, jobs):
    string = title + " = "
    for i in jobs:
        string = string + str(i["id"]) + " "
    print(string)

def saveOutputFile(fname, Lmax, ordered):
    #fname = "out_" + str(index )+ "_" + str(len(ordered)) + ".txt" 
    f = open(fname, "w")
    #print("Lmax: " + str(Lmax)) XD
    f.write(str(Lmax) + "\n")
    for job in ordered:
        f.write(str(job["id"]) + " ")
    f.close()
    return fname
        
    
if len(sys.argv) > 2 and "in" in sys.argv[1]:
    jobs, setUps = getJobsParamsFromInputFile(sys.argv[1])
    fineJobs = getFineJobs(jobs, setUps)
    Lmax = alg5(fineJobs)
    if Lmax == None:
        Lmax = -1
    #print("Algorithm finished")
    fileName = saveOutputFile(sys.argv[2], Lmax, fineJobs)
    #print("File " + fileName + " saved.") XD
    
    

if len(sys.argv) in (1, 2):
    print("NO args detected!")    
