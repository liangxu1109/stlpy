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

u_guess = [[ 2.12112872e-01,  1.06326027e-01,  1.05873103e-01,  2.05975496e-01,
   4.71322779e-01,  1.55574136e-01,  1.29734084e-04, -1.55427115e-01,
  -6.61034920e-01, -2.20288101e-01, -6.17642215e-04],
 [ 6.63809321e-01,  2.50366342e-01,  8.75858912e-02,  1.19514541e-02,
  -5.16469205e-02, -2.16979219e-01, -1.21668531e-01, -1.36508087e-01,
  -2.92021319e-01, -9.72615658e-02, -6.17769419e-04]]
print(u_guess)