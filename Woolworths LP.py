

import numpy as np
import pandas as pd 
from pulp import *



def load_data():
    # Read file and convert into panda dataframe
    easternRoutes = pd.read_csv("Eastern_Routes.csv")
    storeLocations = pd.read_csv("WoolworthsDemands.csv", usecols = [0])
    return easternRoutes, storeLocations



def solve_lp(regionRoutes): 
    
    
    routeData = regionRoutes
    #Get index for the df
    routes = easternRoutes.index
    #get store columns for the df
    #stores = pd.Series([str(x) for x in range(64 + 1)], index = routes)
    
    # routeData = pd.DataFrame({'routeNumber': routes, 
    #                             'Stores': stores, })

    #for i,x in enumerate(routes):
        
    

    #create prob variable object for problem data
    #prob = LpProblem("Eastern Routes", LpMinimize)

    #Dictionary containing route variables
    #route_chosen = LpVariable.dicts("chosen", routes, 0, 1, cat = 'Integer')


    # #input the obj function into prob using the profits for eatch tie type
    #prob +=lpSum([cost[i]*route_chosen[i] for i in easternRoutes.index]), "Objective cost function"

    # for r in easternRoutes.index:
    # prob += easternRoutes.index[r]>= route_chosen[r]*0.1
    # prob += easternRoutes.index[r]<= route_chosen[r]*1e5










    ##SOLVING ROUTINES
    #prob.writeLP('Routes.lp')
    # prob.solve()

    # The status of the solution is printed to the screen
    # print("Status:", LpStatus[prob.status])

    # for v in prob.variables():
    #     print(v.name, "=", v.varValue)
   
    # print("Optimised cost ", value(prob.objective))

    # Each of the variables is printed with its resolved optimum value

    return routeData




if __name__ == "__main__":
    easternRoutes, storeLocations = load_data()

     
    






    print(solve_lp(easternRoutes))

