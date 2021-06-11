import pandas as pd
import numpy as np
import glob


class Mv_expense():
    def __init__(self):
        return

    def ratio(
            self,
            PATH_CURRENT_WEEK : str, 
            PATH_ALLROSTER : str):
           
                
        df_all_ros = pd.concat(map(pd.read_excel, glob.glob(f'{PATH_ALLROSTER}\\*.xlsx')))

        df_curr_week = pd.read_excel(PATH_CURRENT_WEEK)

        df_mvexp = pd.read_excel(PATH_MVEXP)

        df_all_ros.Primary_truck = df_all_ros.Primary_truck.str.replace(' ','')

        # Only select the Route that Current week Roster has  
        curr_wk_route = df_curr_week.Primary_route.unique()

        # Plus All the Satellie route
        curr_wk_satRoute = df_curr_week[df_curr_week.Satellite_Route_1.notnull()].Satellite_Route_1.unique()   

        # Join 2 routes together 
        all_curr_routes = np.append(curr_wk_route, curr_wk_satRoute)

        # Clean the ?????? in Primary Route
        df_all_ros = df_all_ros[df_all_ros.Primary_route.isin(all_curr_routes) & df_all_ros.Primary_truck.ne('??????')]      

        occurrence = df_all_ros.groupby(['Primary_truck','Primary_route'])['Run_type'].count().reset_index()   

        total = df_all_ros.groupby('Primary_truck')['Run_type'].count().reset_index() 

        table_ratio = pd.merge(occurrence, total, how='left', on='Primary_truck') 

        table_ratio['portion'] = table_ratio.Run_type_x / table_ratio.Run_type_y
        # Display
        table_ratio = table_ratio[['Primary_truck', 'Primary_route', 'portion']]

        return table_ratio



    def allocation(
        self, 
        df_mvexp : object ,
        ratio_table : object):
        
        mv_exp_table = df_mvexp.groupby(['catID','Job No.'])['Debit'].sum().reset_index()

        merge = pd.merge(mv_exp_table, ratio_table, how='left', left_on='Job No.',right_on='Primary_truck') 

        merge['amount_portion'] = merge.Debit * merge.ratio

        merge = merge.groupby(['catID','Primary_route'])['amount_portion'].sum().reset_index().sort_values('catID')

        return merge


    # Allocation 