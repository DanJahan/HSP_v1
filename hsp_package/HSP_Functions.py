"""Docstring for HSP_Functions file."""

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
def get_param():
    
    prompt_dD = "Enter your dD parameter: \n"
    dD = float(input(prompt_dD))
    
    prompt_dP = "Enter your dP parameter: \n"
    dP = float(input(prompt_dP))
    
    prompt_dH = "Enter your dH parameter: \n"
    dH = float(input(prompt_dH))
    
    return np.array([dD, dP, dH])

##############################################
#   Filter Solvents
##############################################

def filterNFPA(Health,Fire,React,sols):
    """Remove any solvents that have a NFPA value greater than the user inputted values."""
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
    sols = [sol for sol in sols if sol["stock"] == True]
    return sols


##############################################
#   Solvent Blend Functions
##############################################

def solventblend(SolAmount, sols):
    """Create blended solvent parameters based on the proportions of solvents used."""
    props = np.zeros(len(Param))  # Varaible for storing the parameters
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

def Cost(L,sols):
    """Cost function that will be used to in the minimize function."""
    cost = 0
    for i in range(len(sols)):
        cost += L[i] * sols[i]["cost"]
    return cost


def BlendDist(L, sols):
    """Find square of euclidean distances between the target blend parameters and a given blend's parameters."""
    return SumSqr(solventblend(L, sols), Param)


##############################################
#   Constraints
##############################################
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
