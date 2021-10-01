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
    
    travelDurations = pd.read_csv(travelDurationFile)
    coordinates = pd.read_csv(locationFile)

    return travelDurations, coordinates

def group_coordinates(coordinates):
    ''' Groups the store locations into defined groups

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



def two_stop_route_generation(durations, locations):
    ''' Generates two stop routes between a given location and the closet location
        (As well as too and from the distribution center)
        
        Parameters:
        -----------
        durations : Panda dataframe
            Dataframe of travel times between each location
        locations : list
            List of locations to visit
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
    routes = pd.DataFrame(columns = ['Duration','First Stop', 'Second Stop'])

    # Iterates through each inputted location and finds the shortest route to the location, then the distance
    # to the next closest location, followed by the distance back to the distribution center
    for location in locations:
        minDistance = 1.e10
        nextStop = ""        
        for i in range(0,rows):
            if(location == durations.iloc[i,0]):
                for j in range(1, cols - 1):
                    if (durations.iloc[i,j] < minDistance) and (durations.iloc[i,j] > 0):
                        minDistance = durations.iloc[i,j] 
                        distanceTo = durations.iloc[distributionVal,i + 1]
                        distanceFrom = durations.iloc[j - 1,distributionVal + 1]
                        nextStop = durations.iloc[j - 1,0]
        # Adds new route into the overall panda dataframe for output
        newRoute = pd.DataFrame({'Duration': (minDistance + distanceTo + distanceFrom), 'First Stop' : location, 'Second Stop' : nextStop}, index = ['1'])
        routes = pd.concat([routes, newRoute], ignore_index = True)
    return routes


if __name__ == "__main__":
    durations, coordinates = load_data()

    south, east, west = group_coordinates(coordinates)

    southRoutes = two_stop_route_generation(durations, south)
    eastRoutes = two_stop_route_generation(durations, east)
    westRoutes = two_stop_route_generation(durations, west)

   # print(southRoutes, eastRoutes, westRoutes)