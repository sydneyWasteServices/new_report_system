import pandas as pd
import numpy as np 

class Suez_tip():
    def __init__(self):
        return

    def allocation(self, df_ros_ratio : object, df_suez : object):

        df_suez = df_suez.groupby(['Rego'])[['Net (t)','total_price']].sum().reset_index()

        weekly_tipping = pd.merge(df_ros_ratio, df_suez, how='left', left_on='Primary_truck', right_on='Rego')
        

        return 

    # def uos_tip

