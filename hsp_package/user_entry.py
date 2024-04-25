import numpy as np

def get_param():
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
    
    prompt_tol_param = "Enter Paramter Tolerance: \n"
    TolParam = float(input(prompt_tol_param))
    
    prompt_run_mode = "Enter your run Mode: \n"
    runMode = int(input(prompt_run_mode))
    
    return [MaxSols, TolParam, runMode]


def get_filter():
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