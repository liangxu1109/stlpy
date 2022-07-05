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
        x = np.array(list)
        w = []
        for i in range(0, len(list)):
            w.append(1)
        for i in range(0, len(list)):  # Normaliztion of each weight
            w[i] = w[i] / sum(w)

        if any(list[i] > 0 for i in range(len(list))):
            out = 0
            list1 = []  # list which is calculated, only choose the positive robustness
            for i in range(len(list)):
                if list[i] > 0:
                    list1.append(list[i])
            for i in range(0, len(list1)):
                out += list1[i] * w[i]
        else:
            out = - math.pow(1 - list[0], w[0])  #initial number
            for i in range(1, len(list)):
                out *= math.pow(1 - list[i], w[i])
            out = out + 1
        return out

    def NewRobustness(self, y, t, robustness_type):
        list = ([formula.robustness(y, t + self.timesteps[i], robustness_type) for i, formula in
                 enumerate(self.subformula_list)])  # all robustness in a entirely encoded STL
        v = 3  # parameter v > 0 is then defined by taking the weighted average of these effective measures
        rho_tilde = []  # Using this normalized measure, it can be transformed to be non-positive and becomes 0 at rho_i = rho_max
        rho_eff = []
        numerator = 0
        denominator = 0
        rho_max = max(list)
        if rho_max < 0:
            for j in range(0, len(list)):
                tilde_j = (rho_max - list[j]) / rho_max
                rho_tilde.append(tilde_j)
                rho_eff.append(rho_max * np.exp(rho_tilde[j]))
            for j in range(0, len(list)):
                numerator += (rho_eff[j] * np.exp(v * rho_tilde[j]))
                denominator += np.exp(v * rho_tilde[j])
            out = numerator / denominator
        elif rho_max > 0:
            for j in range(0, len(list)):
                tilde_j = (rho_max - list[j]) / rho_max
                rho_tilde.append(tilde_j)
                rho_eff.append(rho_max * np.exp(rho_tilde[j]))
            for j in range(0, len(list)):
                numerator += (list[j] * np.exp(-v * rho_tilde[j]))
                denominator += np.exp(-v * rho_tilde[j])
            out = numerator / denominator
        else:
            out = 0
        return out

    def TimeRobustness(self, y, t, robustness_type):
        # TODO:
        pass