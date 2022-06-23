import stlpy.STL
import math
import numpy as np


class RobustnessMeasure_and():

    def Standard(self, y, t, robustness_type):
        return min([formula.robustness(y, t + self.timesteps[i], robustness_type) for i, formula in
             enumerate(self.subformula_list)])

    def AGM(self, y, t, robustness_type):
        list = ([formula.robustness(y, t + self.timesteps[i], robustness_type) for i, formula in
                 enumerate(self.subformula_list)]) #all robustness in a entirely encoded STL
        if any(list[i] <= 0 for i in range(len(list))):
            list1 = [] #list which is calculated, only choose the negative robustness
            for i in range(len(list)):
                if list[i] <= 0:
                    list1.append(list[i])
            out = (sum(list1) / len(list))
        else:
            out = list[0] + 1 #
            for i in range(1, len(list)):
                out *= (list[i] + 1)
            out = math.pow(out, 1 / len(list)) - 1
        return out

    def Smooth(self, y, t, robustness_type):
        list = ([formula.robustness(y, t + self.timesteps[i], robustness_type) for i, formula in
                 enumerate(self.subformula_list)])
        k1 = 5
        x = np.array(list)
        return -(1 / k1) * np.log(np.sum(np.exp(-k1 * (x))))

    def LSE(self, y, t, robustness_type):
        list = ([formula.robustness(y, t + self.timesteps[i], robustness_type) for i, formula in
                 enumerate(self.subformula_list)])
        k = 5
        x = np.array(list)
        return (-1 / k) * np.log(np.sum(np.exp(k * (-x))))

    def wSTL_Standard(self, y, t, robustness_type):
        list = ([formula.robustness(y, t + self.timesteps[i], robustness_type) for i, formula in
                 enumerate(self.subformula_list)])
        x = np.array(list)
        w = []
        # print("The length of subformula is " + str(len(list)) + " please input each weight of subformula.")
        # for i in range(0, len(list)):#input the weight of each subformula
        #     w_i = float(input("please input the weight of each subformula " + str(i) + ": "))
        #     w.append(w_i)
        for i in range(0, len(list)):
            w.append(1)
        for i in range(0, len(list)):  # Normaliztion of each weight
            w[i] = w[i] / sum(w)
        out=[]
        for i in range(0,len(w)):
            out.append(((0.5-w[i]) * np.sign(x[i]) + 0.5) * x[i])
        return min(out)

    def wSTL_AGM(self, y, t, robustness_type):
        list = ([formula.robustness(y, t + self.timesteps[i], robustness_type) for i, formula in
                 enumerate(self.subformula_list)])
        x = np.array(list)
        w = []
        #input weight
        # print("The length of subformula is " + str(len(list)) + " please input each weight of subformula.")
        # for i in range(0, len(list)):  # input the weight of each subformula
        #     w_i = float(input("please input the weight of each subformula " + str(i) + ": "))
        #     w.append(w_i)
        # for i in range(0, len(list)):
        #     w.append(np.random.uniform(1, 10))
        # for i in range(0, len(list)):  # Normaliztion of each weight
        #     w[i] = w[i] / sum(w)
        for i in range(0, len(list)):
            w.append(1)
        for i in range(0, len(list)):  # Normaliztion of each weight
            w[i] = w[i] / sum(w)

        if any(list[i] <= 0 for i in range(len(list))):
            out = 0
            list1 = []  # list which is calculated, only choose the negative robustness
            for i in range(len(list)):
                if list[i] <= 0:
                    list1.append(list[i])
            for i in range(0, len(list1)):
                out += list1[i] * w[i]
        else:
            out = math.pow(list[0], w[0])  #
            for i in range(1, len(list)):
                out *= math.pow(list[i], w[i])
        return out

    def NewRobustness(self, y, t, robustness_type):
        pass

    def TimeRobustness(self, y, t, robustness_type):
        pass