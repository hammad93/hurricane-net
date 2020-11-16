''' Hammad Usmani
PURPOSE: To provide a class and API for the Official NHC Atlantic Track and 
  Intensity Forecast Errors (1970-2016, excluding depressions)
METHOD: Read the text file provided by the NOAA and NHC into a pandas DataFrame and 
  create an API for common functions and applications
OUTPUT: Forecast Error Database http://www.nhc.noaa.gov/verification/verify7.shtml
'''
import pandas as pd
import numpy as np
import datetime
from datetime import timedelta
import io

class model :
  '''
  PURPOSE: To create a class for each model included in the forecast error database
  METHOD: Provide an API
  OUTOUT: A class with a DataFrame and associated operations
  '''
  name = None
  # Dictionary key: STMID
  storm = dict()
  
  def __init__(self, model_name) :
    self.name = model_name
    return

class models :
  models = dict()
  
  '''
  PURPOSE: Initialize the Forecast Error Database
  METHOD: Read in the text file with the NHC model errors
  OUTPUT: Success / Failure dialogue
  '''
  def __init__(self, filename = "1970-present_OFCL_v_BCD5_ind_ATL_TI_errors_noTDs.txt") :
    self.parse(filename)
    return
  '''
  PURPOSE: Parse in the Forecast Error database
  METHOD: Use the forecast error file format provided by the NHC and NOAA and load into model dictionary
  OUTPUT: pandas DataFrame with appropriate data
  REFERENCES:
    [1] http://www.nhc.noaa.gov/verification/errors/1970-present_OFCL_v_BCD5_ind_ATL_TI_errors_noTDs.txt
    [2] http://www.nhc.noaa.gov/verification/pdfs/Error_Tabulation_File_Format.pdf
  '''
  def parse(self, filename = "1970-present_OFCL_v_BCD5_ind_ATL_TI_errors_noTDs.txt") :
    # Begin parsing by reading in line by line
    with open(filename) as raw :
      lines = raw.readlines()
      
      # Get model names and declare model objects
      line = lines[1].split()
      model_names = line[2:]
      for model_name in model_names :
        self.models[model_name] = model(model_name)
        
      # Data starts at line 9 
      for line in lines[9:] :
          line = line.split()
        
          # Identify atlantic storm date, storm id, associated sample sizes, latitude and longitude, and windspeed
          timestamp = datetime.datetime.strptime(line[0], "%d-%m-%Y/%H:%M:%S")
          storm_id = line[1]
          sample_sizes = {"F012": float(line[2]), "F024": float(line[3]),"F036": float(line[4]), "F048": float(line[5]), "F072": float(line[6]), "F096": float(line[7]), "F120": float(line[8]), "F144": float(line[9]), "F168": float(line[10])} 
          latitude = float(line[11])
          longitude = float(line[12])
          wind_speed = int(line[13])
        
                    
          # Iterate through model forecast track and intensity errors 
          for i in range(len(model_names)) :
            intensity_forecast = dict(list(zip([timestamp, timestamp + timedelta(hours = 12), timestamp + timedelta(hours = 24), timestamp + timedelta(hours = 36), timestamp + timedelta(hours = 48), timestamp + timedelta(hours = 72), timestamp + timedelta(hours = 96), timestamp + timedelta(hours = 120), timestamp + timedelta(hours = 144), timestamp + timedelta(hours = 168)], [None if x == "-9999.0" else float(x) for x in line[14 + (20 * i) : 24 + (20 * i)]])))
            track_forecast = dict(list(zip([timestamp, timestamp + timedelta(hours = 12), timestamp + timedelta(hours = 24), timestamp + timedelta(hours = 36), timestamp + timedelta(hours = 48), timestamp + timedelta(hours = 72), timestamp + timedelta(hours = 96), timestamp + timedelta(hours = 120), timestamp + timedelta(hours = 144), timestamp + timedelta(hours = 168)], [None if x == "-9999.0" else float(x) for x in line[24 + (20 * i) : 34 + (20 * i)]])))
            
            # Add forecast to model and storm, initialize if storm id does not exist
            if storm_id not in self.models[model_names[i]].storm.keys() :
                self.models[model_names[i]].storm[storm_id] = dict()
            self.models[model_names[i]].storm[storm_id].update({
              timestamp : {
                "sample_sizes" : sample_sizes,
                "lat" : latitude,
                "long" : longitude,
                "wind_speed" : wind_speed,
                "intensity_forecast" : intensity_forecast,
                "track_forecast" : track_forecast,
              }
            })