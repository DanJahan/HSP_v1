"""Docstring for HSP_Calc file."""

import shelve as sv  # data perstance: used to store a list of solvents in a shelve
import numpy as np
import pandas as pd
import os
from scipy.optimize import minimize



# runs minimize() on Cost()
if runMode == 0:
    ans = minimize(
        Cost,
        np.ones(len(Sols)) / len(Sols),
        constraints=[{"type": "ineq", "fun": f} for f in [c1, c2]]
        + [{"type": "eq", "fun": Equal1}],
        options={"maxiter": 1000},
    )

# runs minimize() on BlendDist()
elif runMode == 1:
    ans = minimize(
        BlendDist,
        np.ones(len(Sols)) / len(Sols),
        constraints=[{"type": "ineq", "fun": f} for f in [c1]]
        + [{"type": "eq", "fun": Equal1}],
        options={"maxiter": 1000},
    )

    # Pares down the solvent list of dictionaries to only the top solvents
# The amount of solvents in the resultant list will be equal to the MaxSols the user specified
Sols = [Sols[list(ans.x).index(b)] for b in sorted(list(ans.x), reverse=True)[:MaxSols]]


# Run minimize() with the pared down solvent list
limitAns = minimize(
    Cost,
    np.ones(len(Sols)) / len(Sols),
    constraints=[{"type": "ineq", "fun": f} for f in [c1, c2]]
    + [{"type": "eq", "fun": Equal1}],
    options={"maxiter": 2000},
)

# Rounds the found parameters to 3 decimal places
rounded = np.round(limitAns.x, 3)

# Uses an if statement to match the parameter with the correct solvent and prints the results
print(f"The targeted parameters are {Param}.")
print("An optimized solvent blend of")
for i, j in enumerate(rounded):
    if j > 0.0:
        print(f'{round(j*100,3)}% {Sols[i]["name"]}')
print(f"has parameters of {np.round(solventblend(rounded, Sols),2)}.")
print(f"The cost of the solvent blend is ${np.round(Cost(rounded), 3)} per liter.")
