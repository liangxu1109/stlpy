#!/usr/bin/env python

##
#
# Set up, solve, and plot the solution for a simple
# reach-avoid problem, where the robot must avoid
# a rectangular obstacle before reaching a rectangular
# goal.
#
##

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from stlpy.enumerations.option import RobustnessMetrics

from stlpy.benchmarks import ReachAvoid
from stlpy.solvers import *
from stlpy.enumerations.option import RobustnessMetrics
from stlpy.solvers.scipy.scipysolver import solver_list, get_robustness_name

# Specification Parameters
goal_bounds = (7,8,8,9)     # (xmin, xmax, ymin, ymax)
obstacle_bounds = (2.8,4.8,3.2,5.2)
T = 24
# T = 20
# T = 30

# Define the system and specification
scenario = ReachAvoid(goal_bounds, obstacle_bounds, T)
#scenario = ReachAvoid(goal_bounds, obstacle_bounds, T, robustness_type= RobustnessMetrics.AGM)
spec = scenario.GetSpecification()
spec.flatten(spec)
spec.flatten(spec)
sys = scenario.GetSystem()

# Specify any additional running cost (this helps the numerics in
# a gradient-based method)
Q = 1e-3*np.diag([0,0,1,1])   # just penalize high velocities
R = 1e-1*np.eye(2)

# Initial state
x0 = np.array([1.0, 2.0, 0, 0])

# Choose a solver
#solver = GurobiMICPSolver(spec, sys, x0, T, robustness_cost=True, robustness_type=RobustnessMetrics.Standard)
#solver = DrakeMICPSolver(spec, sys, x0, T, robustness_cost=True)
#solver = DrakeSos1Solver(spec, sys, x0, T, robustness_cost=True)
#solver = DrakeSmoothSolver(spec, sys, x0, T, k=2.0)
#solver1 = ScipyGradientSolver(spec, sys, x0, T, robustness_type=RobustnessMetrics.NewRobustness)
# solver2 = ScipyGradientSolver(spec, sys, x0, T, robustness_type=RobustnessMetrics.AGM)
# solver3 = ScipyGradientSolver(spec, sys, x0, T, robustness_type=RobustnessMetrics.Smooth)
#solver4 = ScipyGradientSolver(spec, sys, x0, T, robustness_type=RobustnessMetrics.LSE)
#Set bounds on state and control variables
# u_min = np.array([-1,-1])
# u_max = np.array([1, 1])
# x_min = np.array([0.0, 0.0, -1.0, -1.0])
# x_max = np.array([10.0, 10.0, 1.0, 1.0])

# Add quadratic running cost (optional)
#solver1.AddQuadraticCost(Q,R)
# solver2.AddQuadraticCost(Q,R)
# solver3.AddQuadraticCost(Q,R)
#solver4.AddQuadraticCost(Q,R)

#robustness_index = [0]
# robustness_index = [0, 1, 2, 3, 4, 5, 6]
robustness_index = [1, 4, 5]
solver = []
for i in range(0, 7): #set up all solver
    solver.append(solver_list(spec, sys, x0, T, i))
ax = plt.gca()
scenario.add_to_plot(ax)

#Solve the optimization problem
for i in robustness_index:
    print("Robustness type: ", get_robustness_name(i))
    solver[i].AddQuadraticCost(Q, R)
    xi, ui, _, _, pi = solver[i].Solve()
    if xi is not None:
        plt.scatter(*xi[:2, :], label=get_robustness_name(i))
        plt.plot(*xi[:2, :], '--')
ax.legend()

plt.figure()
for i in robustness_index:
    print("Robustness type: ", get_robustness_name(i))
    solver[i].AddQuadraticCost(Q, R)
    xi, ui, _, _, pi = solver[i].Solve()
    x = np.arange(0, len(pi), 1)
    y = pi
    plt.ylim(0, 1500)
    plt.xlim(0, 25)
    plt.plot(x, y, label=get_robustness_name(i))
plt.legend()
plt.show()

