#!/usr/bin/env python

##
#
# Set up, solve, and plot the solution for the "reach-avoid"
# scenario, where the robot must reach one of two targets before
# reaching the goal.
#
##

import numpy as np
import matplotlib.pyplot as plt
from stlpy.benchmarks import EitherOr
from stlpy.solvers import *
from stlpy.enumerations.option import RobustnessMetrics
from stlpy.solvers.scipy.scipysolver import solver_list
# Specification Parameters
goal = (7,8,8,9)     # (xmin, xmax, ymin, ymax)
target_one = (1,2,6,7)
target_two = (7,8,4.5,5.5)
obstacle = (3,5,4,6)
T = 20
dwell_time = 5

# Create the specification
scenario = EitherOr(goal, target_one, target_two, obstacle, T, dwell_time)
spec = scenario.GetSpecification()
spec.simplify()
sys = scenario.GetSystem()

# Specify any additional running cost
Q = 1e-1*np.diag([0,0,1,1])   # just penalize high velocities
R = 1e-0*np.eye(2)

# Initial state
x0 = np.array([2.0,2.0,0,0])

# Specify a solution strategy
#solver = GurobiMICPSolver(spec, sys, x0, T, robustness_cost=True)
#solver = DrakeMICPSolver(spec, sys, x0, T, robustness_cost=True)
#solver = DrakeSos1Solver(spec, sys, x0, T, robustness_cost=True)
robustness_index = [1, 2, 3]
solver = [0]
for i in robustness_index:
    solver.append(solver_list(spec, sys, x0, T, i))

# Set bounds on state and control variables
# u_min = np.array([-0.5,-0.5])
# u_max = np.array([0.5, 0.5])
# x_min = np.array([0.0, 0.0, -1.0, -1.0])
# x_max = np.array([10.0, 10.0, 1.0, 1.0])
#solver.AddControlBounds(u_min, u_max)
#solver.AddStateBounds(x_min, x_max)

# Add quadratic running cost (optional)
#solver.AddQuadraticCost(Q,R)

ax = plt.gca()
scenario.add_to_plot(ax)
# Solve the optimization problem
for i in range(1,len(robustness_index)+1):
    xi, ui, _, _ = solver[i].Solve()
    if xi is not None:
        plt.scatter(*xi[:2, :])
plt.show()

