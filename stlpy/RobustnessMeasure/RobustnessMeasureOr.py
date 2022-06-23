import stlpy.STL
import math
import numpy as np


class RobustnessMeasure_or():

    def Standard(self, y, t, robustness_type):
        return max([formula.robustness(y, t + self.timesteps[i], robustness_type) for i, formula in
             enumerate(self.subformula_list)])

    def AGM(self, y, t, robustness_type):
        list = ([formula.robustness(y, t + self.timesteps[i], robustness_type) for i, formula in
                 enumerate(self.subformula_list)])
        if any(list[i] > 0 for i in range(len(list))):
            list1 = []
            for i in range(len(list)):
                if list[i] > 0:
                    list1.append(list[i])
            out = (sum(list1) / len(list))
        else:
            out = 1 - list[0]
            for i in range(1, len(list)):
                out *= (1 - list[i])
            out = - math.pow(out, 1 / len(list)) + 1
        return out

    def Smooth(self, y, t, robustness_type):
        list = ([formula.robustness(y, t + self.timesteps[i], robustness_type) for i, formula in
                 enumerate(self.subformula_list)])
        k2 = 5
        x = np.array(list)
        return (np.sum(x * np.exp(k2 * (x))) / (np.sum(np.exp(k2 * (x)))))

    def LSE(self, y, t, robustness_type):
        list = ([formula.robustness(y, t + self.timesteps[i], robustness_type) for i, formula in
                 enumerate(self.subformula_list)])
        k = 5
        x = np.array(list)
        return (1 / k) * np.log(np.sum(np.exp(k * (x))))

    def wSTL_Standard(self, y, t, robustness_type):
        return max([formula.robustness(y, t + self.timesteps[i], robustness_type) for i, formula in
                    enumerate(self.subformula_list)])

    def wSTL_AGM(self, y, t, robustness_type):
        list = ([formula.robustness(y, t + self.timesteps[i], robustness_type) for i, formula in
                 enumerate(self.subformula_list)])
        if any(list[i] > 0 for i in range(len(list))):
            list1 = []
            for i in range(len(list)):
                if list[i] > 0:
                    list1.append(list[i])
            out = (sum(list1) / len(list))
        else:
            out = 1 - list[0]
            for i in range(1, len(list)):
                out *= (1 - list[i])
            out = - math.pow(out, 1 / len(list)) + 1
        return out

    def NewRobustness(self, y, t, robustness_type):
        pass