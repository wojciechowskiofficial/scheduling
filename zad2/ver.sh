#!/bin/bash

args=("$@")
for ((i=50; i<=500; i+= 50)); do
	python ver136376_2.py "136376/in_136376_$i.txt" "cos.txt" "algorytmy/alg${args[0]}.py"
done
