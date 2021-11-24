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
for i in range(2*n+1):
    input_list[i] = input_list[i].split(" ")
    if i >= 1 and i <= n:
        inprod.append(input_list[i])
    if i > n:
        inmatrix.append(input_list[i])

for i in range(len(inprod)):
    costvalue.append((int(inprod[i][0]) + int(inprod[i][2])) * int(inprod[i][1]) + (int(inprod[i][2])-int(inprod[i][0])))
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
            outprod[i] = j

currentTime = 0
maxDelay = 0
for i in range(len(inprod)):
    if i != 0:
        currentTime += int(inmatrix[outprod[i-1]][outprod[i]])
    if currentTime < int(inprod[outprod[i]][1]):
        currentTime = int(inprod[outprod[i]][1])
    currentTime += int(inprod[outprod[i]][0])
    if (currentTime - int(inprod[outprod[i]][2])) > maxDelay:
        maxDelay = currentTime - int(inprod[outprod[i]][2])

outputs = open(output, "w")
outputs.write(str(maxDelay))
outputs.write("\n")
for i in range(n):
    if i < n-1:
        outputs.write(str(outprod[i]) + " ")
    else:
        outputs.write(str(outprod[i]))
