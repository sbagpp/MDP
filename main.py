from MDP import *

f = open("result.txt", "w")
s = ""
for i in range(1, 50):
    name = "SOM-a/SOM-a/SOM-A"+str(i)+".txt"
    s += risolutore(name)

f.write(s)
f.close()