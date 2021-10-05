

import numpy as np
import pandas as pd 
from pulp import *



def load_data():
    # Read file and convert into panda dataframe
    Weekday_Routes = pd.read_csv("Weekday_Routes.csv")
    Weekend_Routes = pd.read_csv("Weekend_Routes.csv")
    storeLocations = pd.read_csv("WoolworthsDemands.csv", usecols = [0])
    return Weekday_Routes, Weekend_Routes, storeLocations



def solve_lp(routeData, storeLocations): 
    
    
    
    #Get index for the df
    routes = routeData.index
    #print(routeData)
    durations = routeData['Duration']
    costs = durations.multiply(0.0625)

    print(routeData)

    firstStops = routeData.to_dict()['First Stop']
    secondStops = routeData.to_dict()['Second Stop']
    thirdStops = routeData.to_dict()['Third Stop']
    fourthStops = routeData.to_dict()['Fourth Stop']
    storeLocationDict = storeLocations.to_dict()['Store']

    routeVisits = np.zeros( (len(firstStops), len(storeLocations)) )


    



    for i in range(len(firstStops)):
        for j in range(len(storeLocations)):
            routeNumber = list(storeLocationDict.keys())[list(storeLocationDict.values()).index(firstStops[i])]
            routeVisits[i][routeNumber] = 1   

    print(routeVisits)   
    

    
    
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
    # prob += easternRoutes.index[r]>= route_chosen[f]*0.1
    # prob += easternRoutes.index[r]<= route_chosen[f]*1e5










    ##SOLVING ROUTINES
    #prob.writeLP('Routes.lp')
    # prob.solve()

    # The status of the solution is printed to the screen
    # print("Status:", LpStatus[prob.status])

    # for v in prob.variables():
    #     print(v.name, "=", v.varValue)
   
    # print("Optimised cost ", value(prob.objective))

    # Each of the variables is printed with its resolved optimum value

    return 




if __name__ == "__main__":
    Weekday_Routes, Weekend_Routes, storeLocations = load_data()

    # View all items: TieData
    #print(easternRoutes)

    #Get all labels (items): TieData.index
    #print(easternRoutes.index)

    #Get an entire column: TieData['Silk']
    #print(easternRoutes['First Stop'])

    #Get an entire row: TieData.loc['AllPoly']
    #print(easternRoutes.loc[3])

    #Get information about a particular item: TieData['Silk']['SilkCotton']
    #print(easternRoutes[3]['First Stop'])

    
    






    solve_lp(Weekday_Routes, storeLocations)

