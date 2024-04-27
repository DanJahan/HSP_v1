"""Docstring for __main__.py file."""

# Imports the package
import hsp_package as hsp

# Creates shelve file
hsp.Create_Shelve(file_ext="/HSP_v1/hsp_package/HSP_Costs.csv")

# Loads shelve file and stores it in variable "sols"
sols = hsp.Load_Shelve()

# Prompts the user to input parameters and saves parameters to variables
[hansen, mode, filter] = hsp.get_param()
[maxSols, tolParam, runMode] = mode
[stock, cost, NFPA] = filter

# Filter in Stock
if stock == 1:
    sols = hsp.filterInStock(sols)

# Filter Cost
if runMode == 0 or cost == 1:
    sols = hsp.filterCost(sols)

# Filter NFPA
if NFPA:
    sols = hsp.filterNFPA(filter[2], sols)

# Runs the Calculator base on the Run Mode
if runMode == 0:
    [ans, paredSols] = hsp.runModeCost(hansen, tolParam, maxSols, sols)
elif runMode == 1:
    [ans, paredSols] = hsp.runModeTol(hansen, tolParam, maxSols, sols)

# Outputs the results
print(hsp.output(ans, hansen, paredSols))
