import sys
import time
from itertools import filterfalse, count


def getInfoFromInputFile(inFileName):
    inFile = open(inFileName, "r")
    inFileLines = [line.rstrip() for line in inFile.readlines()]

    tasksCount = int(inFileLines[0])

    tasks = []
    for taskNumber in range(tasksCount):
        tasks.append([int(property) for property in inFileLines[taskNumber + 1].split(" ")])

    preparationBetweenTasks = []
    for i in range(tasksCount):
        preparationBetweenTasks.append([int(value) for value in inFileLines[tasksCount + 1 + i].split(" ")])

    return tasksCount, tasks, preparationBetweenTasks


def getHighestPriorityTask(readyTasks, time):
    taskPriorities = []
    for taskNumber, task in readyTasks:
        taskDuration = task[0]
        taskDeadline = task[2]
        taskPriority = (taskDuration * 50) + (time - taskDeadline)
        taskPriorities.append([taskNumber, taskPriority])
    return max(taskPriorities, key=lambda taskPriority: taskPriority[1])[0]


def getReadyTasks(notDoneTasks, tasksOrder, preparationBetweenTasks, time):
    readyTasks = []
    for taskNumber, task in notDoneTasks:
        taskPreparation = 0
        if len(tasksOrder) > 0:
            lastTaskNumber = tasksOrder[-1]
            taskPreparation = preparationBetweenTasks[lastTaskNumber][taskNumber]
        willTaskBeReady = task[1] <= time + taskPreparation
        if willTaskBeReady:
            readyTasks.append([taskNumber, task])
    return readyTasks


def getTaskPreparation(tasksOrder, taskNumber):
    taskPreparation = 0
    if len(tasksOrder) > 0:
        lastTaskNumber = tasksOrder[-1]
        taskPreparation = preparationBetweenTasks[lastTaskNumber][taskNumber]
    return taskPreparation


def calculateLmaxAndOrder(tasksCount, tasks, preparationBetweenTasks):
    notDoneTasks = [[taskNumber, task] for taskNumber, task in enumerate(tasks)]
    time = 0
    tasksOrder = []
    Lmax = -99999
    readyTasks = []

    for _ in range(tasksCount):
        notRealTime = time
        while True:
            readyTasks = getReadyTasks(notDoneTasks, tasksOrder, preparationBetweenTasks, notRealTime)
            if len(readyTasks) == 0:
                notRealTime += 20
            else:
                break

        highestPriorityTaskNumber = getHighestPriorityTask(readyTasks, time)
        highestPriorityTaskPreparation = getTaskPreparation(tasksOrder, highestPriorityTaskNumber)

        highestPriorityTaskDuration = tasks[highestPriorityTaskNumber][0]
        highestPriorityTaskReady = tasks[highestPriorityTaskNumber][1]
        highestPriorityTaskDeadline = tasks[highestPriorityTaskNumber][2]

        time += highestPriorityTaskPreparation
        time = max(time, highestPriorityTaskReady)
        time += highestPriorityTaskDuration
        Lmax = max(Lmax, time - highestPriorityTaskDeadline)

        tasksOrder.append(highestPriorityTaskNumber)
        notDoneTasks = list(filterfalse(lambda i, counter=count(): i[0] == highestPriorityTaskNumber and next(counter) < 1, notDoneTasks))

    return Lmax, tasksOrder


def getOutFileName(inFileName):
    inFileNameSeparated = inFileName.split("_")
    index = inFileNameSeparated[1]
    n = inFileNameSeparated[2]
    return "out_" + str(index) + "_" + str(n)


def generateOutFile(outFileName, Lmax, tasksOrder):
    outFile = open(outFileName, "w+")
    outFile.write(str(Lmax))
    outFile.write("\n")

    for taskNumber in range(len(tasksOrder) - 1):
        outFile.write(str(tasksOrder[taskNumber]) + " ")
    outFile.write(str(tasksOrder[len(tasksOrder) - 1]))

    outFile.close()


if __name__ == '__main__':
    inFileName = sys.argv[1]
    outFileName = sys.argv[2]
    tasksCount, tasks, preparationBetweenTasks = getInfoFromInputFile(inFileName)
    start = time.perf_counter()
    Lmax, tasksOrder = calculateLmaxAndOrder(tasksCount, tasks, preparationBetweenTasks)
    end = time.perf_counter()
    generateOutFile(outFileName, Lmax, tasksOrder)
