import sys
from itertools import filterfalse, count


def getInfoFromInputFile(inFileName):
    inFile = open(inFileName, "r")
    inFileLines = [line.rstrip() for line in inFile.readlines()]

    tasksCount = int(inFileLines[0].rstrip())

    machinesSpeed = [float(value) for value in inFileLines[1].rstrip().split(" ")]

    tasks = []
    for taskNumber in range(tasksCount):
        tasks.append([int(property) for property in inFileLines[taskNumber + 2].rstrip().split(" ")])

    return tasksCount, machinesSpeed, tasks


def getHighestPriorityTask(readyTasks, machineReadyTimer, machineSpeed):
    taskPriorities = []
    for taskNumber, task in readyTasks:
        taskDuration = task[0]
        taskDeadline = task[2]
        taskWeight = task[3]
        taskPriority = (taskDuration * 50 * taskWeight) + (machineReadyTimer - taskDeadline) + (taskWeight * 50)
        taskPriorities.append([taskNumber, taskPriority])
    return max(taskPriorities, key=lambda taskPriority: taskPriority[1])[0]


def calculateLmaxAndOrder(tasksCount, machinesSpeed, tasks):
    machinesReadyTimers = [0, 0, 0, 0]
    machinesTaskOrder = [[], [], [], []]

    notDoneTasks = [[taskNumber, task] for taskNumber, task in enumerate(tasks)]
    readyTasks = []

    Lmax = 0

    for _ in range(tasksCount):
        chosenMachineNumber, chosenMachineReadyTimer = min(enumerate(machinesReadyTimers),
                                                           key=lambda machine: machine[1])
        notRealTime = chosenMachineReadyTimer
        while True:
            readyTasks = [[taskNumber, task] for taskNumber, task in notDoneTasks if task[1] <= notRealTime]
            if len(readyTasks) == 0:
                notRealTime += 20
            else:
                break

        highestPriorityTaskNumber = getHighestPriorityTask(readyTasks, chosenMachineReadyTimer,
                                                           machinesSpeed[chosenMachineNumber])

        highestPriorityTaskDuration = tasks[highestPriorityTaskNumber][0]
        highestPriorityTaskReady = tasks[highestPriorityTaskNumber][1]
        highestPriorityTaskDeadline = tasks[highestPriorityTaskNumber][2]
        highestPriorityTaskWeight = tasks[highestPriorityTaskNumber][3]

        machinesReadyTimers[chosenMachineNumber] = max(machinesReadyTimers[chosenMachineNumber],
                                                       highestPriorityTaskReady)
        machinesReadyTimers[chosenMachineNumber] +=\
            float(highestPriorityTaskDuration) / float(machinesSpeed[chosenMachineNumber])

        if machinesReadyTimers[chosenMachineNumber] > highestPriorityTaskDeadline:
            Lmax += highestPriorityTaskWeight

        machinesTaskOrder[chosenMachineNumber].append(highestPriorityTaskNumber)
        notDoneTasks = list(filterfalse(lambda i, counter=count(): i[0] == highestPriorityTaskNumber and
                                                                   next(counter) < 1, notDoneTasks))

    return Lmax, machinesTaskOrder


def listToString(s):
    str1 = ""
    for ele in s:
        str1 += str(ele) + " "
    return str1.rstrip() + "\n"


def getOutFileName(inFileName):
    inFileNameSeparated = inFileName.split("_")
    index = inFileNameSeparated[1]
    n = inFileNameSeparated[2]
    return "out_" + str(index) + "_" + str(n)


def generateOutFile(outFileName, Lmax, machinesTaskOrder):
    outFile = open(outFileName, "w+")
    outFile.write(str(Lmax))
    outFile.write("\n")

    for machineTaskOrder in machinesTaskOrder:
        outFile.write(listToString(machineTaskOrder))

    outFile.close()


if __name__ == '__main__':
    inFileName = sys.argv[1]
    outFileName = sys.argv[2]
    tasksCount, machinesSpeed, tasks = getInfoFromInputFile(inFileName)
    Lmax, machinesTaskOrder = calculateLmaxAndOrder(tasksCount, machinesSpeed, tasks)
    generateOutFile(outFileName, Lmax, machinesTaskOrder)
