"""Docstring for HSP_Functions file."""

# Import relevant libraries
import shelve as sv  # data perstance: used to store a list of solvents in a shelve
import numpy as np
import pandas as pd
import os
from scipy.optimize import minimize


##############################################
#   Create the shelve file from .csv file
##############################################
def Create_Shelve(file_ext="/HSP_v1/hsp_package/HSP_Costs.csv"):
    """Create shelve file."""

    # Imports the solvents .cvs file into 'filePath' for storage
    path = os.getcwd()
    filePath = path + file_ext

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

    return


##############################################
#   Load the shelve file
##############################################
def Load_Shelve():
    """Load solvent shelve."""
    # Opens solvents shelve
    solvents = sv.open("solvents")

    # stores the solvent dictionary in Sols for use in the functions/constraints below
    sols = solvents["solvents"]

    # Close the solvents shelve
    solvents.close()

    return sols


##############################################
#   User Interface
##############################################
def get_hansen():

    prompt_dD = "Enter your dD parameter: \n"
    dD = float(input(prompt_dD))

    prompt_dP = "Enter your dP parameter: \n"
    dP = float(input(prompt_dP))

    prompt_dH = "Enter your dH parameter: \n"
    dH = float(input(prompt_dH))

    return np.array([dD, dP, dH])


def get_mode():
    """Get solvent modes."""
    prompt_max_sols = "Enter Maximum of solvents in your blends: \n"
    MaxSols = int(input(prompt_max_sols))

    prompt_tol_param = "Enter Parameter Tolerance: \n"
    TolParam = float(input(prompt_tol_param))

    prompt_run_mode = "Enter your run Mode: (1 or 0) \n"
    runMode = int(input(prompt_run_mode))

    return [MaxSols, TolParam, runMode]


def get_NFPA():
    """Take user input to determine the NFPA values."""
    prompt_Health = "Enter your max Health NFPA: \n"
    Max_NFPA_Health = int(input(prompt_Health))

    prompt_Fire = "Enter your max Fire NFPA: \n"
    Max_NFPA_Fire = int(input(prompt_Fire))

    prompt_React = "Enter your max Reactivity NFPA: \n"
    Max_NFPA_Reactivity = int(input(prompt_React))

    return [Max_NFPA_Health, Max_NFPA_Fire, Max_NFPA_Reactivity]


def get_filter():
    """Take user input to determine solvent filtering."""

    prompt_inStock = "Filter out solvents not in stock: (1 or 0)\n"
    inStock = bool(int(input(prompt_inStock)))

    prompt_cost = "Filter out solvents with no cost data: (1 or 0)\n"
    cost = bool(int(input(prompt_cost)))

    prompt_NFPA = "Would you like to filter for NFPA values? (1 or 0)\n"
    NFPA = bool(int(input(prompt_NFPA)))

    if NFPA:
        NFPA = get_NFPA()

    return [inStock, cost, NFPA]


def get_param():
    """Get user parameters for running script."""
    print(
        "Welcome to the Hansen Solubility Calculator! \n User input prompts will be displayed below."
    )

    hansen = get_hansen()
    mode = get_mode()
    filter = get_filter()

    return [hansen, mode, filter]


##############################################
#   Filter Solvents
##############################################


def filterNFPA(NFPA, sols):
    """Remove any solvents that have a NFPA value greater than the user inputted values."""

    [Health, Fire, React] = NFPA
    sols = [sol for sol in sols if sol["nfpa"][0] <= Health]
    sols = [sol for sol in sols if sol["nfpa"][1] <= Fire]
    sols = [sol for sol in sols if sol["nfpa"][2] <= React]
    return sols


def filterCost(sols):
    """Remove solvents from the list that have no data in the cost column."""
    sols = [sol for sol in sols if sol["cost"] == sol["cost"]]
    return sols


def filterInStock(sols):
    """If the filterStock parameter is on, remove any solvents from the list that are not in stock."""
    sols = [sol for sol in sols if sol["stock"]]
    return sols


def pareSols(ans, maxSols, sols):

    sols = [
        sols[list(ans.x).index(b)] for b in sorted(list(ans.x), reverse=True)[:maxSols]
    ]
    return sols


##############################################
#   Solvent Blend Functions
##############################################


def solventblend(SolAmount, sols):
    """Create blended solvent parameters based on the proportions of solvents used."""
    props = np.zeros(3)  # Variable for storing the parameters
    for i in range(
        len(sols)
    ):  # for each solvent, multiply by the parameters by amount used
        props += SolAmount[i] * sols[i]["parameters"]
    return props


def SumSqr(A, B):
    """Square of euclidean distances."""
    diff = A - B
    diff = diff**2
    diff = sum(diff)
    return diff


def Cost(L, sols):
    """Cost function that will be used to in the minimize function."""
    cost = 0
    for i in range(len(sols)):
        cost += L[i] * sols[i]["cost"]
    return cost


def BlendDist(L, hansen, sols):
    """Find square of euclidean distances between the target blend parameters and a given blend's parameters."""
    return SumSqr(solventblend(L, sols), hansen)


##############################################
#   Constraints
###############################################
def EqualTo1(L):
    """Ensure the blend of solvents adds to 1 (100%)."""
    return 1 - sum(L)


def NoNegativeSols(L):
    """Ensure no amount of solvent used is negative."""
    m = min(L)
    return m


def ToleranceError(L, hansen, tolParam, sols):
    """Ensure the blend of solvent parameters stays within the tolerance."""
    n = (tolParam**2) - SumSqr(solventblend(L, sols), hansen)
    return n


##############################################
#   Optimization Functions
##############################################
def runModeCost(hansen, tolParam, maxSols, sols):
    """Runs the calculator on tolerance optimization only"""

    def solCost(L):
        return Cost(L, sols)

    def tolError(L):
        return ToleranceError(L, hansen, tolParam, sols)

    ans = minimize(
        solCost,
        np.ones(len(sols)) / len(sols),
        constraints=[{"type": "ineq", "fun": f} for f in [NoNegativeSols, tolError]]
        + [{"type": "eq", "fun": EqualTo1}],
        options={"maxiter": 1000},
    )

    sols = pareSols(ans, maxSols, sols)

    ans = minimize(
        solCost,
        np.ones(len(sols)) / len(sols),
        constraints=[{"type": "ineq", "fun": f} for f in [NoNegativeSols, tolError]]
        + [{"type": "eq", "fun": EqualTo1}],
        options={"maxiter": 2000},
    )

    return [ans, sols]


def runModeTol(hansen, tolParam, maxSols, sols):
    """Runs the calculator on tolerance optimization only"""

    def solBlendDist(L):
        return BlendDist(L, hansen, sols)

    def tolError(L):
        return ToleranceError(L, hansen, tolParam, sols)

    ans = minimize(
        solBlendDist,
        np.ones(len(sols)) / len(sols),
        constraints=[{"type": "ineq", "fun": f} for f in [NoNegativeSols]]
        + [{"type": "eq", "fun": EqualTo1}],
        options={"maxiter": 1000},
    )

    sols = pareSols(ans, maxSols, sols)

    ans = minimize(
        solBlendDist,
        np.ones(len(sols)) / len(sols),
        constraints=[{"type": "ineq", "fun": f} for f in [NoNegativeSols]]
        + [{"type": "eq", "fun": EqualTo1}],
        options={"maxiter": 2000},
    )

    return [ans, sols]


##############################################
#   Output Functions
##############################################


def output(ans, hansen, sols):
    rounded = np.round(ans.x, 3)

    print(f"The targeted parameters are {hansen}.")
    print("An optimized solvent blend of")
    for i, j in enumerate(rounded):
        if j > 0.0:
            print(f'{round(j*100,3)}% {sols[i]["name"]}')
    print(f"has parameters of {np.round(solventblend(rounded, sols),2)}.")
    print(
        f"The cost of the solvent blend is ${np.round(Cost(rounded, sols), 3)} per liter."
    )
