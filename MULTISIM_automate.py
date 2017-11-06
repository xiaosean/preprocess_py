import time

def log(msg):
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(time.time()))
    msg = current_time + "\t" + msg
    print(msg)
    with open("log.txt", "a") as log_file:
        log_file.write(msg + "\n")

log("Importing Packages")

import pandas as pd
import numpy as np

def check_ci_bound(data, ci=0.95):
    _data = pd.DataFrame(np.sort(data).tolist(), columns = ["value"])
    _data['interval'] = np.ceil(_data['value']/0.05)*0.05
    return _data.iloc[int(np.floor(ci * len(_data) )), 1]

sims = ['A', 'B', 'C', 'D']
DATA_MONTH = '2017/4/1'

log("Reading Data")

cols = ['DATA_MONTH', 'MINING_DW_SUBSCR_NO', 'DW_PARTY_ID', 'PTY_CBU_PO_CNT', 'SUBSCR_STATUS_CODE', 'DORMANT_MONTH_CNT_MKT', 'TENURE_SCV', 'RPS_NAME', 'CUST_TYPE']
multisim_mds = pd.read_csv('NEW_DATA_FULL_2017_10_18/ALL_MDS.txt', usecols=cols)

multisim_mds.PTY_CBU_PO_CNT = pd.to_numeric(multisim_mds.PTY_CBU_PO_CNT, errors='coerce')
multisim_mds.PTY_CBU_PO_CNT.fillna(0, inplace=True)

multisim_mds_filter = multisim_mds[(multisim_mds.RPS_NAME == "CONSUMER MOBILITY") & (multisim_mds.SUBSCR_STATUS_CODE == 'A') & (multisim_mds.TENURE_SCV >=3) & (multisim_mds.DORMANT_MONTH_CNT_MKT < 2) & (multisim_mds.DATA_MONTH == DATA_MONTH)]

mining_id_df = pd.DataFrame(multisim_mds_filter.groupby('DW_PARTY_ID')['MINING_DW_SUBSCR_NO'].apply(np.array).reset_index())

df1_2 = pd.read_csv('NEW_DATA_FULL_2017_10_18/CDR_2SIM_DIALING_CALL.txt')
df1_3 = pd.read_csv('NEW_DATA_FULL_2017_10_18/CDR_3SIM_DIALING_CALL.txt')
df1_4 = pd.read_csv('NEW_DATA_FULL_2017_10_18/OH_FNL_1_4SIM_20171013.txt')
df1_2 = df1_2.rename(columns={'SELF_CALL': 'AB_SELF_CALL'})

df2_2 = pd.read_csv('NEW_DATA_FULL_2017_10_18/CDR_2SIM_CALL_INT.txt', error_bad_lines=False)
df2_3 = pd.read_csv('NEW_DATA_FULL_2017_10_18/CDR_3SIM_CALL_INT.txt', error_bad_lines=False)
df2_4 = pd.read_csv('NEW_DATA_FULL_2017_10_18/OH_FNL_2_4SIM_20171013.txt', error_bad_lines=False)
df2_2 = df2_2.rename(columns={'INTERSECTION': 'AB_INTERSECTION'})

df4_2 = pd.read_csv('NEW_DATA_FULL_2017_10_18/CDR_2SIM_LOCATION_INT_02_WITHMI.txt', error_bad_lines=False)
df4_3 = pd.read_csv('NEW_DATA_FULL_2017_10_18/CDR_3SIM_LOCATION_INT_02_WITHMI.txt', error_bad_lines=False)
df4_4 = pd.read_csv('NEW_DATA_FULL_2017_10_18/OH_FNL_4_4SIM_20171013.txt', error_bad_lines=False)
df4_2 = df4_2.rename(columns={'INTERSECTION_VOICE': 'AB_INTERSECTION_VOICE', 
                              'INTERSECTION_DATA': 'AB_INTERSECTION_DATA', 
                              'INTERSECTION': 'AB_INTERSECTION'})

log("Filtering out PTY_CBU_PO_CNT > 4")

over_four = multisim_mds_filter[multisim_mds_filter.PTY_CBU_PO_CNT > 4][['DATA_MONTH', 'MINING_DW_SUBSCR_NO']].copy().reset_index(drop=True)
over_four.loc[:, 'GROUPS_NAME'] = 'Over_four_sims'
over_four.loc[:, 'GROUPS_ID'] = 1
over_four.to_csv('pty_over_four.csv', index=False)

log("Joining 2, 3, 4 sims")

df1 = pd.concat([df1_4, df1_3, df1_2], ignore_index=True)
# df1 = pd.concat([df1_3, df1_2], ignore_index=True)

# ABCD_ID = df1[['DW_PARTY_ID', 'MINING_DW_SUBSCR_NO_A','MINING_DW_SUBSCR_NO_B', 'MINING_DW_SUBSCR_NO_C']]
ABCD_ID = df1[['DW_PARTY_ID', 'MINING_DW_SUBSCR_NO_A','MINING_DW_SUBSCR_NO_B', 'MINING_DW_SUBSCR_NO_C', 'MINING_DW_SUBSCR_NO_D']]

ABCD_ID = pd.merge(ABCD_ID, mining_id_df, how='left', on='DW_PARTY_ID')

ABCD_ID = ABCD_ID[pd.notnull(ABCD_ID.MINING_DW_SUBSCR_NO)]

for index, row in ABCD_ID.iterrows():
    for s in sims:
        if pd.notnull(row['MINING_DW_SUBSCR_NO_' + s]) and not row['MINING_DW_SUBSCR_NO_' + s] in row['MINING_DW_SUBSCR_NO']:
            ABCD_ID.at[index, 'MINING_DW_SUBSCR_NO_' + s] = None

log("Computing Location Bound")

# df4 = pd.concat([df4_3, df4_2], ignore_index=True)
df4 = pd.concat([df4_4, df4_3, df4_2], ignore_index=True)

# df4.drop(['MINING_DW_SUBSCR_NO_A', 'MINING_DW_SUBSCR_NO_B', 'MINING_DW_SUBSCR_NO_C'], 1, inplace=True)
df4.drop(['MINING_DW_SUBSCR_NO_A', 'MINING_DW_SUBSCR_NO_B', 'MINING_DW_SUBSCR_NO_C', 'MINING_DW_SUBSCR_NO_D'], 1, inplace=True)
df4 = pd.merge(df4, ABCD_ID, how='left', on='DW_PARTY_ID')

for s in sims:
    df4[s + '_LOCATION'] = df4[s + '_LOCATION_DATA'] + df4[s + '_LOCATION_VOICE']

for i in range(len(sims) - 1):
    s1 = sims[i]
    for s2 in sims[i+1:]:
        df4[s1 + s2 + '_INTERSECTION'] = df4[s1 + s2 + '_INTERSECTION_VOICE'] + df4[s1 + s2 + '_INTERSECTION_DATA']
        df4[s1 + s2 + '_intersect_persentage'] = df4[s1 + s2 + '_INTERSECTION'] / ((df4[s1 + '_LOCATION'] + df4[s2 + '_LOCATION']) / 2)
        df4.loc[(df4[s1 + '_LOCATION'] + df4[s2 + '_LOCATION']) == 0, s1 + s2 + '_intersect_persentage'] = 0

location_intersection = pd.concat([
    df4.loc[(pd.notnull(df4.MINING_DW_SUBSCR_NO_A) & pd.notnull(df4.MINING_DW_SUBSCR_NO_B)), 'AB_intersect_persentage'].dropna(), 
    df4.loc[(pd.notnull(df4.MINING_DW_SUBSCR_NO_A) & pd.notnull(df4.MINING_DW_SUBSCR_NO_C)), 'AC_intersect_persentage'].dropna(),
    df4.loc[(pd.notnull(df4.MINING_DW_SUBSCR_NO_A) & pd.notnull(df4.MINING_DW_SUBSCR_NO_D)), 'AD_intersect_persentage'].dropna(), 
    df4.loc[(pd.notnull(df4.MINING_DW_SUBSCR_NO_B) & pd.notnull(df4.MINING_DW_SUBSCR_NO_C)), 'BC_intersect_persentage'].dropna(), 
    df4.loc[(pd.notnull(df4.MINING_DW_SUBSCR_NO_B) & pd.notnull(df4.MINING_DW_SUBSCR_NO_D)), 'BD_intersect_persentage'].dropna(), 
    df4.loc[(pd.notnull(df4.MINING_DW_SUBSCR_NO_C) & pd.notnull(df4.MINING_DW_SUBSCR_NO_D)), 'CD_intersect_persentage'].dropna()
])

location_bound = check_ci_bound(location_intersection)

df2 = pd.concat([df2_4, df2_3, df2_2], ignore_index=True)
# df2 = pd.concat([df2_3, df2_2], ignore_index=True)

df2.drop(['MINING_DW_SUBSCR_NO_A', 'MINING_DW_SUBSCR_NO_B', 'MINING_DW_SUBSCR_NO_C', 'MINING_DW_SUBSCR_NO_D'], 1, inplace=True)
# df2.drop(['MINING_DW_SUBSCR_NO_A', 'MINING_DW_SUBSCR_NO_B', 'MINING_DW_SUBSCR_NO_C'], 1, inplace=True)
df2 = pd.merge(df2, ABCD_ID, how='left', on='DW_PARTY_ID')

for i in range(len(sims) - 1):
    s1 = sims[i]
    for s2 in sims[i+1:]:
        df2[s1 + s2 + '_intersect_persentage'] = df2[s1 + s2 + '_INTERSECTION'] / ((df2[s1 + '_CALL_RECORD'] + df2[s2 + '_CALL_RECORD']) / 2)
        df2.loc[(df2[s1 + '_CALL_RECORD'] + df2[s2 + '_CALL_RECORD']) == 0, s1 + s2 + '_intersect_persentage'] = 0

call_intersection = pd.concat([
    df2.loc[(pd.notnull(df2.MINING_DW_SUBSCR_NO_A) & pd.notnull(df2.MINING_DW_SUBSCR_NO_B)), 'AB_intersect_persentage'].dropna(), 
    df2.loc[(pd.notnull(df2.MINING_DW_SUBSCR_NO_A) & pd.notnull(df2.MINING_DW_SUBSCR_NO_C)), 'AC_intersect_persentage'].dropna(),
    df2.loc[(pd.notnull(df2.MINING_DW_SUBSCR_NO_A) & pd.notnull(df2.MINING_DW_SUBSCR_NO_D)), 'AD_intersect_persentage'].dropna(), 
    df2.loc[(pd.notnull(df2.MINING_DW_SUBSCR_NO_B) & pd.notnull(df2.MINING_DW_SUBSCR_NO_C)), 'BC_intersect_persentage'].dropna(), 
    df2.loc[(pd.notnull(df2.MINING_DW_SUBSCR_NO_B) & pd.notnull(df2.MINING_DW_SUBSCR_NO_D)), 'BD_intersect_persentage'].dropna(), 
    df2.loc[(pd.notnull(df2.MINING_DW_SUBSCR_NO_C) & pd.notnull(df2.MINING_DW_SUBSCR_NO_D)), 'CD_intersect_persentage'].dropna()
])

call_bound = check_ci_bound(call_intersection)

log("Cheking Different or Same behavior in each party id")

result = ABCD_ID.copy()

for i in range(len(sims) - 1):
    s1 = sims[i]
    for s2 in sims[i+1:]:
        result.loc[:, s1 + s2 + '_diff'] = ((df2[s1 + s2 + '_intersect_persentage'] < call_bound) & (df4[s1 + s2 + '_intersect_persentage'] < location_bound)) | ((df2[s1 + s2 + '_intersect_persentage'] < call_bound) & (df4[s1 + s2 + '_intersect_persentage'] >= location_bound) & (df1[s1 + s2 + '_SELF_CALL'] > 0))

result.loc[:, 'All_diff'] = True

for i in range(len(sims)-1):
    s1 = sims[i]
    for s2 in sims[i+1:]:
        result.loc[((~pd.isnull(result['MINING_DW_SUBSCR_NO_' + s1])) & (~pd.isnull(result['MINING_DW_SUBSCR_NO_' + s2])) & (result[s1 + s2 + '_diff'] == False)), 'All_diff'] = False

result_diff_id_df = pd.DataFrame()
result_diff_id_df['MINING_DW_SUBSCR_NO'] = np.concatenate(result[result.All_diff].MINING_DW_SUBSCR_NO.values)

result_other_id_df = pd.DataFrame()
result_other_id_df['MINING_DW_SUBSCR_NO'] = np.concatenate(result[result.All_diff != True].MINING_DW_SUBSCR_NO.values)
result_other_id_df.loc[:, 'DATA_MONTH'] = DATA_MONTH
result_other_id_df.loc[:, 'GROUPS_NAME'] = 'Not_diff'
result_other_id_df.loc[:, 'GROUPS_ID'] = 2

# log("Merging Real sim count")

# result['REAL_PTY_CNT'] = result.MINING_DW_SUBSCR_NO.apply(len)

# real_cnt = result.REAL_PTY_CNT.value_counts()

# mining_id_to_real_cnt = result.groupby('REAL_PTY_CNT')['MINING_DW_SUBSCR_NO'].apply(np.array)

# mining_real_cnt_df = pd.DataFrame()
# for index in mining_id_to_real_cnt.index:
#     mining = mining_id_to_real_cnt[index]
#     temp = np.concatenate(mining)
#     temp_df = pd.DataFrame()
#     temp_df['MINING_DW_SUBSCR_NO'] = temp
#     temp_df['REAL_PTY_CNT'] = [index] * len(temp)
#     mining_real_cnt_df = pd.concat([mining_real_cnt_df, temp_df], ignore_index=True)

# result_diff_id_df = pd.merge(result_diff_id_df, mining_real_cnt_df, how='left', on='MINING_DW_SUBSCR_NO')
# result_other_id_df = pd.merge(result_other_id_df, mining_real_cnt_df, how='left', on='MINING_DW_SUBSCR_NO')

log("Writing to CSV")

result_diff_id_df.to_csv('result_diff_all.csv', index=False)
result_other_id_df.to_csv('result_other_all.csv', index=False)

log("Finished")

