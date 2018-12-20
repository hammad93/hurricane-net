''' Hammad Usmani
PURPOSE: To provide a class and API for the HURDAT2 database
METHOD: Read the text file provided by the NOAA and NHC into a pandas DataFrame and
  create an API for common functions and applications.
INPUT: HURDAT2 database http://www.nhc.noaa.gov/data/#hurdat
'''
import pandas as pd
import numpy as np
import datetime
import io

class hurdat2 :
    hurricanes = pd.DataFrame()
    
    '''
    PURPOSE: Initialize the HURDAT2 API class
    METHOD: Read in the text file with the NHC data into hurricanes DataFrame
    OUTPUT: Success / Failure dialogue
    '''
    def __init__(self, filename = "hurdat2.txt") :
        self.hurricanes = self.parse(filename)
        return
    '''
    PURPOSE: Parse in HURDAT2 database
    METHOD: Use the HURDAT2 format provided by the NHC and NOAA
    OUTPUT: pandas DataFrame with appropriate data
    REFERENCES:
        [1] http://www.nhc.noaa.gov/data/hurdat/hurdat2-format-atlantic.pdf
    '''
    def parse(self, filename = "/hurdat2.txt", encoding="utf-8") :
        db = []
        
        # Begin parsing by reading in line by line
        with open(filename) as raw :
            for line in raw :
                line = line.replace(' ', '').split(',')

                # Identify atlantic storm, first 2 letters should be AL
                if (line[0][:2] == 'AL') :
                    storm_id = line[0]
                    storm_name = line[1]
                    storm_entries = line[2]

                    # Iterate and read through best track entries
                    for i in range(int(storm_entries)) :
                        entry = raw.readline().replace(' ', '').split(',')
                        # Filter -999 placeholder for missing central pressure
                        entry = [None if x == "-999" else x for x in entry]
                        # Construct date and time based on first two columns
                        timestamp = datetime.datetime(int(entry[0][:4]), int(entry[0][4:6]), int(entry[0][6:8]), int(entry[1][:2]), int(entry[1][3:]))
                        # Add entry into our current database
                        db.append([storm_id, storm_name, timestamp] + entry[2:-1])
                else :
                    print("Error, unidentified storm ".join(str(line[0])))

        # Return DataFrame
        return pd.DataFrame(db, columns = ['storm_id', 'storm_name', 'entry_time', 'entry_id', 'entry_status', 'lat', 'long','max_wind', 'min_pressure', '34kt_ne', '34kt_se', '34kt_sw', '34kt_nw', '50kt_ne', '50kt_se', '50kt_sw', '50kt_nw', '64kt_ne', '64kt_se', '64kt_sw', '64kt_nw'])
