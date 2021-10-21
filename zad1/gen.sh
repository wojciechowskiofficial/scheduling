#!/bin/bash

args=("$@")
for ((i=50; i<=500; i+= 50)); do
	python gen_136376.py --n $i
done
