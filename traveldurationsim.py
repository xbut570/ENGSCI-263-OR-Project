import numpy as np
from pulp import *
from Woolworths_LP import *
import statistics as stats

# load data
Weekday_Routes, Weekend_Routes, storeLocations = load_data()

# find the optimal routes
routesWeek = solve_lp(Weekday_Routes, storeLocations)[2]
routesSat = solve_lp(Weekend_Routes, storeLocations, True)[2]

# optain the optimal durations found for both weekdays and saturdays
weekDuration = routesWeek.loc[:,'Duration']
satDuration = routesSat.loc[:,'Duration']

 # convert to an array to calculate
weekDuration = weekDuration.values
satDuration = satDuration.values

# subtract the loading time as it is irrelevant to the travel durations
weekDuration = weekDuration-(7.5*60)
satDuration = satDuration-(7.5*60)

weekCost = [0] * 1000
satCost = [0] * 1000
simulations = [0] * 1000

for j in range(len(simulations)):

    # multiply by the random factor generated from the random lognormal distribution
    mu = 0.03 
    sigma = 0.07

    random = np.random.lognormal(mu, sigma)
    weekRandom = weekDuration * random
    satRandom = satDuration * random

    # add back the loading times
    weekRandom = weekRandom + (7.5*60)
    satRandom = satRandom + (7.5*60)

    # convert to hours
    weekRandom = weekRandom/(60*60)
    satRandom = satRandom/(60*60)

    # convert to costs
    for i in range(len(weekRandom)):
        if weekRandom[i] < 4:
            weekRandom[i] = weekRandom[i] * 225
        else:
            overtime = weekRandom[i]-4
            weekRandom[i] = (weekRandom[i] * 225) + (overtime * 275)

    for i in range(len(satRandom)):
        if satRandom[i] < 4:
            satRandom[i] = satRandom[i] * 225
        else:
            overtime = satRandom[i]-4
            satRandom[i] = (satRandom[i] * 225) + (overtime * 275)


    weekCost[j] = sum(weekRandom)
    satCost[j] = sum(satRandom)

weekRange = [(min(weekCost),stats.mean(weekCost),max(weekCost))]
satRange = [(min(satCost),stats.mean(satCost),max(satCost))]

print(weekRange)
print(satRange)