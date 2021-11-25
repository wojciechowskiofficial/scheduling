#!/bin/bash

args=("$@")
for ((i=50; i<=500; i+= 50)); do
	python ver136376_2.py "IN/${args[0]}/in_${args[0]}_$i.txt" "${args[1]}" "alg${args[2]}.py"
done
