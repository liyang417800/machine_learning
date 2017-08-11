from numpy import *

a=mat('1 2 3; 4 5 3')

print a
print a.T
print a.I

print a*a.I
# print (a*a.T).I