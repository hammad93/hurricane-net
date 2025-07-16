import pandas as pd
import numpy as np
import datetime
import io
import sys
import logging

class data :
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format="hurricane_net %(asctime)s - %(levelname)s - %(name)s - %(message)s")
    def __init__(self, q = 'all', link = "https://www.ncei.noaa.gov/data/international-best-track-archive-for-climate-stewardship-ibtracs/v04r01/access/csv/ibtracs.ALL.list.v04r01.csv") :
        '''
        Input
        -----
        q String
            The string with the filter identifier
        link String
            The URL for the CSV. The default value is the IBTrACS database in the references
        References
        ----------
          - https://www.ncei.noaa.gov/data/international-best-track-archive-for-climate-stewardship-ibtracs/v04r01/access/csv/
          - https://www.ncei.noaa.gov/products/international-best-track-archive
        '''
        logging.info(f'Loading data with link for {link.split("/")[-1]}')
        self.all_storms = pd.read_csv(link, na_filter=False, dtype=str)
        logging.info('Loading complete. hn.data.all_storms available')
        self.filter(q) # creates self.storms

    def filter(self, q):
        '''
        BASIN
        NA - North Atlantic
        EP - Eastern North Pacific
        WP - Western North Pacific
        NI - North Indian
        SI - South Indian
        SP - Southern Pacific
        SA - South Atlantic

        USA_STATUS
        DB - disturbance,
        TD - tropical depression, TS - tropical storm,
        TY - typhoon,
        ST - super typhoon,
        TC - tropical cyclone,
        HU, HR - hurricane,
        SD - subtropical depression, SS - subtropical storm,
        EX - extratropical systems, PT - post tropical,
        IN - inland,
        DS - dissipating,
        LO - low,
        WV - tropical wave,
        ET - extrapolated,
        MD - monsoon depression, XX - unknown.

        References
        ----------
          - https://www.ncei.noaa.gov/sites/g/files/anmtlf171/files/2025-04/IBTrACS_v04r01_column_documentation.pdf
        '''
        if q == 'all':
            self.storms = self.all_storms
            logging.info('hn.data.storms has all available storms.')
        elif q in ['NA', 'EP', 'SI', 'SP', 'SA']:
            self.storms = self.all_storms[self.all_storms['BASIN'] == q]
            logging.info(f'hn.data.storms set to {q} basin.')
        elif q == 'hurricanes':
            # get Atlantic storms
            self.atlantic_storms = self.all_storms[self.all_storms['BASIN'] == 'NA']
            logging.info('hn.data.atlantic_storms now available.')
            hurricane_ids = set(self.atlantic_storms[self.atlantic_storms['USA_STATUS'].isin(['HU', 'HR'])]['SID'])
            self.hurricanes = self.atlantic_storms[self.atlantic_storms['SID'].isin(hurricane_ids)]
            logging.info('hn.data.hurricanes now available. Filter USA_STATUS column where hurricane records are HU, HR')
            self.storms = self.all_storms[self.all_storms['BASIN'] == 'NA'][self.all_storms['USA_STATUS'].isin(['HU', 'HR'])]
            logging.info('hn.data.storms to hurricanes')