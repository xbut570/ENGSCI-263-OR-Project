

import numpy as np
from numpy.core.numeric import NaN
import pandas as pd 
from pulp import *

np.set_printoptions(threshold=sys.maxsize)
pd.set_option('display.max_rows', None)

# Stores are rows, routes are columns.  Change value to 1 if route visits store

def load_data():
    # Read file and convert into panda dataframe
    Weekday_Routes = pd.read_csv("Weekday_Routes.csv")
    Weekend_Routes = pd.read_csv("Weekend_Routes.csv")
    storeLocations = pd.read_csv("WoolworthsDemands.csv", usecols = [0])
    return Weekday_Routes, Weekend_Routes, storeLocations

def column_generation(routeData, storeLocations):

    firstStops = routeData.to_dict()['First Stop']
    secondStops = routeData.to_dict()['Second Stop']
    thirdStops = routeData.to_dict()['Third Stop']
    fourthStops = routeData.to_dict()['Fourth Stop']
    storeLocationDict = storeLocations.to_dict()['Store']
    routeVisits = np.zeros( (len(storeLocations), len(firstStops)) )

    #pulls the location number from a route number 
    locationNumber = list(storeLocationDict.keys())[list(storeLocationDict.values()).index(firstStops[160])]

    for i in range(len(firstStops)):
        #pulls the location number from a route number
        if pd.isna(firstStops[i]) is False:
            locationNumber = list(storeLocationDict.keys())[list(storeLocationDict.values()).index(firstStops[i])]
            routeVisits[locationNumber][i] = 1   
    
    for i in range(len(secondStops)):
        #pulls the location number from a route number 
        if pd.isna(secondStops[i]) is False:
            locationNumber = list(storeLocationDict.keys())[list(storeLocationDict.values()).index(secondStops[i])]
            routeVisits[locationNumber][i] = 1  
    
    for i in range(len(thirdStops)):
        #pulls the location number from a route number 
        if pd.isna(thirdStops[i]) is False:
            locationNumber = list(storeLocationDict.keys())[list(storeLocationDict.values()).index(thirdStops[i])]
            routeVisits[locationNumber][i] = 1  
    
    for i in range(len(fourthStops)):
        #pulls the location number from a route number
        if pd.isna(fourthStops[i]) is False:
            locationNumber = list(storeLocationDict.keys())[list(storeLocationDict.values()).index(fourthStops[i])]
            routeVisits[locationNumber][i] = 1  

    return routeVisits

def solve_lp(routeData, storeLocations): 

    routeVisits = column_generation(routeData, storeLocations)
    rows = np.shape(routeVisits)[0]
    columns = np.shape(routeVisits)[1]
    
    #Get index for the df
    routes = routeData.index
    
    durations = routeData['Duration']
    costs = durations.multiply(0.0625)

    for i in range(len(durations)):
        if (durations[i] > 14400):
            costs[i] += 2000
    
    demands = routeData['Demand']
    for i in range(len(demands)):
        if demands[i] > 26:
            costs[i] += 2000

    costs = costs.to_dict()

    #create prob variable object for problem data
    prob = LpProblem("Routes", LpMinimize)

    #Dictionary containing route variables
    route_chosen = LpVariable.dicts("route", routes, 0, None, cat = 'Binary')

    #input the obj function into prob using the profits for each tie type
    prob +=lpSum([costs[i]*route_chosen[i] for i in routes]), "Objective cost function"
    

    #constraint: each route only visits node once
    for i in range(rows):    
        prob += lpSum([route_chosen[b] * routeVisits[i][b] for b in routes]) == 1

    #constraint: Trucks
    prob += lpSum(route_chosen[i] for i in routes) <= 60


        
    # for r in easternRoutes.index:
    # prob += easternRoutes.index[r]>= route_chosen[f]*0.1
    # prob += easternRoutes.index[r]<= route_chosen[f]*1e5


    ##SOLVING ROUTINES
    prob.writeLP('Routes.lp')
    prob.solve()

    # The status of the solution is printed to the screen
    #print("Status:", LpStatus[prob.status])

    '''for v in prob.variables():
        print(v.name, "=", v.varValue)
    '''

    #print("Optimised cost ", value(prob.objective))

    #optimalRoutes = np.array(list(dict(zip( range(len(prob._variables)), prob._variables)).items()))[:,0]
    

    for i in range(len(prob._variables)):
        prob._variables[i] = int(str(prob._variables[i]).replace("route_", ""))

    optimalRoutes = prob._variables

    optimalRouteData = pd.DataFrame(columns=routeData.columns)
    optimalRouteData = routeData.loc[np.r_[optimalRoutes]]

    
    return LpStatus[prob.status], value(prob.objective), optimalRouteData




if __name__ == "__main__":
    Weekday_Routes, Weekend_Routes, storeLocations = load_data()

    status, minimisedCost, routes = solve_lp(Weekday_Routes, storeLocations)
    #status, minimisedCost, routes = solve_lp(Weekend_Routes, storeLocations)

    print("Status: ", status)
    print("Minimal Cost: ", minimisedCost)
    print("Routes: \n", routes)


