#!/usr/bin/env python

##
#
# Set up, solve, and plot the solution for a simple
# reach-avoid problem, where a robot with nonlinear
# (unicycle) dynamics must avoid a circular obstacle
# before reaching a circular goal.
#
##

import numpy as np
import matplotlib.pyplot as plt

from stlpy.benchmarks import NonlinearReachAvoid
from stlpy.solvers import *
from stlpy.enumerations.option import RobustnessMetrics
from stlpy.solvers.scipy.scipysolver import solver_list, get_robustness_name
# Specification Parameters
goal = (7.5, 8.5)  # goal center and radius
goal_rad = 0.75
obs = (4.25, 5.25)     # obstacle center and radius
obs_rad = 1.5
T = 23

# Define the system and specification
scenario = NonlinearReachAvoid(goal, goal_rad, obs, obs_rad, T)
spec = scenario.GetSpecification()
sys = scenario.GetSystem()

# Specify any additional running cost (this helps the numerics in
# a gradient-based method)
Q = np.diag([0,0,0])
R = 1e-4*np.eye(2)

# Initial state
x0 = np.array([1.0,2.0,0])

# Choose a solver
#solver = DrakeSmoothSolver(spec, sys, x0, T, k=2.0)
# solver = ScipyGradientSolver(spec, sys, x0, T, robustness_type=RobustnessMetrics.AGM)

# Set bounds on state and control variables
# u_min = np.array([0,-5.0])
# u_max = np.array([10, 5.0])
# x_min = np.array([-10.0, -10.0, -2*np.pi])
# x_max = np.array([10.0, 10.0, 2*np.pi])
#solver.AddControlBounds(u_min, u_max)
#solver.AddStateBounds(x_min, x_max)

# Add quadratic running cost (optional)


# Solve the optimization problem
# robustness_index = [0, 1, 2, 3, 4, 5, 6]
robustness_index = [4, 5]
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
    plt.xlim(0, 50)
    plt.plot(x, y, label=get_robustness_name(i))
plt.legend()

plt.show()
