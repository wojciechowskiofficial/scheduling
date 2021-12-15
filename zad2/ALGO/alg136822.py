import sys
import numpy as np


inprod = []
inmatrix = []

costvalue = []
outprod = []

if __name__ == '__main__':
    input = sys.argv[1]
    output = sys.argv[2]

inputs = open(input, "r")
content = inputs.read()
input_list = content.splitlines()
n = int(input_list[0])
for i in range(n+2):
    input_list[i] = input_list[i].split(" ")
    if i > 1:
        inprod.append(input_list[i])

machines = input_list[1]

for i in range(len(inprod)):
    costvalue.append(int(inprod[i][3]) * int(inprod[i][2]) * int(inprod[i][1]) + int(inprod[i][0]) )
    outprod.append(i)

costarray = np.array(costvalue)
costvalue = np.array(costvalue)
outprod = np.array(outprod)

for i in range(len(inprod)):
    min = costarray[i]
    pos = i
    for j in range(len(inprod)-i):
        if costarray[j+i] < min:
            min = costarray[j+i]
            pos = j+i
    tempval = costarray[i]
    costarray[i] = min
    costarray[pos] = tempval

for i in range(len(inprod)):
    for j in range(len(inprod)):
        if costarray[i] == costvalue[j]:
            temp = outprod[i]
            outprod[i] = j
            outprod[j] = i

machineTime = [0,0,0,0]
machineProcs = [[], [], [], []]
sumWage = 0
for i in range(len(inprod)):
    counter = 0
    min = machineTime[0]
    pos = 0
    for j in range(len(machines)):
        if machineTime[j] < min:
            min = machineTime[j]
            pos = j
        if machineTime[j] + (int(inprod[int(outprod[i])][0]) / int(machines[j])) <= int(inprod[int(outprod[i])][2]):
            if machineTime[j] < int(inprod[int(outprod[i])][1]):
                machineTime[j] = int(inprod[int(outprod[i])][1])
            machineProcs[j].append(outprod[i])
            machineTime[j] += (int(inprod[int(outprod[i])][0]) / int(machines[j]))
            break
        else:
            counter += 1
    if counter == 4:
        machineTime[pos] += (int(inprod[int(outprod[i])][0]) / int(machines[pos]))
        machineProcs[pos].append(outprod[i])
        sumWage = sumWage + int(inprod[int(outprod[i])][3])
outputs = open(output, "w")
outputs.write(str(sumWage))
outputs.write("\n")
for i in range(4):
    for j in range(len(machineProcs[i])):
        if j < len(machineProcs[i]) - 1:
            outputs.write(str(machineProcs[i][j]) + " ")
        else:
            outputs.write(str(machineProcs[i][j]))
    outputs.write("\n")



