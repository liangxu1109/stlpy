import numpy as np
import math

# def AGM(list):
#     if any(list[i] <= 0 for i in range(len(list))):
#         list1 = []  # list which is calculated, only choose the negative robustness
#         for i in range(len(list)):
#             if list[i] <= 0:
#                 list1.append(list[i])
#         out = (sum(list1) / len(list))
#     else:
#         out = list[0] + 1  #
#         for i in range(1, len(list)):
#             out *= (list[i] + 1)
#         out = math.pow(out, 1 / len(list)) - 1
#     return out
#
# list1 = [-1,2,3,4,5,6,7,8,9]
# list2 = [1,2,3,4,5,6,7,8,9]
# robustness1 = AGM(list1)
# robustness2 = AGM(list2)

# print(robustness1)
# print(robustness2)


# A=[1,2,3,4,-5,6,7,8,9,10]
# w = []
# print("The length of subformula is " + str(len(A)) + " please input each weight of subformula.")
# for i in range(0, len(A)):
#     w_i = float(input("please input the weight of subformula "+ str(i) + ": "))
#     w.append(w_i)
# for i in range(0, len(A)):
#     w[i] = w[i]/sum(w)
# out = []
# for i in range(0, len(w)):
#     out.append(((0.5 - w[i]) * np.sign(A[i]) + 0.5) * A[i])
# print(min(out))

# list=[1,2,3,4,-5,6,7,8,9,10]
# w = []
# print("The length of subformula is " + str(len(list)) + " please input each weight of subformula.")
# for i in range(0, len(list)):
#     w_i = float(input("please input the weight of subformula "+ str(i) + ": "))
#     w.append(w_i)
# for i in range(0, len(list)):
#     w.append(np.random.uniform(1, 10))
#
# for i in range(0, len(list)):
#     w[i] = w[i]/sum(w)
#
# print(w)
# if any(list[i] <= 0 for i in range(len(list))):
#     out = 0
#     list1 = []  # list which is calculated, only choose the negative robustness
#     for i in range(len(list)):
#         if list[i] <= 0:
#             list1.append(list[i])
#     for i in range(0, len(list1)):
#         out += list1[i] * w[i]
# else:
#     out = math.pow(list[0], w[0])  #
#     for i in range(1, len(list)):
#         out *= math.pow(list[i], w[i])
# print(out)


# solver = []
# solver.append("asd")
# print(solver)

list=[1,2,3,4,-5,6,7,8,9,10]
print(min(list))
