"""Docstring for __main__.py file."""

import hsp_package as hsp

hsp.Create_Shelve(file_ext="/HSP_v1/hsp_package/HSP_Costs.csv")

sols = hsp.Load_Shelve()

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
