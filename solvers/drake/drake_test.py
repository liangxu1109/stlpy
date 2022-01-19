from solvers.drake.drake_base import DrakeSTLSolver
from STL import STLPredicate
import numpy as np
import time
from pydrake.all import (MathematicalProgram, 
                         GurobiSolver, MosekSolver, ClpSolver,
                         SolverOptions, CommonSolverOption,
                         eq, le, ge)
from pydrake.solvers.branch_and_bound import MixedIntegerBranchAndBound

from itertools import chain, combinations

class DrakeTestSolver(DrakeSTLSolver):
    """
    Scratch solver for implementing research ideas
    """
    def __init__(self, spec, sys, x0, T, M=1000, relaxed=False, robustness_cost=True, solver='gurobi'):
        assert M > 0, "M should be a (large) positive scalar"
        super().__init__(spec, sys, x0, T)
        self.M = M

        # Choose which solver to use
        if solver == 'gurobi':
            self.solver = GurobiSolver()
        elif solver == 'mosek':
            self.solver = MosekSolver()
        else:
            print("Using Naive Branch-and-Bound solver")
            self.solver = "bnb"

        # Get list of all conjunctive state formulas
        self.CSFs = self.spec.get_all_conjunctive_state_formulas()
        self.n_csf = len(self.CSFs)

        # Define a list of indexes for all possible combinations of CSFs
        s = [i for i in range(self.n_csf)]
        self.powerset_idx = list(chain.from_iterable(combinations(s, r) for r in range(len(s)+1)))

        # DEBUG: define global bounds on y
        # TODO: let the user determine this
        y_min = np.array([0,0,-1,-1,-0.5,-0.5])
        y_max = np.array([10,10,1,1,0.5,0.5])
        A0 = np.vstack([np.eye(6),-np.eye(6)])
        b0 = np.hstack([y_max,-y_min])

        # Define a list of inequalities (A*y<=b) associated with each possible
        # combination of CSFs.
        self.powerset = []
        for idx in self.powerset_idx:
            # TODO: check feasibility
            As = [A0]
            bs = [b0]
            for i in idx:
                state_formula = self.CSFs[i]
                A, b = state_formula.get_all_inequalities()
                As.append(A)
                bs.append(b)

            A = np.vstack(As)
            b = np.hstack(bs)

            self.powerset.append((A,b))


        # Define binary variables for each CSF at each timestep
        self.z = self.mp.NewBinaryVariables(self.n_csf,self.T,'z')
        

        # Flag for whether to use a convex relaxation
        self.convex_relaxation = relaxed

        # Add cost and constraints to the optimization problem
        self.AddDynamicsConstraints()
        self.AddSTLConstraints()
        self.AddRobustnessConstraint()
        if robustness_cost:
            self.AddRobustnessCost()

    def Solve(self):
        # Set verbose output
        options = SolverOptions()
        options.SetOption(CommonSolverOption.kPrintToConsole,1)
        #options.SetOption(GurobiSolver.id(), "Presolve", 2)
        self.mp.SetSolverOptions(options)
            
        if self.solver == "bnb":
            bnb_solver = MixedIntegerBranchAndBound(self.mp, ClpSolver.id())
            st = time.time()
            status = bnb_solver.Solve()
            solve_time = time.time() - st
            success = True
            res = bnb_solver

        else:
            res = self.solver.Solve(self.mp)
            success = res.is_success()
            solve_time = res.get_solver_details().optimizer_time
            
        print("")
        print("Solve time: ", solve_time)

        if success:
            x = res.GetSolution(self.x)
            u = res.GetSolution(self.u)

            y = np.vstack([x,u])
            rho = self.spec.robustness(y,0)[0]
            print("Optimal robustness: ", rho)
        else:
            print("No solution found")
            x = None
            u = None
            rho = -np.inf

        return (x,u, rho, solve_time)

    def AddDynamicsConstraints(self):
        """
        Add the constraints

            x_{t+1} = A@x_t + B@u_t
            x_0 = x0

        to the optimization problem. 
        """
        # Initial condition
        self.mp.AddConstraint(eq( self.x[:,0], self.x0 ))

        # Dynamics
        for t in range(self.T-1):
            self.mp.AddConstraint(eq(
                self.x[:,t+1], self.sys.A@self.x[:,t] + self.sys.B@self.u[:,t]
            ))
            self.mp.AddConstraint(eq(
                self.y[:,t], self.sys.C@self.x[:,t] + self.sys.D@self.u[:,t]
            ))
        self.mp.AddConstraint(eq(
            self.y[:,self.T-1], self.sys.C@self.x[:,self.T-1] + self.sys.D@self.u[:,self.T-1]
        ))

    def AddSTLConstraints(self):
        """
        Add the STL constraints

            (x,u) |= specification

        to the optimization problem, via the recursive introduction
        of binary variables for all subformulas in the specification.
        """
        # Add constraints to enforce state formulas depending on the value
        # of binary variables z
        for t in range(self.T):
            for i in range(self.n_csf):
                A, b = self.CSFs[i].get_all_inequalities()
                y = self.y[:,t]
                z = self.z[i,t]
                self.mp.AddLinearConstraint(le(
                    A@y - b, self.M*(1-z) - self.rho
                ))

        # Add a binary variable which takes a value of 1 only 
        # if the overall specification is satisfied.
        z_spec = self.mp.NewContinuousVariables(1)
        self.mp.AddConstraint(eq( z_spec, 1 ))

        # Recursively traverse the tree defined by the specification
        # subformulas and add similar binary constraints. 
        self.AddSubformulaConstraints(self.spec, z_spec, 0)

    def AddSubformulaConstraints(self, formula, z, t):
        """
        Given an STLFormula (formula) and a binary variable (z),
        add constraints to the optimization problem such that z
        takes value 1 only if the formula is satisfied (at time t). 

        If the formula is a predicate, this constraint uses the "big-M" 
        formulation

            A[x(t);u(t)] - b + (1-z)M >= 0,

        which enforces A[x;u] - b >= 0 if z=1, where (A,b) are the 
        linear constraints associated with this predicate. 

        If the formula is not a predicate, we recursively traverse the
        subformulas associated with this formula, adding new binary 
        variables z_i for each subformula and constraining

            z <= z_i  for all i

        if the subformulas are combined with conjunction (i.e. all 
        subformulas must hold), or otherwise constraining

            z <= sum(z_i)

        if the subformulas are combined with disjuction (at least one
        subformula must hold). 
        """
        # We're at the bottom of the tree, so add the big-M constraints
        if formula.is_conjunctive_state_formula():
            # Get indeces for all powersets that include this formula
            idx = self.CSFs.index(formula)
            idxs = []
            for i in range(len(self.powerset_idx)):
                if idx in self.powerset_idx[i]:
                    idxs.append(i)

            # Get the binary variable corresponding to this state_formula
            # (Note that this implementation is somewhat inefficient, since
            # the continuous variable z is redundant, but good solvers like
            # Gurobi should remove that redundancy efficiently in presolve)
            idx = self.CSFs.index(formula)
            self.mp.AddConstraint(eq( z, self.z[idx, t] ))
        
        # We haven't reached the bottom of the tree, so keep adding
        # boolean constraints recursively
        else:
            z_subs = self.mp.NewContinuousVariables(len(formula.subformula_list),1)
            self.mp.AddConstraint(ge(z_subs, 0))
                    
            if formula.combination_type == "and":
                self.mp.AddConstraint(le( z, z_subs ))
            else:  # combination_type == "or":
                self.mp.AddConstraint(le( z, sum(z_subs) ))

            for i, subformula in enumerate(formula.subformula_list):
                t_sub = formula.timesteps[i]
                self.AddSubformulaConstraints(subformula, z_subs[i], t+t_sub)
