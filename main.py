import pandas as pd 
import numpy as np
import typing
from functools import reduce
import operator
import xlwings as xw


from report_data.routes_list import By_Revenue_type


from raw_data_transformation.cleaner import Cleaner
from raw_data_transformation.filter import Filter
from raw_data_transformation.incomes import Incomes
from raw_data_transformation.transform_date import Transform_date
from raw_data_transformation.resmpleDf import ResampleDf

from tip.waste_edge_tip import Waste_edge_tip

from report_data.general_waste_info import General_waste_info


# Class feature for lcating rotue header
from report_outlook.locator import Locator


# Data info objects
from report_data.route_info import Route_info

# Roster
from roster.roster import Roster


CURRENT_WEEK = '18th_2021'

BOOKING_PATH = f'D:\\Run Analysis\\BLOB_STORAGE\\booking_weekly\\{CURRENT_WEEK}.csv'

TIPPING_PATH = f'D:\\Run Analysis\\BLOB_STORAGE\\tipping_weekly\\waste_edge_tipping\\{CURRENT_WEEK}.csv'

SUEZ_PATH = f'D:\\Run Analysis\\BLOB_STORAGE\\og_tipping_suez\\weekly\\{CURRENT_WEEK}.csv'

# Excel
ROSTER_PATH = f'D:\\Run Analysis\\BLOB_STORAGE\\Roster\\weekly_roster_processed\\{CURRENT_WEEK}.xlsx'

# Excel
SALARY_PATH = 'D:\\Run Analysis\\BLOB_STORAGE\\Drivers_pay\\paysheet_17th_2021.xlsx'

VISY_PATH = ''

r_types = [
    # 'TOTAL', 
    # 'TOTAL_EXCL_SUBCON', 
    'GENERAL_WASTE', 
    'COMINGLE',
    'CARDBOARD',
    'UOS'
    # 'SUBCONTRACTED'
]

gw = sorted(By_Revenue_type['GENERAL_WASTE'].value)
cm = sorted(By_Revenue_type['COMINGLE'].value)
cb = sorted(By_Revenue_type['CARDBOARD'].value)
uos = sorted(By_Revenue_type['UOS'].value)

NON_GW_ROUTE = ['APR', 'FLP', 'HYG', 'RED', 'RL5', 'RL6', 'RL8', 'RLP', 'RLR', 'SWP','CBK', 'RLC', 'RLG', 'DOY','NEPCB','UOSCB','CMDCB','CUMCB']

booking_df = pd.read_csv(BOOKING_PATH, dtype={"Schd Time Start": str, "PO": str})

# Cleaning and Transform Dataframe 
# Booking
# =====================================
booking_df = Cleaner().cleanNsplit_routes(booking_df, 'Route number')

booking_df = Transform_date().datify(booking_df, 'Date', '%d/%m/%y')

booking_df = Transform_date().indexitfy(booking_df, 'Date')

booking_df = Filter().confirmed_only(booking_df)
# =====================================
# resampled - so get group key first, then get df group 
booking_df = ResampleDf().resample_weekly(booking_df)

booking_df = ResampleDf().get_first_group(booking_df)

# Filter Non Confirm rows

booking_df = Filter().confirmed_only(booking_df)

# Cleaning and Transform Dataframe 
# Waste Edge Tipping 
# ==============================================
we_tipping_df = pd.read_csv(TIPPING_PATH)

we_tipping_df = Cleaner().cleanNsplit_routes(we_tipping_df, 'Route No')

we_tipping_df = Transform_date().datify(we_tipping_df, 'Route Date', '%d-%b-%Y')

we_tipping_df = Transform_date().datify(we_tipping_df, 'Disposal Date', '%d-%b-%Y')

we_tipping_df = Waste_edge_tip().filter(we_tipping_df)

all_route_waste_edge_tip = Waste_edge_tip().route_tip(we_tipping_df)

# Clean Roster DataFrame   
# ==============================================

df_ros = pd.read_excel(ROSTER_PATH)

df_ros = Roster().rm_space('Primary_truck', df_ros)

df_gw_ros = Roster().df_gw_runs(NON_GW_ROUTE, df_ros)

df_gw_ratio = Roster().ratio(df_ros)

print(df_gw_ratio)
# ==============================================



# Insert info into route income objects

ROUTE_INFO_LIST = {}

all_route_income_name = Incomes().all_route_income(booking_df)


# Populate income into ROUTE_INFO_LIST
for name in all_route_income_name.index:
    ROUTE_INFO_LIST[name] = Route_info(name)
    ROUTE_INFO_LIST[name].income = all_route_income_name[name]

# Populate Waste Edge Weight Only GW CM CB

# Populate Suez Tipping

for name in all_route_waste_edge_tip.index:

    if name in gw:

        ROUTE_INFO_LIST[name].gw_waste_edge_weight = all_route_waste_edge_tip[name]
                
    elif name in cm:

        ROUTE_INFO_LIST[name].cm_waste_edge_weight = all_route_waste_edge_tip[name]
        
    elif name in cb:

        ROUTE_INFO_LIST[name].cb_waste_edge_weight = all_route_waste_edge_tip[name]
    
    # UOS runs - Mixed with GW CM CB => split the actual weight 

     
# Actual From Suez Tip 






# # ====================================================================
# # General Waste Info process 


# gw_total_income = Incomes().types_income(booking_df, gw)

# gw_route_income_table = Incomes().routes_income(booking_df, gw)

# gw_routes_number = list(gw_route_income_table['Route number'])

# gw_routes_income = list(gw_route_income_table['Price'])

# # General Waste Rotue Header start at
# # Row 4 Column 12  

# wb = xw.Book()

# START_GW_ROUTE_HEADER_ROW = 4

# START_GW_ROUTE_HEADER_COL = 12






# # Total Sheet
# # =================================================
# wb.sheets[0].name = 'Total'

# # =================================================

# wb.sheets[0].range((START_GW_ROUTE_HEADER_ROW,START_GW_ROUTE_HEADER_COL)).value = gw_routes_number

# gw_total_route_addresses = Locator().get_route_header_address(wb, 0,START_GW_ROUTE_HEADER_ROW,START_GW_ROUTE_HEADER_COL)

# gw_info = General_waste_info(gw_total_income, gw_routes_income, gw_total_route_addresses)


# print(gw_info.address_in_total_sheet)

