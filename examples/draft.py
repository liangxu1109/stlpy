import numpy as np
np.random.seed(0)
a = np.random.uniform(-0.2,0.2,(2,3))
import math


cons={}
cons["fun"] = "a"
cons["type"] = "ineq"
print(cons)
def a():
    return lambda k, m: 0
print(a)

x=[0.9,0.8,0.7]
a = np.array(x)
k1 =10
def s():
    return -(1/k1)*np.log(np.sum(np.exp(-k1*(a))))
#print(s())

def r(list):
    if any(list[i] <= 0 for i in range(len(list))):
        list1 = []
        for i in range(len(list)):
            if list[i] <= 0:
                list1.append(list[i])
        out = (sum(list1) / len(list))
    else:
        out = list[0] + 1
        for i in range(1, len(list)):
            out *= (list[i] + 1)
        out = math.pow(out, 1 / len(list)) - 1
    return out

list = [1,2,3,4,5,6]
rho = r(list)
print(rho)