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

    def wSTL(self, y, t, robustness_type):
        pass

    def NewRobustness(self, y, t, robustness_type):
        pass