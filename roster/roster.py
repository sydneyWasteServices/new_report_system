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

    # Return Ratio Specific for Suez tipping per route calculation
    def suez_ratio(self, df : object):
        
        occurrence = df.groupby(['Primary_truck','Primary_route'])['Primary_driver_Name'].count().reset_index()

        total = df.groupby('Primary_truck')['Primary_route'].count().reset_index()

        merge = pd.merge(occurrence, total, on='Primary_truck', how='left')

        merge['tip_portion'] = merge.Primary_driver_Name / merge.Primary_route_y

        merge = merge[['Primary_truck', 'Primary_route_x', 'tip_portion']]

        return merge


    def salary_ratio(self, df : object):
        
        occurrence = df.groupby(['Primary_employeeID','Primary_route'])['Run_type'].count().reset_index()

        total = df.groupby('Primary_employeeID')['Run_type'].count().reset_index()

        merge = pd.merge(occurrence, total, how='left', on='Primary_employeeID')

        merge = merge.rename(columns={'Run_type_y' : 'Total'})

        merge['portion'] = merge.Run_type_x / merge.Total
        
        return merge 
        

    def toll_ratio(self, df : object):
        
        occurence = df.groupby(['Primary_truck','Primary_route'])['Primary_driver_Name'].count().reset_index()

        total = df.groupby('Primary_truck')['Primary_driver_Name'].count().reset_index()

        merge = pd.merge(occurence, total, how='left', on='Primary_truck')

        merge['portion'] = merge['Primary_driver_Name_x'] / merge['Primary_driver_Name_y']

        return merge
        

    def rego_ratio(self, df : object):

        occurence = df.groupby(['Primary_truck','Primary_route'])['Run_type'].count().reset_index()

        total = df.groupby('Primary_truck')['Primary_route'].count().reset_index()

        merge = pd.merge(occurence, total, how='left', on='Primary_truck')

        merge['portion'] = merge['Run_type'] / merge['Primary_route_y']

        return merge 