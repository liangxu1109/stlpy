import numpy as np
np.random.seed(0)
a = np.random.uniform(-0.2,0.2,(2,3))


cons={}
cons["fun"] = "a"
cons["type"] = "ineq"
print(cons)