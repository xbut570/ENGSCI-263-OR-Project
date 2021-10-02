import numpy as np
import pandas as pd

travelDurationFile = "WoolworthsTravelDurations.csv"
locationFile = "WoolworthsLocations.csv"

def load_data():
    ''' Returns travel durations and coordinates for stores.

        Parameters:
        -----------
        none

        Returns:
        --------
        travelDurations : Panda dataframe
            Vector of times (years) at which measurements were taken.
        coordinates : Panda dataframe
            Vector of copper measurements

    '''
    
    # Read files and convert into panda dataframes
    travelDurations = pd.read_csv(travelDurationFile)
    coordinates = pd.read_csv(locationFile)

    return travelDurations, coordinates


def group_coordinates(coordinates):
    ''' Groups the store locations into predefined groups

        Parameters:
        -----------
        coordinates : Panda dataframe
            Dataframe of all stores
        Returns:
        --------
        southLocations : List
            List of stores with latitude less than distribution centre
        eastLocations : List
            List of stores with longitude less than distribution centre
            and latitude greater than distribution centre
        westLocations : List
            List of stores with longitude greater than distribution centre
            and latitude greater than distribution centre
    '''

    # Hardcoded coordinates for distribution centre latitude and longitude
    distributionLat = -36.94904179
    distributionLong = 174.8080123

    # Creatie sub-data frames based off of sections
    southCoordinates = coordinates.loc[coordinates["Lat"] < distributionLat]
    northCoordinates = coordinates.loc[coordinates["Lat"] > distributionLat]
    eastCoordinates = northCoordinates.loc[northCoordinates["Long"] > distributionLong]
    westCoordinates = northCoordinates.loc[northCoordinates["Long"] < distributionLong]

    # Create lists of stores in each section
    southLocations = southCoordinates["Store"].tolist()
    eastLocations = eastCoordinates["Store"].tolist()
    westLocations = westCoordinates["Store"].tolist()

    return southLocations, eastLocations, westLocations


def two_stop_route_generation(durations, locations, finalStop):
    ''' Generates two stop routes between a given location and the closet location
        (As well as too and from the distribution center)
        
        Parameters:
        -----------
        durations : Panda dataframe
            Dataframe of travel times between each location
        locations : list
            List of locations to visit
        finalStop : Boolean
            Boolean equalling true if this is the last stop in the route
            (If not true, the return distance to the distribution centre will not be 
            included in the duration)
        Returns:
        --------
        routes : Panda dataframe
            Dataframe containing the route length, and stops visited
    '''    
    # Defines shape of array
    rows, cols = durations.shape

    # Hardcoded location of distribution center in table
    distributionVal = 55

    # Creates empty panda dataframe
    routes = pd.DataFrame(data = None, index = None, columns = ['Duration','First Stop', 'Second Stop'])

    # Iterates through each inputted location and finds the shortest route to the location, then the distance
    # to the next closest location
    for location in locations:
        minDistance = 1.e10
        nextStop = ""        
        for i in range(0,rows):
            if(location == durations.iloc[i,0]):
                for j in range(1, cols):
                    if (durations.iloc[i,j] < minDistance) and (durations.iloc[i,j] > 0):
                        minDistance = durations.iloc[i,j] 
                        distanceTo = durations.iloc[distributionVal,i + 1]
                        distanceFrom = durations.iloc[j - 1,distributionVal + 1]
                        nextStop = durations.iloc[j - 1,0]
        
        # If this is the final stop in the route the return distance to the distribution is added
        if(finalStop):
            totalDistance = minDistance + distanceTo + distanceFrom
        else:
            totalDistance = minDistance + distanceTo
        
        # Adds new route into the overall panda dataframe for output
        newRoute = pd.DataFrame({'Duration': totalDistance, 'First Stop' : location, 'Second Stop' : nextStop}, index = ['1'])
        routes = pd.concat([routes, newRoute], ignore_index = True)

    return routes

def three_stop_route_generation(durations, locations, finalStop):
    ''' Generates three stop routes between a given location and the closet location,
        this is then routed to the next closest location
        (As well as too and from the distribution center)
        
        Parameters:
        -----------
        durations : Panda dataframe
            Dataframe of travel times between each location
            (If not true, the return distance to the distribution centre will not be 
            included in the duration)
        locations : list
            List of locations to visit
        finalStop : Boolean
            Boolean equalling true if this is the last stop in the route
        Returns:
        --------
        routes : Panda dataframe
            Dataframe containing the route length, and stops visited
    '''   
    # Calls the two_stop_route_generation function to create the first stops of the route
    two_stop_routes = two_stop_route_generation(durations, locations, False)
    
    # Parses data outputted from the two_stop_route_generation dataframe into arrays
    first_stops = two_stop_routes["First Stop"].values
    second_stops = two_stop_routes["Second Stop"].values
    currentDuration = two_stop_routes["Duration"].values
    
    # Defines shape of array    
    rows, cols = durations.shape

    # Hardcoded location of distribution center in table
    distributionVal = 55
    
    # Creates empty panda dataframe
    routes = pd.DataFrame(columns = ['Duration','First Stop', 'Second Stop', 'Third Stop'])

    # Iterates through each second stop in the route and finds the shortest route to the 
    # location, then the distance to the next closest location excluding the first stop
    for i in range(0,len(second_stops)):
        minDistance = 1.e10
        nextStop = ""
        for j in range(0,rows):
            if (second_stops[i] == durations.iloc[j,0]):
                for k in range(1,cols):
                    if(durations.iloc[j,k] < minDistance) and (durations.iloc[j,k] > 0) and (durations.iloc[k-1,0] != first_stops[i]):
                        minDistance = durations.iloc[j,k]
                        distanceFrom = durations.iloc[k - 1,distributionVal + 1]
                        nextStop = durations.iloc[k - 1,0]                        
        
        # If this is the final stop in the route the return distance to the distribution is added        
        if(finalStop):
            totalDistance = minDistance + currentDuration[i] + distanceFrom
        else:
            totalDistance = minDistance + currentDuration[i]   

        # Adds new route into the overall panda dataframe for output           
        newRoute = pd.DataFrame({'Duration': totalDistance, 'First Stop' : first_stops[i], 'Second Stop' : second_stops[i], 'Third Stop' : nextStop}, index = ['1'])
        routes = pd.concat([routes, newRoute], ignore_index = True)

    return routes

if __name__ == "__main__":
    
    #VARIOUS TEST CONDITIONS NOT FINALIZED
    durations, coordinates = load_data()

    south, east, west = group_coordinates(coordinates)

    southRoutes = three_stop_route_generation(durations, south, True)
    eastRoutes = three_stop_route_generation(durations, east, True)
    westRoutes = three_stop_route_generation(durations, west, True)

    print(southRoutes)
    print("\n")
    print(eastRoutes)
    print("\n")
    print(westRoutes)

    south2 = two_stop_route_generation(durations, south, True)
    test = pd.concat([south2, southRoutes], ignore_index = True)

    print("\n")
    print(test)