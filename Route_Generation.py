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

def group_locations(coordinates):
    ''' Groups the store locations into defined groups

        Parameters:
        -----------
        coordinates : Panda dataframe
            Dataframe of all stores
        Returns:
        --------
        south : Panda dataframe
            Dataframe of stores with latitude less than distribution centre
        east : Panda dataframe
            Dataframe of stores with longitude less than distribution centre
            and latitude greater than distribution centre
        west : Panda dataframe
            Dataframe of stores with longitude greater than distribution centre
            and latitude greater than distribution centre
    '''

    # Hardcoded coordinates for distribution centre latitude and longitude
    distributionLat = -36.94904179
    distributionLong = 174.8080123

    south = coordinates.loc[coordinates["Lat"] < distributionLat]
    
    # east and west dataframes derived from "north" dataframe
    north = coordinates.loc[coordinates["Lat"] > distributionLat]
    east = north.loc[north["Long"] > distributionLong]
    west = north.loc[north["Long"] < distributionLong]

    return south, east, west


if __name__ == "__main__":
    durations, coordinates = load_data()

    south, east, west = group_locations(coordinates)