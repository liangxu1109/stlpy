import math
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
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

list=[1,-2,3,4,5,6,7,8,9,10]
# # if any(list[i] <= 0 for i in range(len(list))):
# #     print(min(list))
# v = 3  # parameter v > 0 is then defined by taking the weighted average of these effective measures
# rho_tilde = [] #Using this normalized measure, it can be transformed to be non-positive and becomes 0 at rho_i = rho_min
# rho_eff = []
# numerator = 0
# denominator = 0
# rho_min = min(list)
# for i in range(0, len(list)):
#     if rho_min != 0:
#         tilde_i = (list[i] - rho_min) / rho_min
#         rho_tilde.append(tilde_i)
#         rho_eff.append(rho_min * np.exp(rho_tilde[i]))
# if min(list) < 0:
#     for i in range(0, len(list)):
#         numerator += (rho_eff[i] * np.exp(v * rho_tilde[i]))
#         denominator += np.exp(v * rho_tilde[i])
#     out = numerator / denominator
# elif min(list) > 0:
#     for i in range(0, len(list)):
#         numerator += (list[i] * np.exp(-v * rho_tilde[i]))
#         denominator += np.exp(-v * rho_tilde[i])
#     out = numerator / denominator
# else:
#     out = 0
# print(out)
# print(rho_min)
# for i in list:
#     print(i)
# w = []
# for i in range(0, len(list)):
#     w.append(1.5)
# print(w)
# sum = sum(w)
# for i in range(0, len(list)):  # Normaliztion of each weight
#     w[i] = w[i] / sum
# print(w)
# x_min = np.array([0.0, 0.0, -1.0, -1.0])
# x_max = np.array([10.0, 10.0, 1.0, 1.0])
# bounds = np.asarray([[x_min[0], x_max[0]],
#                     [x_min[1], x_max[1]],
#                     [x_min[2], x_max[2]],
#                     [x_min[3], x_max[3]]])
# print(np.sign(list))
# 自定义函数
def func(x, a, b, c):
    return a * np.exp(-b * x) + c

# 构造数据
xdata = np.linspace(0, 4, 50)
y = func(xdata, 2.5, 1.3, 0.5)
print(y)
rng = np.random.default_rng()
y_noise = 0.2 * rng.normal(size=xdata.size)
ydata = y + y_noise
print(ydata)
# 拟合
popt, pcov = curve_fit(func, xdata, ydata)

## 设置参数取值范围
popt1, pcov1 = curve_fit(func, xdata, ydata, bounds=(0, [3., 1., 0.5]))

# 可视化
plt.plot(xdata, ydata, 'b-', label='data')
plt.plot(xdata, func(xdata, *popt), 'r-',
         label='fit: a=%5.3f, b=%5.3f, c=%5.3f' % tuple(popt))
plt.plot(xdata, func(xdata, *popt1), 'g--',
         label='fit: a=%5.3f, b=%5.3f, c=%5.3f' % tuple(popt1))

plt.legend()
plt.show()