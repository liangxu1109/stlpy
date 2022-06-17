#!/usr/bin/env python

##
#
# Set up, solve, and plot the solution for the door-puzzle
# scenario, where a robot needs to pick up several keys
# before reaching a goal region.
#
##

import numpy as np
import matplotlib.pyplot as plt
from stlpy.benchmarks import DoorPuzzle
from stlpy.solvers import *
from stlpy.solvers.scipy.gradient_solver import ScipyGradientSolver
from stlpy.enumerations.option import RobustnessMetrics

# Specification Parameters
T = 25
N_pairs = 2

# Create the specification and system
scenario = DoorPuzzle(T, N_pairs)
spec = scenario.GetSpecification()
spec.simplify()
sys = scenario.GetSystem()

# Specify any additional running cost (this helps the numerics in
# a gradient-based method)
Q = 1e-1*np.diag([0,0,1,1])   # just penalize high velocities
R = 1e-1*np.eye(2)

# Initial state
x0 = np.array([6.0,1.0,0,0])

# Define the solver
#solver = GurobiMICPSolver(spec, sys, x0, T, robustness_cost=False, robustness_type=RobustnessMetrics.Standard)
#solver = DrakeMICPSolver(spec, sys, x0, T, robustness_cost=True)
#solver = DrakeSos1Solver(spec, sys, x0, T, robustness_cost=True)
solver = ScipyGradientSolver(spec,sys,x0,T, robustness_type=RobustnessMetrics.Standard)
# Set bounds on state and control variables
u_min = np.array([-0.5,-0.5])
u_max = np.array([0.5, 0.5])
x_min = np.array([0.0, 0.0, -2.0, -2.0])
x_max = np.array([15.0, 10.0, 2.0, 2.0])
# solver.AddControlBounds(u_min, u_max)
# solver.AddStateBounds(x_min, x_max)

# Add quadratic running cost (optional)
solver.AddQuadraticCost(0.01*Q,0.01*R)

# Solve the optimization problem
x, u, _, _ = solver.Solve()
print(x.shape)

if x is not None:
    # Plot the solution
    ax = plt.gca()
    scenario.add_to_plot(ax)
    plt.scatter(*x[:2,:])
    plt.show()
