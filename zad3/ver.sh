#!/bin/bash

args=("$@")
for ((i=50; i<=500; i+= 50)); do
	python ver136376.py "${args[0]}/in_${args[0]}_$i.txt" "OUT/out_136376_$i.txt"
done
