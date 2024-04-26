"""README for HSP_Calculator."""

#Use the following guild as an example for how to run the calculator:

#The desired parameters that the calculator will solve for
#Parameter ordering is dD, dP, dH
dD = 16
dP = 11
dH = 10

#Max solvents that the belnd will consist of
MaxSols = 4

#Run Mode for the calculator
#0 is minimizing cost of the blend
#1 is minimize distance of blend parameter to target parameter when cost is not a factor
#The default is 0
runMode = 0

#If using Run Mode 0:
#Tolerance used for the solvent blend constraint
#This is how close the solvent blend has to be to to the desired parameters
#Values between 0.1 - 1 work well
#The default is 0.5
TolParam = 0.5

#Enter 0 include solvents that are not in stock
#Enter 1 to filter out solvents that are not in stock
##The default is 1
filterInStock = 0

#Enter 0 include solvents that do not have cost data associated with them
#Enter 1 to filter out solvents that do not have cost data associated with them
#filterCost will be forced to  when using runMode = 0 
#The default is 1
filterCost = 1

#Enter 0 include solvents without considering NFPA data

#Enter 1 to filter out solvents based on user specified NFPA values below
#The default is 0
filterNFPA = 1

#If filterNFPA is on, enter Max NFPA values for Health, Fire and Reactivity. 
#Any solvents with values greater than the entered will be filtered out. 
#The defaults for each is 4, and will not filter out any solvents
Max_NFPA_Health = 4

Max_NFPA_Fire = 4

Max_NFPA_Reactivity = 4