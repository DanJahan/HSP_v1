"""Docstring for HSP_Calc file."""

import shelve as sv  # data perstance: used to store a list of solvents in a shelve
import numpy as np
import pandas as pd
import os
from scipy.optimize import minimize

# Imports the solvents .cvs file into 'filePath' for storage
path = os.getcwd()
filePath = f"{path}/HSP_v1/hsp_package/HSP_Costs.csv"


# Uses Pandas library to read the .csv file into SOLVENTS, turns the data into rows in rowsList
SOLVENTS = pd.read_csv(filePath, header=0)
rowsList = list(SOLVENTS.iterrows())


# Placeholder variable for the solvents list
solventList = []


# Builds the solvent list of dictionaries by iterating through rowsList and matching the values with
# the correct keys for each solvent
for i in range(len(rowsList)):
    sol = rowsList[i][1]
    solventList.append(
        {
            "name": sol["Solvents"],
            "parameters": np.array([sol["dD"], sol["dP"], sol["dH"]]),
            "molvol": sol["MVol"],
            "cost": sol["Cost"],
            "nfpa": np.array([sol["Health"], sol["Fire"], sol["Reactivity"]]),
            "stock": sol["Stock"],
        }
    )


# Writes the solvent list of dictionaries to the shelf file
solvents = sv.open("solvents")
solvents["solvents"] = solventList

# Syncs the Shelf file
solvents.sync()

# Closes the shelf file
solvents.close()

# Opens solvents shelve
solvents = sv.open("solvents")

# stores the# Run minimize() with the pared down solvent list
limitAns = minimize(
  runcost,
    np.ones(len(Sols)) / len(Sols),
    constraints=[{"type": "ineq", "fun": f} for f in [c1, c2]]
    + [{"type": "eq", "fun": Equa solvent dictionary in Sols for use in the functions/constraints below
Sols = solvents["solvents"]

# Close the solvents shelve
solvents.close()

# User Specified Parameters

# The desired parameters that the calculator will solve for
# Parameter ordering is dD, dP, dH
dD = 16
dP = 11
dH = 10

# Max solvents that the belnd will consist of
MaxSols = 4

# Run Mode for the calculator
# 0 is minimizing cost of the blend
# 1 is minimize distance of blend parameter to target parameter when cost is not a factor
# The default is 0
runMode = 0

# If using Run Mode 0:
# Tolerance used for the solvent blend constraint
# This is how close the solvent blend has to be to to the desired parameters
# Values between 0.1 - 1 work well
# The default is 0.5
TolParam = 0.5

# Enter 0 include solvents that are not in stock
# Enter 1 to filter out solvents that are not in stock
# The default is 1
filterInStock = 0

# Enter 0 include solvents that do not have cost data associated with them
# Enter 1 to filter out solvents that do not have cost data associated with them
# filterCost will be forced to  when using runMode = 0
# The default is 1
filterCost = 1

# Enter 0 include solvents without considering NFPA data

# Enter 1 to filter out solvents based on user specified NFPA values below
# The default is 0
filterNFPA = 1

# If filterNFPA is on, enter Max NFPA values for Health, Fire and Reactivity.
# Any solvents with values greater than the entered will be filtered out.
# The defaults for each is 4, and will not filter out any solvents
Max_NFPA_Health = 4

Max_NFPA_Fire = 4

Max_NFPA_Reactivity = 4

# Stores the user specified target parameters into a numpy array
Param = np.array([dD, dP, dH])

# Determines the min and max dD, dP, and dH that are included in the solvents list
solParamMaxdD = max([sol["parameters"][0] for sol in Sols])
solParamMindD = min([sol["parameters"][0] for sol in Sols])
solParamMaxdP = max([sol["parameters"][1] for sol in Sols])
solParamMindP = min([sol["parameters"][1] for sol in Sols])
solParamMaxdH = max([sol["parameters"][2] for sol in Sols])
solParamMindH = min([sol["parameters"][2] for sol in Sols])

# Checks that the user entered target parameter is within the min/max range of dD, dP, and dH in
# the solvents list
ParamCheck = (
    (solParamMaxdD < Param[0])
    or (solParamMindD > Param[0])
    or (solParamMaxdP < Param[1])
    or (solParamMindP > Param[1])
    or (solParamMaxdH < Param[2])
    or (solParamMindH > Param[2])
)

# Prints an error if the user entered target parameter is outside the min/max range
if ParamCheck:
    print("Target parameter is unreachable.")
    print(f"dD of solvents are between {solParamMindD} and {solParamMaxdD}.")
    print(f"dP of solvents are between {solParamMindP} and {solParamMaxdP}.")
    print(f"dH of solvents are between {solParamMindH} and {solParamMaxdH}.")

# Checks that the user entered max solvents for the blend is within the range
b = len(Sols)
if MaxSols not in range(1, b + 1):
    print(f"Please input a valid of MaxSols. Any whole number between 1 and {b}.")

# Checks that the user entered run mode is valid
if runMode not in range(2):
    print("Unknown Run Mode. Please enter a value of either 0 or 1.")

# Checks that the user entered tolerance is valid
try:
    if TolParam < 0:
        print(
            "Unknown parameter tolerance. Please enter a value greater than or equal to 0."
        )
except:
    print(
            "Could not understand input. Please enter a number greater than or equal to 0."
        )


# Checks that the user entered fliterCost is valid
if filterCost not in range(2):
    print("Please enter 0 or 1 for filterCost.")

# Checks that the user entered fliterInStock is valid
if filterInStock not in range(2):
    print("Please enter 0 or 1 for filterStock.")

# Checks that the user entered NFPA option is valid
if filterNFPA not in range(2):
    print("Please enter 0 or 1 for filterNFPA.")

# Checks that the user entered NFPA values are valid
if filterNFPA == 1:
    if Max_NFPA_Health not in range(5):
        print("Unknown Healbool([3, 3, 4])th NFPA value. Please enter a whole number between 0 and 4.")

    if Max_NFPA_Fire not in range(5):
        print("Unknown Health NFPA value. Please enter a whole number between 0 and 4.")

    if Max_NFPA_Reactivity not in range(5):
        print("Unknown Health NFPA value. Please enter a whole number between 0 and 4.")

print("All good")

# If the runMode is 0 (minimizing solvent blend on cost), the the filterCost parameter is forced on
if runMode == 0:
    filterCost = 1

# If the filterCost parameter is on, remove solvents from the list that have no data in the cost column
if filterCost == 1:
    Sols = [sol for sol in Sols if sol["cost"] == sol["cost"]]

# If the filterStock parameter is on, remove any solvents from the list that are not in stock
if filterInStock == 1:
    Sols = [sol for sol in Sols if sol["stock"] == True]

# Removes any solvents that have a NFPA value greater than the user inputted values
if filterNFPA == 1:
    Sols = [sol for solan in Sols if sol["nfpa"][0] <= Max_NFPA_Health]
    Sols = [sol for sol in Sols if sol["nfpa"][1] <= Max_NFPA_Fire]
    Sols = [sol for sol in Sols if sol["nfpa"][2] <= Max_NFPA_Reactivity]


def solventblend(SolAmount, Sols):
    """Create blended solvent parameters based on the proportions of solvents used."""
    props = np.zeros(len(Param))  # Varaible for storing the parameters
    for i in range(
        len(Sols)
    ):  # for each solvent, multiply by the parameters by amount used
        props += SolAmount[i] * Sols[i]["parameters"]
    return props


def SumSqr(A, B):
    """Square of euclidean distances."""
    diff = A - B
    diff = diff**2
    diff = sum(diff)
    return diff


def Cost(L, *, solventsList):
    """Cost function that will be used to in the minimize function."""
    cost = 0
    for i in range(len(solventsList)):
        cost += L[i] * solventsList[i]["cost"]
    return cost


def BlendDist(L):
    """Find square of euclidean distances between the target blend parameters and a given blend's parameters."""
    return SumSqr(solventblend(L, Sols), Param)


# Constraints
def Equal1(L):
    """Ensure the blend of solvents adds to 1 (100%)."""
    return 1 - sum(L)


def c1(L):
    """Ensure no amount of solvent used is negative."""
    m = min(L)
    return m


def c2(L):
    """Ensure the blend of solvent parameters stays within the tolerance."""
    n = (TolParam**2) - SumSqr(solventblend(L, Sols), Param)
    return n



def runcost(L):
  return Cost(L, solventsList = Sols)
  
# runs minimize() on Cost()
if runMode == 0:
    print("Running!")
    ans = minimize(
      runcost,
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
  runcost,
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
print(f"The cost of the solvent blend is ${np.round(Cost(rounded, solventsList = Sols), 3)} per liter.")
