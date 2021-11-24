#!/bin/bash

args=("$@")
for ((i=50; i<=500; i+= 50)); do
	python ver136376.py "IN/${args[0]}/in_${args[0]}_$i.txt" "OUT/out_$i.txt"
done
