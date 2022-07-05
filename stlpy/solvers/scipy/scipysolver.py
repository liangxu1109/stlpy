import numpy as np

from stlpy.solvers.scipy.gradient_solver import ScipyGradientSolver
from  stlpy.enumerations.option import RobustnessMetrics

def solver_list(spec, sys, x0, T, robustness_index):
    solver = []
    solver.append(ScipyGradientSolver(spec, sys, x0, T, robustness_type=RobustnessMetrics.Standard))
    solver.append(ScipyGradientSolver(spec, sys, x0, T, robustness_type=RobustnessMetrics.AGM))
    solver.append(ScipyGradientSolver(spec, sys, x0, T, robustness_type=RobustnessMetrics.LSE))
    solver.append(ScipyGradientSolver(spec, sys, x0, T, robustness_type=RobustnessMetrics.Smooth))
    solver.append(ScipyGradientSolver(spec, sys, x0, T, robustness_type=RobustnessMetrics.wSTL_Standard))
    solver.append(ScipyGradientSolver(spec, sys, x0, T, robustness_type=RobustnessMetrics.wSTL_AGM))
    solver.append(ScipyGradientSolver(spec, sys, x0, T, robustness_type=RobustnessMetrics.NewRobustness))
    solver.append(ScipyGradientSolver(spec, sys, x0, T, robustness_type=RobustnessMetrics.TimeRobustness))
    return solver[robustness_index]

def get_robustness_name(i):
    robustness_name = [
                       RobustnessMetrics.Standard,
                       RobustnessMetrics.AGM,
                       RobustnessMetrics.LSE,
                       RobustnessMetrics.Smooth,
                       RobustnessMetrics.wSTL_Standard,
                       RobustnessMetrics.wSTL_AGM,
                       RobustnessMetrics.NewRobustness,
                       RobustnessMetrics.TimeRobustness
                       ]
    return robustness_name[i]

