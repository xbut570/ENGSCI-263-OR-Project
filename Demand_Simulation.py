import numpy as np
import pandas as pd
from Woolworths_LP import *
import statistics as stats

np.set_printoptions(threshold=sys.maxsize)
pd.set_option("display.max_rows", None)

simulations = 1000
np.random.seed(100)

def load_data():
    """Loads data from csv files for routes, locations, and demands

    Parameters:
    -----------
    none

    Returns:
    --------
    Weekday_Routes : Panda dataframe
        Array of routes outputted by Route_Generation.py for weekdays
    Weekend_Routes : Panda dataframe
        Array of routes outputted by Route_Generation.py for weekends
    storeLocations : Panda dataframe
        Array of store names and locations
    demand : Panda dataframe
        Array of all demands over time for each store, sorted with
        weekdays first followed by weekends
    """

    # Read files and convert into panda dataframes
    Weekday_Routes = pd.read_csv("Weekday_Routes.csv")
    Weekend_Routes = pd.read_csv("Weekend_Routes.csv")
    storeLocations = pd.read_csv("WoolworthsDemands.csv", usecols=[0])
    demand = pd.read_csv("Formatted Demands.csv")

    return Weekday_Routes, Weekend_Routes, storeLocations, demand


def demand_simulator(routes, demand, isSaturday):
    """Calculates the demand for inputted routes, randomly decided using 1 of the
    given data points for that day.

    Parameters:
    -----------
    routes : Panda dataframe
        Dataframe of pre written routes containing trip duration and stops
    demand : Panda dataframe
        Dataframe containing the demands for each store for both weekdays and weekend
    isSaturday : Boolean
        Boolean equalling true if this route is for the weekend

    Returns:
    --------
    routes : Panda dataframe
        Dataframe containing the route time length, total demand, and stops visited
        Note, the duration values are still based off of the orginal demand and have
        not been recalculated
    """
    
    # Defines shape of arrays
    rows, cols = routes.shape
    demandRows, demandCols = demand.shape

    # Establishes which demand values to use
    if isSaturday:
        demandColMin = 22
        demandColMax = 25
    else:
        demandColMin = 1
        demandColMax = 21
    # Sets each value in the "demand" column to the routes dataframe to 0
    routes["Demand"] = 0

    # Loops through each of the routes adding their demand, and the time taken to unload packages
    # (which is based off of demand)
    # Stops searching once the correct demand is found and does not check nans
    for i in range(0, rows):
        for j in range(3, 6):
            currentStore = routes.iloc[i, j]
            if not pd.isna(currentStore):
                for k in range(0, demandRows):
                    if currentStore == demand.iloc[k, 0]:
                        demandCol = np.random.randint(demandColMin, demandColMax)
                        routes.iloc[i, 1] += demand.iloc[k, demandCol]                        

    return routes


def demand_evaluator(routes, minCost):
    """Evaluates demands for routes testing if they are above truck capacity.
        If they are, the cost of wet leasing a truck is added for each route 
        above capacity.

    Parameters:
    -----------
    routes : Panda dataframe
        Dataframe of pre written routes containing trip duration and stops
    minCost : Double
        Value representing the current minimum cost of a route, set to 0 
        so the output only represents the costs of additional trucks.

    Returns:
    --------
    minCost : Double
        Number representing the additional cost of extra trucks for routes
    """    
    
    # Defines shape of arrays
    rows, cols = routes.shape

    # Loops through routes testing if any routes are over capacity, if they
    # are the cost is increased
    for i in range(0,rows):
        if routes.iloc[i,1] > 26:
            minCost += 2000
    
    return minCost

if __name__ == "__main__":
    # Loads in data
    Weekday_Routes, Weekend_Routes, storeLocations, demand = load_data()
    
    # Solves for optimal routes using Woolworths_LP
    status, weekdayMinCost, weekdaySolved = solve_lp(Weekday_Routes, storeLocations)
    status, satMinCost, satSolved = solve_lp(Weekend_Routes, storeLocations, True)

    # Preinitializes arrays of costs
    weekdayCost = [0] * simulations
    satCost = [0] * simulations

    # Runs the given number of simulations for weekday and saturday evaluations
    for i in range(0,simulations):
        simulationWeekday = demand_simulator(weekdaySolved, demand, False)
        weekdayCost[i] = demand_evaluator(simulationWeekday, 0)
        simulationSat = demand_simulator(satSolved, demand, True)
        satCost[i] = demand_evaluator(simulationSat, 0)

    # Calculates the minimum, mean, and maximum valeus of costs
    weekRange = [(min(weekdayCost),stats.mean(weekdayCost),max(weekdayCost))]
    satRange = [(min(satCost),stats.mean(satCost),max(satCost))]

    print("Additional costs for travel durations weekdays (min,mean,max):", weekRange)
    print("Additional costs for travel durations saturdays (min,mean,max):", satRange)