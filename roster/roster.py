import pandas as pd
import numpy as np

class Roster():
    def __init__(self):
        return

    def df_gw_runs(self, non_gw_runs: list, df : object):
        
        df = df[~df['Primary_route'].isin(non_gw_runs)]

        return df


    def rm_space(self, colName : str, df : object):

        df[colName] = df[colName].str.replace(' ','')

        return df


    def ratio(self, df : object):
        
        occurrence = df.groupby(['Primary_truck','Primary_route'])['Primary_driver_Name'].count().reset_index()

        total = df.groupby('Primary_truck')['Primary_route'].count().reset_index()

        merge = pd.merge(occurrence, total, on='Primary_truck', how='left')

        merge['tip_portion'] = merge.Primary_driver_Name / merge.Primary_route_y

        merge = merge[['Primary_truck', 'Primary_route_x', 'tip_portion']]

        return merge