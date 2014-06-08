#!/bin/bash
c=1
while [ $c -le 10 ]
do
	python shuffleSelect.py 200 70
	python main.py 10 -o   -baseline2 +feat you vulgarity raw_vulgarity sentiment
	(( c++ ))
done
python scorer.py
rm ./archieves/results.txt
