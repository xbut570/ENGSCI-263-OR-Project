import numpy as np
import pandas as pd
import random
from Woolworths_LP import *
import statistics as stats

np.set_printoptions(threshold=sys.maxsize)
pd.set_option("display.max_rows", None)

simulations = 1000


def load_data():
    """Returns travel durations and coordinates for stores.

    Parameters:
    -----------
    none

    Returns:
    --------
    travelDurations : Panda dataframe
        Vector of times (years) at which measurements were taken.
    coordinates : Panda dataframe
        Vector of copper measurements

    """

    # Read files and convert into panda dataframes
    Weekday_Routes = pd.read_csv("Weekday_Routes.csv")
    Weekend_Routes = pd.read_csv("Weekend_Routes.csv")
    storeLocations = pd.read_csv("WoolworthsDemands.csv", usecols=[0])
    demand = pd.read_csv("Formatted Demands.csv")

    return Weekday_Routes, Weekend_Routes, storeLocations, demand


def demand_simulator(routes, demand, isSaturday):
    """Calculates the demand for inputted routes, randomly decided to use 1 of the
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
    weekdaySolved["Demand"] = 0

    # Loops through each of the routes adding their demand, and the time taken to unload packages
    # (which is based off of demand)
    # Stops searching once the correct demand is found and does not check nans
    for i in range(0, rows):
        for j in range(2, 6):
            currentStore = routes.iloc[i, j]
            if not pd.isna(currentStore):
                for k in range(0, demandRows):
                    if currentStore == demand.iloc[k, 0]:
                        demandCol = random.randint(demandColMin, demandColMax)
                        routes.iloc[i, 1] += demand.iloc[k, demandCol]
                        
    return routes


def demand_evaluator(routes, minCost):
    # Defines shape of arrays
    rows, cols = routes.shape

    for i in range(0,rows):
        if routes.iloc[i,1] > 26:
            minCost += 2000
    
    return minCost

if __name__ == "__main__":
    # find the optimal routes
    Weekday_Routes, Weekend_Routes, storeLocations, demand = load_data()
    
    status, weekdayMinCost, weekdaySolved = solve_lp(Weekday_Routes, storeLocations)
    status, satMinCost, satSolved = solve_lp(Weekend_Routes, storeLocations, True)

    weekdayCost = [weekdayMinCost] * simulations
    satCost = [satMinCost] * simulations

    for i in range(0,simulations):
        simulationWeekday = demand_simulator(weekdaySolved, demand, False)
        weekdayCost[i] = demand_evaluator(simulationWeekday, weekdayMinCost)
        simulationSat = demand_simulator(satSolved, demand, True)
        satCost[i] = demand_evaluator(simulationSat, satMinCost)

weekRange = [(min(weekdayCost),stats.mean(weekdayCost),max(weekdayCost))]
satRange = [(min(satCost),stats.mean(satCost),max(satCost))]

print("Costs for travel durations weekdays (min,mean,max):", weekRange)
print("Costs for travel durations saturdays (min,mean,max):", satRange)