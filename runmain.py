

import os
import itertools

allfeats=['goodsmiley', 'badsmiley' , 'upper', 'question_marks', 'exclamation_marks', 'raw_vulgarity', 'vulgarity', 'you','disagreement', 'unpoliteness', 'sentiment']
i=0
# for L in range(0, len(allfeats)+1):
#     for subset in itertools.combinations(allfeats, L):
#         i+=1
#         print(subset)

c0="python shuffleSelect.py 80 80"
c="python main.py 10 -o "

out=open('main.sh', 'w')

out.write("#!/bin/bash")
out.write('\n')

out.write('c=1')
out.write('\n')
out.write('while [ $c -le 10 ]')
out.write('\n')
out.write('do')
out.write('\n')
out.write('\tpython shuffleSelect.py 80 80\n')
for feat in allfeats:
    out.write('\t%s -feat %s\n'%(c,feat))    
#out.write('\tpython main.py 10 -all -o\n')  
out.write('\t(( c++ ))\n')    
out.write('done\n')     
out.write('python scorer.py\n')    
    



