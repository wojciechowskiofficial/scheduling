#!/bin/bash

args=("$@")
for ((i=50; i<=500; i+= 50)); do
	python ver_136376.py --in_name "${args[0]}/in_${args[0]}_$i.txt" --out_name "out_136376_$i.txt"
done
