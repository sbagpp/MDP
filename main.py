from MDP import *

f = open("result.txt", "w")
''''
for i in range(50):
    name = "SOM-a/SOM-a/SOM-A"+str(i)+".txt"
    s = risolutore(name)
    f.write(s)
'''
name = "SOM-a/SOM-a/SOM-A2.txt"
s = risolutore(name)
f.write(s)
f.close