#!/bin/bash

args=("$@")
for ((i=50; i<=500; i+= 50)); do
	python ver136376_2.py "instances/${args[0]}/in_${args[0]}_$i.txt" "cos.txt" alg136376.py
done
