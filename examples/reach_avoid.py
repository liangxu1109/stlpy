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
from stlpy.enumerations.option import RobustnessMetrics

from stlpy.benchmarks import ReachAvoid
from stlpy.solvers import *
from stlpy.enumerations.option import RobustnessMetrics
from stlpy.solvers.scipy.scipysolver import solver_list

# Specification Parameters
goal_bounds = (7,8,8,9)     # (xmin, xmax, ymin, ymax)
obstacle_bounds = (3,5,4,6)
T = 25

# Define the system and specification
scenario = ReachAvoid(goal_bounds, obstacle_bounds, T)
#scenario = ReachAvoid(goal_bounds, obstacle_bounds, T, robustness_type= RobustnessMetrics.AGM)
spec = scenario.GetSpecification()
spec.flatten(spec)
spec.flatten(spec)
sys = scenario.GetSystem()

# Specify any additional running cost (this helps the numerics in
# a gradient-based method)
Q = 1e-5*np.diag([0,0,1,1])   # just penalize high velocities
R = 1e-1*np.eye(2)

# Initial state
x0 = np.array([1.0,2.0,0,0])

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
# u_min = np.array([-0.5,-0.5])
# u_max = np.array([0.5, 0.5])
# x_min = np.array([0.0, 0.0, -1.0, -1.0])
# x_max = np.array([10.0, 10.0, 1.0, 1.0])
#solver.AddControlBounds(u_min, u_max)
#solver.AddStateBounds(x_min, x_max)

# Add quadratic running cost (optional)
#solver1.AddQuadraticCost(Q,R)
# solver2.AddQuadraticCost(Q,R)
# solver3.AddQuadraticCost(Q,R)
#solver4.AddQuadraticCost(Q,R)

# Solve the optimization problem
# x, u, _, _= solver1.Solve()
# x2, u2, _, _= solver2.Solve()
# x3, u3, _, _= solver3.Solve()
#x4, u4, _, _= solver4.Solve()
#print(u)
# print(u2)
# print(u3)
# if x is not None:
#     # Plot the solution
#     ax = plt.gca()
#     scenario.add_to_plot(ax)
#     plt.scatter(*x[:2,:])
#     plt.show()

robustness_index = [0, 1, 2, 3]
solver = [0]
for i in robustness_index:
    solver.append(solver_list(spec, sys, x0, T, i))
ax = plt.gca()
scenario.add_to_plot(ax)

# Solve the optimization problem
for i in range(1,len(robustness_index)+1):
    xi, ui, _, _ = solver[i].Solve()
    if xi is not None:
        plt.scatter(*xi[:2, :])
plt.show()

