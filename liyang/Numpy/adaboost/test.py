from numpy import *

a=mat('1 2 3; 4 5 3')

print a
print a.T
print a.I

print a*a.I
# print (a*a.T).I

#!/usr/bin/python
# #_*_ coding: utf-8 _*_

import sys
import datetime
# "规格:RN1-10/50;规格:RN1-10/50;规格:RN1-10/50"
# ["规格:RN1-10/51;规格:RN1-10/52;规格:RN1-10/53", '11', '22']
# ["规格", "RN1-10/51", '11', '22']
# ["规格", "RN1-10/52", '11', '22']
# ["规格", "RN1-10/53", '11', '22']

for line in sys.stdin:
        values = line.split('\t')
        values = [ i.strip() for i in values ]
        tmp = values[0]
        key_values = tmp.split(";")
        for kv in key_values:
                k = kv.split(":")[0]
                v = kv.split(":")[1]
                print '\t'.join([k,v,values[1],values[2]])