import numpy as np
from numpy.core.numeric import NaN
import pandas as pd
from pulp import *

np.set_printoptions(threshold=sys.maxsize)
pd.set_option("display.max_rows", None)


def load_data():
    """Returns route info from route generation in pandas dataframes.

    Parameters:
    -----------
    none

    Returns:
    --------
    Weekday_Routes : Panda dataframe
        Has info about duration, total demand, first, second, third and fourth stops of each route
    Weekend_Routes : Panda dataframe
        Has info about duration, total demand, first, second, third and fourth stops of each route
    storeLocations : Pandas dataframe
        Has info about store names and coordinates


    """
    # Read file and convert into panda dataframe
    Weekday_Routes = pd.read_csv("Weekday_Routes.csv")
    Weekend_Routes = pd.read_csv("Weekend_Routes.csv")
    storeLocations = pd.read_csv("WoolworthsDemands.csv", usecols=[0])
    return Weekday_Routes, Weekend_Routes, storeLocations


def column_generation(routeData, storeLocations):
    """Returns a matrix for constructing route location constraints in the LP.

    Parameters:
    -----------
    none

    Returns:
    --------
    routeVisits : 2d Array
        matrix where the rows are store locations and the columns are the routes. The matrix value is 1 if the route passes through
        the location and 0 if not.
    """
    # this reads demand by weekday, removes the distribution centre and sorts it to be the same order as storeLocations
    # demand_check = pd.read_csv("Demand by weekday.csv").drop(55, axis=0).sort_values("Store").reset_index(drop=True)

    firstStops = routeData.to_dict()["First Stop"]
    secondStops = routeData.to_dict()["Second Stop"]
    thirdStops = routeData.to_dict()["Third Stop"]
    fourthStops = routeData.to_dict()["Fourth Stop"]
    storeLocationDict = storeLocations.to_dict()["Store"]
    routeVisits = np.zeros((len(storeLocations), len(firstStops)))

    for i in range(len(firstStops)):
        # pulls the location number from a route number
        if pd.isna(firstStops[i]) is False:
            locationNumber = list(storeLocationDict.keys())[
                list(storeLocationDict.values()).index(firstStops[i])
            ]
            routeVisits[locationNumber][i] = 1

    for i in range(len(secondStops)):
        # pulls the location number from a route number
        if pd.isna(secondStops[i]) is False:
            locationNumber = list(storeLocationDict.keys())[
                list(storeLocationDict.values()).index(secondStops[i])
            ]
            routeVisits[locationNumber][i] = 1

    for i in range(len(thirdStops)):
        # pulls the location number from a route number
        if pd.isna(thirdStops[i]) is False:
            locationNumber = list(storeLocationDict.keys())[
                list(storeLocationDict.values()).index(thirdStops[i])
            ]
            routeVisits[locationNumber][i] = 1

    for i in range(len(fourthStops)):
        # pulls the location number from a route number
        if pd.isna(fourthStops[i]) is False:
            locationNumber = list(storeLocationDict.keys())[
                list(storeLocationDict.values()).index(fourthStops[i])
            ]
            routeVisits[locationNumber][i] = 1

    return routeVisits


def solve_lp(routeData, storeLocations, isSaturday=False):
    """Solves the mixed integer programme given routeData and .

    Parameters:
    -----------
    routeData : Pandas Dataframe
        Df of route info from route generation
    storeLocations : Pandas Dataframe
        Df of every store name and coordinates

    Returns:
    --------
    LpStatus[prob.status] : Variable
        status of the problem, should be optimal
    value(prob.objective) : Int
        value of the minimised cost
    optimalRouteData : Pandas DataFrame
        Data frame with all the route info of the chosen routes in the optimal routing plan
    """
    # this reads demand by weekday, removes the distribution centre and sorts it to be the same order as storeLocations
    demand = (
        pd.read_csv("Demand by weekday.csv")
        .drop(55, axis=0)
        .sort_values("Store")
        .reset_index(drop=True)
    )

    # create the matrix of which routes visit which locations
    routeVisits = column_generation(routeData, storeLocations)
    rows = np.shape(routeVisits)[0]

    # Get index of all route numbers for the df
    routes = routeData.index

    # Get durations and work out initial costs
    durations = routeData["Duration"]
    costs = durations.multiply(0.0625)

    # update costs to include cost of going over 4 hrs and cost of going over demand per route
    for i in range(len(durations)):
        if durations[i] > 14400:
            costs[i] += 2000
    demands = routeData["Demand"]
    for i in range(len(demands)):
        if demands[i] > 26:
            costs[i] += 2000
    # convert costs to dictionary
    costs = costs.to_dict()

    # create prob variable object for problem data
    prob = LpProblem("Routes", LpMinimize)

    # Dictionary containing route variables
    route_chosen = LpVariable.dicts("route", routes, 0, None, cat="Binary")

    # input the obj function into prob using the costs for each route
    prob += (
        lpSum([costs[i] * route_chosen[i] for i in routes]),
        "Objective cost function",
    )

    # constraint: each route only visits node once
    for i in range(rows):
        if demand.iloc[i, int(isSaturday)] != 0:
            prob += lpSum([route_chosen[b] * routeVisits[i][b] for b in routes]) == 1

    # constraint: Trucks
    prob += lpSum(route_chosen[i] for i in routes) <= 60

    ##SOLVING ROUTINES##
    prob.writeLP("Routes.lp")
    prob.solve()

    # get and store the route numbers that were chosen by the solver
    optimalRoutes = []
    for v in prob.variables():
        if v.varValue == 1:
            optimalRoutes.append(int(str(v.name).replace("route_", "")))

    # Use the route numbers to pull the correponding route data and append it to an empty df to display.
    optimalRouteData = pd.DataFrame(columns=routeData.columns)
    optimalRouteData = routeData.loc[np.r_[optimalRoutes]]

    return LpStatus[prob.status], value(prob.objective), optimalRouteData


if __name__ == "__main__":

    Weekday_Routes, Weekend_Routes, storeLocations = load_data()

    # UNCOMMENT THE ONE YOU WANT TO SOLVE
    # status, minimisedCost, routes = solve_lp(Weekday_Routes, storeLocations)
    status, minimisedCost, routes = solve_lp(Weekend_Routes, storeLocations, True)

    print("Status: ", status)
    print("Minimal Cost: ", minimisedCost)
    print("Routes: \n", routes)
