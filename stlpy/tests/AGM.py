import numpy as np
import math

def AGM(list):
    if any(list[i] <= 0 for i in range(len(list))):
        list1 = []  # list which is calculated, only choose the negative robustness
        for i in range(len(list)):
            if list[i] <= 0:
                list1.append(list[i])
        out = (sum(list1) / len(list))
    else:
        out = list[0] + 1  #
        for i in range(1, len(list)):
            out *= (list[i] + 1)
        out = math.pow(out, 1 / len(list)) - 1
    return out

list1 = [-1,2,3,4,5,6,7,8,9]
list2 = [1,2,3,4,5,6,7,8,9]
robustness1 = AGM(list1)
robustness2 = AGM(list2)

print(robustness1)
print(robustness2)