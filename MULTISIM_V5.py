
# coding: utf-8

# In[410]:

import pandas as pd
import numpy as np
import os
import glob
import itertools as it

pd.set_option('display.float_format', lambda x: '%.1f' % x)


# In[411]:

table = {}
#files
files = glob.glob("D:/MULTISIM_CHECK/rawdata_2/*.txt")
#db
#db = ['']
for index, elem in enumerate(files):
    #files
    name = elem.split('\\', 1)[1].split('.', 1)[0]
    table[name] = pd.read_csv(elem)
print(table.keys())
#dict_keys(['ALL_MDS', 'CDR_2SIM_CALL_INT', 'CDR_2SIM_DIALING_CALL', 
#'CDR_2SIM_LOCATION_INT_02_WITHMI', 'CDR_3SIM_CALL_INT', 'CDR_3SIM_DIALING_CALL', 'CDR_3SIM_LOCATION_INT_02_WITHMI'])


# In[412]:

base_mds = table['ALL_MDS']
all_multi_base = base_mds.query('PTY_CBU_PO_CNT > 1 and SUBSCR_STATUS_CODE == "A" and DORMANT_MONTH_CNT_MKT < 2 and TENURE_SCV >= 3 and RPS_NAME == "CONSUMER MOBILITY"')


# In[413]:

multi_base = base_mds.query('SUBSCR_STATUS_CODE == "A" and DORMANT_MONTH_CNT_MKT < 2 and TENURE_SCV >= 3 and PTY_CBU_PO_CNT > 1 and PTY_CBU_PO_CNT < 4 and RPS_NAME == "CONSUMER MOBILITY"')
multi_base = multi_base[['DW_PARTY_ID', 'MINING_DW_SUBSCR_NO','PTY_CBU_PO_CNT','CUST_TYPE']]
multi_base = multi_base.sort_values(['DW_PARTY_ID'])
multi_base.head(5)


# In[414]:

party_cust_type = pd.DataFrame(multi_base.groupby(['DW_PARTY_ID'])['CUST_TYPE'].apply(list).reset_index()).rename(columns={'CUST_TYPE': 'PARTY_CUST_TYPE'})
party_cust_type.head(5)


# In[415]:

multi_sims_base = pd.merge(multi_base.iloc[:,0:-1], party_cust_type, how='left', on=['DW_PARTY_ID'])
multi_sims_base['SEGMENT_TYPE'] = 0
multi_sims_base.shape


# In[416]:

multi_sims_base['REAL_PTY_CBU_PO_CNT'] =  multi_sims_base['PARTY_CUST_TYPE'].str.len()


# In[417]:

single_sims = multi_sims_base.query('REAL_PTY_CBU_PO_CNT == 1')
two_sims = multi_sims_base.query('REAL_PTY_CBU_PO_CNT == 2')
three_sims = multi_sims_base.query('REAL_PTY_CBU_PO_CNT == 3')


# In[418]:

single_sims.shape


# In[419]:

two_sims.shape


# ### change mds table structure to similar with other table for join purpose

# In[420]:

two_sims['variable'] = ["MINING_DW_SUBSCR_NO_A","MINING_DW_SUBSCR_NO_B"]*int(len(two_sims)/2)


# In[421]:

base_two_sims = two_sims.pivot(index='DW_PARTY_ID', columns='variable', values='MINING_DW_SUBSCR_NO').reset_index()


# In[422]:

three_sims['variable'] = ["MINING_DW_SUBSCR_NO_A","MINING_DW_SUBSCR_NO_B", "MINING_DW_SUBSCR_NO_C"]*int(len(three_sims)/3)


# In[423]:

base_three_sims = three_sims.pivot(index='DW_PARTY_ID', columns='variable', values='MINING_DW_SUBSCR_NO').reset_index()


# In[424]:

base_three_sims.shape[0] * 3


# # Location

# In[425]:

table["CDR_2SIM_LOCATION_INT_02_WITHMI"].shape


# In[426]:

two_sims_location = pd.merge(base_two_sims, table["CDR_2SIM_LOCATION_INT_02_WITHMI"], 
                             how='left',on=['DW_PARTY_ID','MINING_DW_SUBSCR_NO_A','MINING_DW_SUBSCR_NO_B'])
two_sims_location = two_sims_location.fillna(0)
two_sims_location.shape


# In[427]:

three_sims_location = pd.merge(base_three_sims, table["CDR_3SIM_LOCATION_INT_02_WITHMI"], how='left',
                                       on=['DW_PARTY_ID','MINING_DW_SUBSCR_NO_A','MINING_DW_SUBSCR_NO_B','MINING_DW_SUBSCR_NO_C'])
three_sims_location = three_sims_location.fillna(0)
three_sims_location.shape


# In[428]:

two_sims_location['ALL_LOCATION'] =  two_sims_location['A_LOCATION_DATA'] + two_sims_location['B_LOCATION_DATA'] + two_sims_location['A_LOCATION_VOICE'] + two_sims_location['B_LOCATION_VOICE']
two_sims_location['AVG_INTERSECTION'] = two_sims_location['INTERSECTION'] / (two_sims_location['ALL_LOCATION'] / 2)


# In[429]:

three_sims_location.head(5)


# In[430]:

#AB
three_sims_location['AB_ALL_LOCATION'] = three_sims_location['A_LOCATION_DATA'] + three_sims_location['A_LOCATION_VOICE'] + three_sims_location['B_LOCATION_DATA'] + three_sims_location['B_LOCATION_VOICE'] 
three_sims_location['AB_AVG_INTERSECTION'] = three_sims_location['AB_INTERSECTION'] / (three_sims_location['AB_ALL_LOCATION'] / 2)

#BC
three_sims_location['BC_ALL_LOCATION'] = three_sims_location['B_LOCATION_DATA'] + three_sims_location['B_LOCATION_VOICE'] + three_sims_location['C_LOCATION_DATA'] + three_sims_location['C_LOCATION_VOICE'] 
three_sims_location['BC_AVG_INTERSECTION'] = three_sims_location['BC_INTERSECTION'] / (three_sims_location['BC_ALL_LOCATION'] / 2)

#AC

three_sims_location['AC_ALL_LOCATION'] = three_sims_location['A_LOCATION_DATA'] + three_sims_location['A_LOCATION_VOICE'] + three_sims_location['C_LOCATION_DATA'] + three_sims_location['C_LOCATION_VOICE'] 
three_sims_location['AC_AVG_INTERSECTION'] = three_sims_location['AC_INTERSECTION'] /(three_sims_location['AC_ALL_LOCATION'] / 2)


# In[431]:

three_sims_location.head(10)


# In[432]:

loc_intersection = pd.concat([two_sims_location.loc[:,'AVG_INTERSECTION'], three_sims_location.loc[:, 'AB_AVG_INTERSECTION'], three_sims_location.loc[:,'BC_AVG_INTERSECTION'], three_sims_location.loc[:,'AC_AVG_INTERSECTION']])


# In[433]:

loc_intersection.shape


# # Call Intersection

# In[434]:

table['CDR_2SIM_CALL_INT'].head(5)                      


# In[435]:

two_sims_call = pd.merge(base_two_sims, table["CDR_2SIM_CALL_INT"], how='left',
                                       on=['DW_PARTY_ID', 'MINING_DW_SUBSCR_NO_A', 'MINING_DW_SUBSCR_NO_B'])
two_sims_call = two_sims_call.fillna(0)
two_sims_call.shape


# In[436]:

table["CDR_3SIM_CALL_INT"].shape


# In[437]:

three_sims_call = pd.merge(base_three_sims, table["CDR_3SIM_CALL_INT"], how='left',
                                       on=['DW_PARTY_ID', 'MINING_DW_SUBSCR_NO_A', 'MINING_DW_SUBSCR_NO_B' , 'MINING_DW_SUBSCR_NO_C'])
three_sims_call = three_sims_call.fillna(0)
three_sims_call.shape


# In[438]:

two_sims_call['ALL_CALL'] =  two_sims_call['A_CALL_RECORD'] + two_sims_call['B_CALL_RECORD'] 
two_sims_call['AVG_INTERSECTION'] = two_sims_call['INTERSECTION'] / (two_sims_call['ALL_CALL'] / 2)


# In[439]:

three_sims_call.head(5)


# In[440]:

#AB
three_sims_call['AB_ALL_CALL'] = three_sims_call['A_CALL_RECORD'] + three_sims_call['B_CALL_RECORD']  
three_sims_call['AB_AVG_INTERSECTION'] = three_sims_call['AB_INTERSECTION'] / (three_sims_call['AB_ALL_CALL'] / 2)

#BC
three_sims_call['BC_ALL_CALL'] = three_sims_call['B_CALL_RECORD'] + three_sims_call['C_CALL_RECORD']
three_sims_call['BC_AVG_INTERSECTION'] = three_sims_call['BC_INTERSECTION'] / (three_sims_call['BC_ALL_CALL'] / 2)

#AC
three_sims_call['AC_ALL_CALL'] = three_sims_call['A_CALL_RECORD'] + three_sims_call['C_CALL_RECORD'] 
three_sims_call['AC_AVG_INTERSECTION'] = three_sims_call['AC_INTERSECTION'] /(three_sims_call['AC_ALL_CALL'] / 2)


# In[441]:

call_intersection = pd.concat([two_sims_call.loc[:,'AVG_INTERSECTION'], 
                               three_sims_call.loc[:, 'AB_AVG_INTERSECTION'],
                               three_sims_call.loc[:,'BC_AVG_INTERSECTION'], 
                               three_sims_call.loc[:,'AC_AVG_INTERSECTION']])


# In[442]:

call_intersection.shape


# ***

# # fill na distribution
# # all
# call_int = call_intersection.fillna(0)
# loc_int = loc_intersection.fillna(0)

# #only two sims
# call_int = two_sims_call.loc[:,'AVG_INTERSECTION'].fillna(0)
# loc_int = two_sims_location.loc[:,'AVG_INTERSECTION'].fillna(0)

# #only three sims
# call_int = pd.concat([three_sims_call.loc[:,'AB_AVG_INTERSECTION'],
#                      three_sims_call.loc[:,'BC_AVG_INTERSECTION'], 
#                      three_sims_call.loc[:,'AC_AVG_INTERSECTION']]).fillna(0)

# loc_int =  pd.concat([three_sims_location.loc[:, 'AB_AVG_INTERSECTION'], 
#                       three_sims_location.loc[:,'BC_AVG_INTERSECTION'], three_sims_location.loc[:,'AC_AVG_INTERSECTION']]).fillna(0)


# # drop na distribution

# In[461]:

# # all
# call_int = call_intersection.dropna()
# loc_int = loc_intersection.dropna()

# #only two sims
# call_int = two_sims_call.loc[:,'AVG_INTERSECTION'].dropna(0)
# loc_int = two_sims_location.loc[:,'AVG_INTERSECTION'].dropna(0)

#only three sims
call_int = pd.concat([three_sims_call.loc[:,'AB_AVG_INTERSECTION'],
                     three_sims_call.loc[:,'BC_AVG_INTERSECTION'], 
                     three_sims_call.loc[:,'AC_AVG_INTERSECTION']]).dropna(0)

loc_int =  pd.concat([three_sims_location.loc[:, 'AB_AVG_INTERSECTION'], 
                      three_sims_location.loc[:,'BC_AVG_INTERSECTION'], three_sims_location.loc[:,'AC_AVG_INTERSECTION']]).dropna(0)


# In[462]:

def check_ci_bound(data, ci=0.95):
    _data = pd.DataFrame(np.sort(data).tolist(), columns = ["value"])
    _data['interval'] = np.ceil(_data['value']/0.05)*0.05
    return _data.iloc[int(np.floor(ci * len(_data) )), 1]


# In[463]:

from __future__ import division, print_function
from matplotlib import pyplot as plt
# In a notebook environment, display the plots inline
get_ipython().magic('matplotlib inline')

# Set some parameters to apply to all plots. These can be overridden
# in each plot if desired
import matplotlib
# Plot size to 14" x 7"
matplotlib.rc('figure', figsize = (14, 7))
# Font size to 14
matplotlib.rc('font', size = 14)
# Do not display top and right frame lines
matplotlib.rc('axes.spines', top = False, right = False)
# Remove grid lines
matplotlib.rc('axes', grid = False)
# Set backgound color to white
matplotlib.rc('axes', facecolor = 'white')


# In[464]:

# Define a function for a histogram
def histogram(data, x_label, y_label, title, bound):
    _, ax = plt.subplots()
    ax.hist(data, color = '#539caf')
    ax.set_ylabel(y_label)
    ax.set_xlabel(x_label)
    ax.set_title(title)
    ax.axvline(data.mean(), color='b', linestyle='dashed', linewidth=2, label="mean")
    ax.annotate('Mean', xy=(data.mean(), len(data)*0.05), xytext=(data.mean() + 0.05, len(data)*0.05),
            arrowprops=dict(facecolor='black', shrink=0.05),
            )
    y = 1
    for b in bound:
        b_value = check_ci_bound(data, b)
        ax.axvline(b_value, color='r', linestyle='dashed', linewidth=2, label="mean")
        ax.annotate('Confidence Interval ' + str(b), xy=(b_value, len(data)*0.05), xytext=(b_value + 0.05, (len(data)*0.05) * y),
                arrowprops=dict(facecolor='black', shrink=0.05),
                )
        y +=1


# In[465]:

# Call the function to create plot
histogram(data = loc_int
           , x_label = 'Percentage of location similarity'
           , y_label = 'Number of people'
           , title = 'Distribution of location similarity'
           , bound = [0.95, 0.9])


# In[466]:

# Call the function to create plot
histogram(data = call_int
           , x_label = 'Percentage of contact list similarity'
           , y_label = 'Number of people'
           , title = 'Distribution of contact list similarity'
           , bound = [0.95,0.9])


# ***

# ***

# # TWO SIMS

# ## location

# In[220]:

fin_two_sims_location = two_sims_location[['DW_PARTY_ID', 'MINING_DW_SUBSCR_NO_A', 'MINING_DW_SUBSCR_NO_B', 
                                           'ALL_LOCATION', 'AVG_INTERSECTION' ]]
fin_two_sims_location = fin_two_sims_location.rename(columns={'AVG_INTERSECTION' : 'LOC_AVG_INTERSECTION'})


# In[221]:

fin_two_sims_location.set_index(['DW_PARTY_ID', 'LOC_AVG_INTERSECTION'], inplace=True)
loc_result = pd.DataFrame(pd.concat([fin_two_sims_location.MINING_DW_SUBSCR_NO_A, fin_two_sims_location.MINING_DW_SUBSCR_NO_B]), 
             columns=['MINING_DW_SUBSCR_NO']).reset_index()


# In[222]:

loc_result.loc[loc_result.LOC_AVG_INTERSECTION >= loc_bound, 'LOC_AVG_INTERSECTION'] = 1
loc_result.loc[loc_result.LOC_AVG_INTERSECTION < loc_bound, 'LOC_AVG_INTERSECTION'] = 0
loc_result = loc_result[['DW_PARTY_ID', 'MINING_DW_SUBSCR_NO', 'LOC_AVG_INTERSECTION']]
loc_result = loc_result.fillna(0)


# In[223]:

loc_result.groupby(['LOC_AVG_INTERSECTION']).size()


# ## call

# In[224]:

fin_two_sims_call = two_sims_call[['DW_PARTY_ID', 'MINING_DW_SUBSCR_NO_A', 'MINING_DW_SUBSCR_NO_B', 
                                           'ALL_CALL', 'AVG_INTERSECTION' ]]
fin_two_sims_call= fin_two_sims_call.rename(columns={'AVG_INTERSECTION' : 'CALL_AVG_INTERSECTION'})


# In[225]:

fin_two_sims_call.set_index(['DW_PARTY_ID', 'CALL_AVG_INTERSECTION'], inplace=True)
call_result = pd.DataFrame(pd.concat([fin_two_sims_call.MINING_DW_SUBSCR_NO_A, fin_two_sims_call.MINING_DW_SUBSCR_NO_B]), 
             columns=['MINING_DW_SUBSCR_NO']).reset_index()


# In[226]:

call_result.loc[call_result.CALL_AVG_INTERSECTION >= call_bound, 'CALL_AVG_INTERSECTION'] = 1
call_result.loc[call_result.CALL_AVG_INTERSECTION < call_bound, 'CALL_AVG_INTERSECTION'] = 0
call_result = call_result[['DW_PARTY_ID', 'MINING_DW_SUBSCR_NO', 'CALL_AVG_INTERSECTION']]
call_result = call_result.fillna(0)


# In[227]:

call_result.groupby(['CALL_AVG_INTERSECTION']).size()


# # SELF CALL

# In[228]:

self_call = table['CDR_2SIM_DIALING_CALL']
self_call = self_call.sort_values(['DW_PARTY_ID'])

self_call_df = pd.merge(base_two_sims, self_call, how='left', 
                             on=['DW_PARTY_ID','MINING_DW_SUBSCR_NO_A','MINING_DW_SUBSCR_NO_B'])
self_call_df = self_call_df.fillna(0)
self_call_df.set_index(['DW_PARTY_ID', 'SELF_CALL'], inplace=True)
self_call_result = pd.DataFrame(pd.concat([self_call_df.MINING_DW_SUBSCR_NO_A, self_call_df.MINING_DW_SUBSCR_NO_B]), 
             columns=['MINING_DW_SUBSCR_NO']).reset_index()
self_call_result.loc[self_call_result.SELF_CALL > 0, 'SELF_CALL'] = 1
self_call_result.loc[self_call_result.SELF_CALL == 0, 'SELF_CALL'] = 0


# In[229]:

self_call_result.groupby(['SELF_CALL']).size()


# ## FINAL TWO SIMS

# In[230]:

final_df_two = pd.merge(loc_result, call_result, how='left', 
                        on=['DW_PARTY_ID','MINING_DW_SUBSCR_NO'])
final_df_two = pd.merge(final_df_two, self_call_result, how='left', 
                        on=['DW_PARTY_ID','MINING_DW_SUBSCR_NO'])


# In[231]:

final_df_two.shape


# In[232]:

final_df_two.loc[((final_df_two.CALL_AVG_INTERSECTION == 0) & (final_df_two.LOC_AVG_INTERSECTION == 1) & (final_df_two.SELF_CALL == 0)), 
             "SEGMENT_TYPE"] = "same"
final_df_two.loc[((final_df_two.CALL_AVG_INTERSECTION == 0) & (final_df_two.LOC_AVG_INTERSECTION == 1) & (final_df_two.SELF_CALL == 1)), 
             "SEGMENT_TYPE"] = "not same"
final_df_two.loc[((final_df_two.CALL_AVG_INTERSECTION == 1) & (final_df_two.LOC_AVG_INTERSECTION == 1)), 
             "SEGMENT_TYPE"] = "same"
final_df_two.loc[((final_df_two.CALL_AVG_INTERSECTION == 1) & (final_df_two.LOC_AVG_INTERSECTION == 0)), 
             "SEGMENT_TYPE"] = "same"
final_df_two.loc[((final_df_two.CALL_AVG_INTERSECTION == 0) & (final_df_two.LOC_AVG_INTERSECTION == 0)), 
             "SEGMENT_TYPE"] = "not same"


# ***

# # THREE SIMS

# ## location

# Check similarity based on the bound determined

# In[233]:

fin_three_sims_location = three_sims_location[['DW_PARTY_ID', 'MINING_DW_SUBSCR_NO_A', 'MINING_DW_SUBSCR_NO_B', 
                                               'MINING_DW_SUBSCR_NO_C','AB_AVG_INTERSECTION',
                                              'BC_AVG_INTERSECTION', 'AC_AVG_INTERSECTION']]
fin_three_sims_location = fin_three_sims_location.rename(columns={'AB_AVG_INTERSECTION' : 'AB_LOC_AVG_INTERSECTION'})
fin_three_sims_location = fin_three_sims_location.rename(columns={'BC_AVG_INTERSECTION' : 'BC_LOC_AVG_INTERSECTION'})
fin_three_sims_location = fin_three_sims_location.rename(columns={'AC_AVG_INTERSECTION' : 'AC_LOC_AVG_INTERSECTION'})
fin_three_sims_location = fin_three_sims_location.fillna(0)


# In[234]:

fin_three_sims_location.loc[fin_three_sims_location.AB_LOC_AVG_INTERSECTION >= loc_bound, 
                            'AB_LOC_AVG_INTERSECTION'] = 1
fin_three_sims_location.loc[fin_three_sims_location.AB_LOC_AVG_INTERSECTION < loc_bound, 
                            'AB_LOC_AVG_INTERSECTION'] = 0
fin_three_sims_location.loc[fin_three_sims_location.BC_LOC_AVG_INTERSECTION >= loc_bound, 
                            'BC_LOC_AVG_INTERSECTION'] = 1
fin_three_sims_location.loc[fin_three_sims_location.BC_LOC_AVG_INTERSECTION < loc_bound, 
                            'BC_LOC_AVG_INTERSECTION'] = 0
fin_three_sims_location.loc[fin_three_sims_location.AC_LOC_AVG_INTERSECTION >= loc_bound, 
                            'AC_LOC_AVG_INTERSECTION'] = 1
fin_three_sims_location.loc[fin_three_sims_location.AC_LOC_AVG_INTERSECTION < loc_bound, 
                            'AC_LOC_AVG_INTERSECTION'] = 0


# Determine all three sims same and not same [A B C]

# In[235]:

loc_three_same = fin_three_sims_location.query("AB_LOC_AVG_INTERSECTION == 1 and BC_LOC_AVG_INTERSECTION == 1 and AC_LOC_AVG_INTERSECTION == 1")
loc_three_notsame = fin_three_sims_location.query("AB_LOC_AVG_INTERSECTION == 0 and BC_LOC_AVG_INTERSECTION == 0 and AC_LOC_AVG_INTERSECTION == 0")
loc_three_diff = fin_three_sims_location.drop(loc_three_same.index)
loc_three_diff = loc_three_diff.drop(loc_three_notsame.index)


# In[236]:

fin_loc_three_same = pd.DataFrame(pd.concat([loc_three_same.loc[:, 'MINING_DW_SUBSCR_NO_A'], 
                                   loc_three_same.loc[:, 'MINING_DW_SUBSCR_NO_B'],
                                   loc_three_same.loc[:, 'MINING_DW_SUBSCR_NO_C']]), columns=['MINING_DW_SUBSCR_NO'])
fin_loc_three_same['LOCATION_SIM'] = "same"
fin_loc_three_notsame = pd.DataFrame(pd.concat([loc_three_notsame.loc[:, 'MINING_DW_SUBSCR_NO_A'], 
                                   loc_three_notsame.loc[:, 'MINING_DW_SUBSCR_NO_B'],
                                   loc_three_notsame.loc[:, 'MINING_DW_SUBSCR_NO_C']]), columns=['MINING_DW_SUBSCR_NO'])
fin_loc_three_notsame['LOCATION_SIM'] = "not same"


# In[237]:

three_sims_loc_result = pd.concat([fin_loc_three_same, fin_loc_three_notsame])


# Determine the two sims same and one diff

# In[238]:

all_loc_diff = pd.DataFrame(pd.concat([loc_three_diff.loc[:, 'MINING_DW_SUBSCR_NO_A'], 
                                   loc_three_diff.loc[:, 'MINING_DW_SUBSCR_NO_B'],
                                   loc_three_diff.loc[:, 'MINING_DW_SUBSCR_NO_C']]), columns=['MINING_DW_SUBSCR_NO'])
all_loc_diff['LOCATION_SIM'] = 'same'
all_loc_diff = all_loc_diff.set_index(['MINING_DW_SUBSCR_NO'])


# In[239]:

a_loc_diff = loc_three_diff.query('BC_LOC_AVG_INTERSECTION == 1')[['MINING_DW_SUBSCR_NO_A']].rename(
columns={'MINING_DW_SUBSCR_NO_A' : 'MINING_DW_SUBSCR_NO'})
b_loc_diff = loc_three_diff.query('AC_LOC_AVG_INTERSECTION == 1')[['MINING_DW_SUBSCR_NO_B']].rename(
columns={'MINING_DW_SUBSCR_NO_B' : 'MINING_DW_SUBSCR_NO'})
c_loc_diff = loc_three_diff.query('AB_LOC_AVG_INTERSECTION == 1')[['MINING_DW_SUBSCR_NO_C']].rename(
columns={'MINING_DW_SUBSCR_NO_C' : 'MINING_DW_SUBSCR_NO'})
new_loc_diff = pd.concat([a_loc_diff, b_loc_diff, c_loc_diff])
new_loc_diff['LOCATION_SIM'] = 'not same'
new_loc_diff = new_loc_diff.set_index(['MINING_DW_SUBSCR_NO'])


# In[240]:

all_loc_diff.update(new_loc_diff)
all_loc_diff.reset_index(inplace=True)


# In[241]:

three_sims_loc_result = pd.concat([three_sims_loc_result,all_loc_diff])
three_sims_loc_result.shape


# ***

# ## CALL

# Check similarity based on the bound determined

# In[242]:

fin_three_sims_call = three_sims_call[['DW_PARTY_ID', 'MINING_DW_SUBSCR_NO_A', 'MINING_DW_SUBSCR_NO_B', 
                                               'MINING_DW_SUBSCR_NO_C','AB_AVG_INTERSECTION',
                                              'BC_AVG_INTERSECTION', 'AC_AVG_INTERSECTION']]
fin_three_sims_call = fin_three_sims_call.rename(columns={'AB_AVG_INTERSECTION' : 'AB_CALL_AVG_INTERSECTION'})
fin_three_sims_call = fin_three_sims_call.rename(columns={'BC_AVG_INTERSECTION' : 'BC_CALL_AVG_INTERSECTION'})
fin_three_sims_call = fin_three_sims_call.rename(columns={'AC_AVG_INTERSECTION' : 'AC_CALL_AVG_INTERSECTION'})
fin_three_sims_call = fin_three_sims_call.fillna(0)


# In[243]:

fin_three_sims_call.loc[fin_three_sims_call.AB_CALL_AVG_INTERSECTION >= call_bound, 
                            'AB_CALL_AVG_INTERSECTION'] = 1
fin_three_sims_call.loc[fin_three_sims_call.AB_CALL_AVG_INTERSECTION < call_bound, 
                            'AB_CALL_AVG_INTERSECTION'] = 0
fin_three_sims_call.loc[fin_three_sims_call.BC_CALL_AVG_INTERSECTION >= call_bound, 
                            'BC_CALL_AVG_INTERSECTION'] = 1
fin_three_sims_call.loc[fin_three_sims_call.BC_CALL_AVG_INTERSECTION < call_bound, 
                            'BC_CALL_AVG_INTERSECTION'] = 0
fin_three_sims_call.loc[fin_three_sims_call.AC_CALL_AVG_INTERSECTION >= call_bound, 
                            'AC_CALL_AVG_INTERSECTION'] = 1
fin_three_sims_call.loc[fin_three_sims_call.AC_CALL_AVG_INTERSECTION < call_bound, 
                            'AC_CALL_AVG_INTERSECTION'] = 0


# In[244]:

call_three_same = fin_three_sims_call.query("AB_CALL_AVG_INTERSECTION == 1 and BC_CALL_AVG_INTERSECTION == 1 and AC_CALL_AVG_INTERSECTION == 1")
call_three_notsame = fin_three_sims_call.query("AB_CALL_AVG_INTERSECTION == 0 and BC_CALL_AVG_INTERSECTION == 0 and AC_CALL_AVG_INTERSECTION == 0")
call_three_diff = fin_three_sims_call.drop(call_three_same.index)
call_three_diff = call_three_diff.drop(call_three_notsame.index)


# Determine all three sims same and not same [A B C]

# In[245]:

fin_call_three_same = pd.DataFrame(pd.concat([call_three_same.loc[:, 'MINING_DW_SUBSCR_NO_A'], 
                                   call_three_same.loc[:, 'MINING_DW_SUBSCR_NO_B'],
                                   call_three_same.loc[:, 'MINING_DW_SUBSCR_NO_C']]), columns=['MINING_DW_SUBSCR_NO'])
fin_call_three_same['CALL_SIM'] = "same"
fin_call_three_notsame = pd.DataFrame(pd.concat([call_three_notsame.loc[:, 'MINING_DW_SUBSCR_NO_A'], 
                                   call_three_notsame.loc[:, 'MINING_DW_SUBSCR_NO_B'],
                                   call_three_notsame.loc[:, 'MINING_DW_SUBSCR_NO_C']]), columns=['MINING_DW_SUBSCR_NO'])
fin_call_three_notsame['CALL_SIM'] = "not same"


# In[246]:

three_sims_call_result = pd.concat([fin_call_three_same, fin_call_three_notsame])


# Determine the two sims same and one diff

# In[247]:

all_call_diff = pd.DataFrame(pd.concat([call_three_diff.loc[:, 'MINING_DW_SUBSCR_NO_A'], 
                                   call_three_diff.loc[:, 'MINING_DW_SUBSCR_NO_B'],
                                   call_three_diff.loc[:, 'MINING_DW_SUBSCR_NO_C']]), columns=['MINING_DW_SUBSCR_NO'])
all_call_diff['CALL_SIM'] = 'same'
all_call_diff = all_call_diff.set_index(['MINING_DW_SUBSCR_NO'])


# In[248]:

a_call_diff = call_three_diff.query('BC_CALL_AVG_INTERSECTION == 1')[['MINING_DW_SUBSCR_NO_A']].rename(
columns={'MINING_DW_SUBSCR_NO_A' : 'MINING_DW_SUBSCR_NO'})
b_call_diff = call_three_diff.query('AC_CALL_AVG_INTERSECTION == 1')[['MINING_DW_SUBSCR_NO_B']].rename(
columns={'MINING_DW_SUBSCR_NO_B' : 'MINING_DW_SUBSCR_NO'})
c_call_diff = call_three_diff.query('AB_CALL_AVG_INTERSECTION == 1')[['MINING_DW_SUBSCR_NO_C']].rename(
columns={'MINING_DW_SUBSCR_NO_C' : 'MINING_DW_SUBSCR_NO'})
new_call_diff = pd.concat([a_call_diff, b_call_diff, c_call_diff])
new_call_diff['CALL_SIM'] = 'not same'
new_call_diff = new_call_diff.set_index(['MINING_DW_SUBSCR_NO'])


# In[249]:

all_call_diff.update(new_call_diff)
all_call_diff.reset_index(inplace=True)


# In[250]:

three_sims_call_result = pd.concat([three_sims_call_result, all_call_diff])
three_sims_call_result.shape


# # self call

# In[251]:

self_call = table['CDR_3SIM_DIALING_CALL']
self_call_df = pd.merge(base_three_sims, self_call, how='left', 
                             on=['DW_PARTY_ID','MINING_DW_SUBSCR_NO_A','MINING_DW_SUBSCR_NO_B', 'MINING_DW_SUBSCR_NO_C'])
self_call_df = self_call_df.fillna(0)


# In[252]:

self_call_three_same = self_call_df.query("AB_SELF_CALL > 0 and BC_SELF_CALL > 0 and AC_SELF_CALL > 0")
self_call_three_notsame = self_call_df.query("AB_SELF_CALL == 0 and BC_SELF_CALL == 0 and AC_SELF_CALL == 0")
self_call_three_diff = self_call_df.drop(self_call_three_same.index)
self_call_three_diff = self_call_three_diff.drop(self_call_three_notsame.index)


# In[253]:

fin_self_call_three_same = pd.DataFrame(pd.concat([self_call_three_same.loc[:, 'MINING_DW_SUBSCR_NO_A'], 
                                   self_call_three_same.loc[:, 'MINING_DW_SUBSCR_NO_B'],
                                   self_call_three_same.loc[:, 'MINING_DW_SUBSCR_NO_C']]), columns=['MINING_DW_SUBSCR_NO'])
fin_self_call_three_same['SELF_CALL_SIM'] = "same"
fin_self_call_three_notsame = pd.DataFrame(pd.concat([self_call_three_notsame.loc[:, 'MINING_DW_SUBSCR_NO_A'], 
                                   self_call_three_notsame.loc[:, 'MINING_DW_SUBSCR_NO_B'],
                                   self_call_three_notsame.loc[:, 'MINING_DW_SUBSCR_NO_C']]), columns=['MINING_DW_SUBSCR_NO'])
fin_self_call_three_notsame['SELF_CALL_SIM'] = "not same"


# In[254]:

three_sims_self_call_result = pd.concat([fin_self_call_three_same, fin_self_call_three_notsame])
three_sims_self_call_result.shape


# In[255]:

all_self_call_diff = pd.DataFrame(pd.concat([self_call_three_diff.loc[:, 'MINING_DW_SUBSCR_NO_A'], 
                                   self_call_three_diff.loc[:, 'MINING_DW_SUBSCR_NO_B'],
                                   self_call_three_diff.loc[:, 'MINING_DW_SUBSCR_NO_C']]), columns=['MINING_DW_SUBSCR_NO'])
all_self_call_diff['SELF_CALL_SIM'] = 'same'
all_self_call_diff = all_self_call_diff.set_index(['MINING_DW_SUBSCR_NO'])


# In[256]:

a_self_call_diff = self_call_three_diff.query('BC_SELF_CALL > 0')[['MINING_DW_SUBSCR_NO_A']].rename(
columns={'MINING_DW_SUBSCR_NO_A' : 'MINING_DW_SUBSCR_NO'})
b_self_call_diff = self_call_three_diff.query('AC_SELF_CALL > 0')[['MINING_DW_SUBSCR_NO_B']].rename(
columns={'MINING_DW_SUBSCR_NO_B' : 'MINING_DW_SUBSCR_NO'})
c_self_call_diff = self_call_three_diff.query('AB_SELF_CALL > 0')[['MINING_DW_SUBSCR_NO_C']].rename(
columns={'MINING_DW_SUBSCR_NO_C' : 'MINING_DW_SUBSCR_NO'})
new_self_call_diff = pd.concat([a_self_call_diff, b_self_call_diff, c_self_call_diff])
new_self_call_diff['SELF_CALL_SIM'] = 'not same'
new_self_call_diff = new_self_call_diff.set_index(['MINING_DW_SUBSCR_NO'])


# In[257]:

all_self_call_diff.update(new_call_diff)
all_self_call_diff.reset_index(inplace=True)


# In[258]:

three_sims_self_call_result = pd.concat([three_sims_self_call_result, all_self_call_diff])
three_sims_self_call_result.shape


# # final three sims

# In[259]:

final_three_sims = pd.merge(three_sims_loc_result, three_sims_call_result, on=['MINING_DW_SUBSCR_NO'])
final_three_sims = pd.merge(final_three_sims, three_sims_self_call_result, on=['MINING_DW_SUBSCR_NO'])


# In[260]:

final_three_sims['SEGMENT_TYPE'] = 'same'
final_three_sims.loc[(final_three_sims.LOCATION_SIM == "not same") & (final_three_sims.CALL_SIM == "not same"), 
                     'SEGMENT_TYPE'] = "not same"
final_three_sims.loc[(final_three_sims.LOCATION_SIM == "same") & (final_three_sims.CALL_SIM == "not same") & (final_three_sims.SELF_CALL_SIM == "same"), 
                     'SEGMENT_TYPE'] = "not same"


# In[261]:

final_three_sims.shape


# ***

# ***

# # COMBINE AND OUTPUT RESULT

# In[262]:

single_sims.loc[:,'SEGMENT_TYPE'] = "not same"


# In[263]:

multi_sims_final = pd.concat([single_sims[['MINING_DW_SUBSCR_NO', 'SEGMENT_TYPE']], 
                              final_df_two[['MINING_DW_SUBSCR_NO',  'SEGMENT_TYPE']],
                              final_three_sims[['MINING_DW_SUBSCR_NO', 'SEGMENT_TYPE']]
                             ])


# In[264]:

multi_sims_final = pd.merge(multi_sims_base[['DW_PARTY_ID', 'MINING_DW_SUBSCR_NO', 'REAL_PTY_CBU_PO_CNT']], multi_sims_final, how='left', 
                             on=['MINING_DW_SUBSCR_NO'])


# In[265]:

multi_sims_final.groupby(['SEGMENT_TYPE']).size()


# In[266]:

multi_sims_final_grouped = pd.DataFrame(multi_sims_final.groupby(['DW_PARTY_ID','REAL_PTY_CBU_PO_CNT', 'SEGMENT_TYPE']).size().reset_index(name="COUNT_SIZE"))


# In[267]:

multi_sims_final_grouped.to_csv("multi_sims_grouped.csv", mode="w")
multi_sims_final.to_csv("multi_sims_segmentation_0.9.csv", mode="w")


# ***
