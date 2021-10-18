import numpy as np
from pulp import *
from Woolworths_LP import *
import statistics as stats
import matplotlib.pyplot as plt
import scipy.stats as st
def travelsimulation(routesWeek, routesSat):
    """
    
    Simulates the travel times 1000 times to show the range of costs

    Parameters:
    ----------
    routesWeek: Pandas Dataframe
                Contains the routes for weekdays: demand, total duration
    routesSat: Pandas Dataframe
                Contains the routes for Saturdays: demand, total duration
    
    Returns:
    ----------
    weekRange: array
                In form of (minimum, mean, maximum) for Weekdays costs
    satRange: array
                In form of (minimum, mean, maximum) for Saturday costs
    
    """
    # obtain the optimal durations found for both weekdays and saturdays
    weekDuration = routesWeek.loc[:,'Duration']
    satDuration = routesSat.loc[:,'Duration']

    # convert to an array to calculate
    weekDuration = weekDuration.values
    satDuration = satDuration.values

    # obtain the demands for both weekdays and saturdays
    weekDemand = routesWeek.loc[:,'Demand']
    satDemand = routesSat.loc[:,'Demand']

    # convert to an array to calculate
    weekDemand = weekDemand.values
    satDemand = satDemand.values

    # subtract the loading time as it is irrelevant to the travel durations
    weekDuration = weekDuration-(7.5*60*weekDemand)
    satDuration = satDuration-(7.5*60*satDemand)

    # initialise
    weekCost = [0] * 1000
    satCost = [0] * 1000
    simulations = [0] * 1000

    # our estimated random distribution: lognormal
    mu = 0.03 
    sigma = 0.07
    np.random.seed(100)      # seed for random distribution
    random = np.random.lognormal(mu, sigma, 1000)

    for j in range(len(simulations)):

        # multiply by the random factor generated from the random lognormal distribution

        weekRandom = weekDuration * random[j]
        satRandom = satDuration * random[j]

        # add back the loading times
        weekRandom = weekRandom + (7.5*60*weekDemand)
        satRandom = satRandom + (7.5*60*satDemand)

        # convert to hours
        weekRandom = weekRandom/(60*60)
        satRandom = satRandom/(60*60)

        # convert to costs
        for i in range(len(weekRandom)):
            if weekRandom[i] < 4:
                weekRandom[i] = weekRandom[i] * 225
            else:
                overtime = weekRandom[i]-4      # overtime costs
                weekRandom[i] = (weekRandom[i] * 225) + (overtime * 275)

        for i in range(len(satRandom)):
            if satRandom[i] < 4:
                satRandom[i] = satRandom[i] * 225
            else:
                overtime = satRandom[i]-4       # overtime costs
                satRandom[i] = (satRandom[i] * 225) + (overtime * 275)

        # sum of costs of routes for current simulation 
        weekCost[j] = sum(weekRandom)
        satCost[j] = sum(satRandom)

    # obtain the minimum, mean and the maximum costs after 1000 simulations
    weekRange = [(min(weekCost),stats.mean(weekCost),max(weekCost))]
    satRange = [(min(satCost),stats.mean(satCost),max(satCost))]
    

    # Displays histograms of the logistic plan costs
    plt.hist(weekCost, 20, density=True, align='mid')
    #plt.show()
    plt.hist(satCost, 20, density=True, align='mid')
    #plt.show()


    # Confidence interval calculator 
    weekdayInterval = st.lognorm.interval(alpha = 0.95, loc = np.mean(weekCost), scale = st.sem(weekCost))
    saturdayInterval = st.lognorm.interval(alpha = 0.95, loc = np.mean(satCost), scale = st.sem(satCost))
    print("95% Confidence Interval for weekdays", weekdayInterval)
    print("95% Confidence Interval for saturdays", saturdayInterval)
    
    return weekRange, satRange


if __name__ == "__main__":
    # load data
    Weekday_Routes, Weekend_Routes, storeLocations = load_data()

    # find the optimal routes using LP
    routesWeek = solve_lp(Weekday_Routes, storeLocations)[2]
    routesSat = solve_lp(Weekend_Routes, storeLocations, True)[2]

    # enter routes to travel simulator
    weekRange, satRange = travelsimulation(routesWeek, routesSat)

    # print minimum, mean, and maximum
    print("Costs for travel durations weekdays (min,mean,max):", weekRange)
    print("Costs for travel durations saturdays (min,mean,max):", satRange)



