
# coding: utf-8

# In[2]:

import os.path
import numpy as np
import pandas as pd
import time
import pyodbc


# In[3]:

def get_table_path():
    try:
        logger.info("read preprocess_path_file.txt") #写入错误日志
        with open('./preprocess_path_file.txt') as f:
            read_data = f.read()
            read_data = read_data.replace("\r","")
            read_data = read_data.replace('"',"")
            read_data = read_data.replace("\n","")
            logger.info("txt split by ,") #写入错误日志
            table_list = read_data.split(",")
            table_dict = {}
            logger.info("load dict") #写入错误日志
            for table in table_list:
                table_name, table_path = table.split("=")
                table_dict[table_name] = table_path
            return table_dict
    except Exception as e:
        logger.error(e) #写入错误日志
    


# In[4]:

def write_to_log(msg):
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(time.time()))
    with open("log.txt", "a") as log_file:
        log_file.write(current_time + "\t" + msg + "\n")


# # Logger config

# In[5]:


import logging
import os
# create logger
LOG_DIR = "LOG"
if not os.path.exists(os.path.join(LOG_DIR)):
    os.makedirs(LOG_DIR)
log_path = os.path.join(".",LOG_DIR, "logging.log")

logger_name = "test"
logger = logging.getLogger(logger_name)
logger.setLevel(logging.DEBUG)

# create file handler
fh = logging.FileHandler(log_path)
fh.setLevel(logging.WARN)

# create formatter
fmt = "%(asctime)-15s %(levelname)s %(filename)s %(lineno)d %(process)d %(message)s"
datefmt = "%a %d %b %Y %H:%M:%S"
formatter = logging.Formatter(fmt, datefmt)

# add handler and formatter to logger
fh.setFormatter(formatter)
logger.addHandler(fh)


# In[4]:

logger.info("start marketing_filter_columns.py")
print("start marketing_filter_columns.py")
logger.info("start connect pyodbc")
con = pyodbc.connect('Driver=Teradata;DBCName=10.68.64.141;UID=V_CSM;PWD=qazwsx')
con.setencoding(encoding = 'utf-8')


# # Load path configure

# In[18]:

logger.info("Start load path configure")
table_dict = get_table_path()
DATA_MONTH = table_dict["DATA_MONTH"]
MDS_FILE = table_dict["MDS_TABLE"]
TELEGRAM_MT_FILE = table_dict["TELEGRAM_CDR_MT_AGGR_FILE"]
TELEGRAM_MO_FILE = table_dict["TELEGRAM_CDR_MO_AGGR_FILE"]
CWC_FILE = table_dict["CWC_TABLE"]
GROUP_ID_FILE = table_dict["GROUP_ID_FILE"]
OUT_FILENAME = table_dict["OUT_FILENAME"]
month = table_dict["MONTH"]
year = table_dict["YEAR"]
write_to_log("Finish load path configure")
logger.info("Finish load path configure")


# # configure example

# In[6]:

# DATA_MONTH="201704",
# MDS_TABLE="D:/NEW_DATA_FULL_10_6/MDS_MULTI_PTYCBU_1_4.txt",
# TELEGRAM_CDR_MT_AGGR_FILE="D:/0725_preprocess_dat/CDR_MONTHLY_AGGR/dm_subscr_mtc_mly_COMPLETED_revise_month_4.csv",
# TELEGRAM_CDR_MO_AGGR_FILE="D:/0725_preprocess_dat/CDR_MONTHLY_AGGR/dm_subscr_moc_mly_COMPLETED_revise_month_4.csv",
# CWC_TABLE="D:/NEW_DATA_FULL_2017_6_16/CWC_CATG_CNT_COMPLETED.txt",
# GROUP_ID_FILE="./Groups_ID_multi_1008.csv",
# OUT_FILENAME="mrk_picked_with_group_id.csv"


# In[8]:

try:
    
    # read csv file and print cost time
    t0 = time.time()
    query_str = "sel * from CSM_PROJECT." + "MDS_ACTIVE_MLY_567"
    query_where = ' where extract(month from DATA_MONTH) = ' + month + " AND SUBSCR_STATUS_CODE = \'A\' AND RPS_NAME = \'CONSUMER MOBILITY\' AND PTY_CBU_PO_CNT = 1"
    # query_where = ' where extract(month from DATA_MONTH) = ' + month
    query_sample = " sample 10"
    # df1 = pd.read_sql(query_str, con)
    logger.info("QUERY STR => %s" % query_str + query_where + query_sample)
    logger.info("START QUERY => %s" % query_str + query_where + query_sample)
    df = pd.read_sql(query_str + query_where + query_sample, con)
    # df = pd.read_csv(MDS_FILE, sep  = ',', error_bad_lines=False, nrows = 1)
    logger.info("time for read csv: %.2f" % (time.time()-t0))
except Exception as e:
    logger.error(e) #写入错误日志


# In[10]:

df_cols = list(df.columns)


# # Drop Column List

# In[11]:

# saving money id bcz it will merge group
# MINING_DW_SUBSCR_NO
# 因為之後telegram的會併入新的表 原本的有問題
telegram_str= """
MOC_FET_DUR
MOC_TWM_DUR
MOC_CHM_DUR
MOC_OTH_DUR
MOC_PSTN_DUR
MTC_FET_DUR
MTC_TWM_DUR
MTC_CHM_DUR
MTC_PSTN_DUR
"""
drop_str = """
CURR_SUBSCR_ID
DW_PARTY_ID
DATA_MONTH_RPT_TEMP1
DATA_MONTH_RPT_TEMP2
DATA_MONTH_RPT
GA_DATE
CHURN_IND
CHURN_TYPE
INACTV_DATE
MKT_CHURN_DATE
SUSPEND_IND
TARGET_OPR_ID
TEMP_INACTV_DATE
RPS_NAME
SUBSCR_STATUS_CODE
BILL_DISTRICT_NAME
CHURN_INDEX
IMEI_SMART_OS_FLAG
ACTV_CHANNEL_NAME
SHIPMENT_CHANNEL_ID
SHIPMENT_CHANNEL_CODE
SHIPMENT_CHANNEL_NAME
CCI_CHG_DATE
SEGMENT_NAME
NP_IN_DATE
BONDING_FLAG
CHURN_WELCOME_STAGE
PTY_NP_IN_IND
PTY_NP_OUT_IND
RENEW_APPLY_DATE
MDS_ELIGIBLE_FLAG
PROM_BUNDLE_VRP
PROM_BUNDLE_DRP
PROM_CURR_PROM_NAME
PROM_CURR_SYS_MODEL_IND
PROM_DEVICE_TYPE
PROM_DEVICE_BRAND
PROM_DEVICE_OS
PROM_DEVICE_MODEL
PROM_ACTV_PROM_CODE
PROM_ACTV_PROM_NAME
PROM_ACTV_PROM_CATG
PROM_CURR_APPLY_DATE
PROM_CURR_START_DATE
PROM_CURR_END_DATE
PROM_CURR_CONTR_EXP_DATE
L1M_PROM_CODE
L1M_PROM_NAME
L1M_PROM_COMMIT_MONTHS
CURR_PROM_TTL_CMF
CURR_PROM_CONTRACT_PERIOD
L1M_PROM_TTL_CMF
L1M_PROM_CONTRACT_PERIOD
DUM_PROM_CODE
GPRS_CAP_IND
BEST_VRP_DESC
BEST_DRP_DESC
SERVICE_APPLY_MOVIE_FLAG
SERVICE_APPLY_OMUSIC_FLAG
SERVICE_APPLY_READING_FLAG
HS_LEASE_FEATURE_START_DATE
HS_LEASE_FEATURE_END_DATE
HS_LEASE_CONTR_NAME
HS_LEASE_CONTR_START_DATE
HS_LEASE_CONTR_END_DATE
SMS30_FLAG
CURR_DATA_BILL_PLAN_START_DATE
CURR_DATA_BILL_PLAN_END_DATE
PRE_DATA_BILL_PLAN_ID
PRE_DATA_BILL_PLAN_NAME
PRE_DATA_BILL_PLAN_START_DATE
PRE_DATA_BILL_PLAN_END_DATE
DATA_BOOSTER_CURR_START_DATE
LIM_BILL_PLAN_NAME
L1M_DATA_BILL_PLAN_NAME
CURR_BILL_PLAN_START_DATE
EVER_PSTN_FEATURE_START_DATE
EVER_PSTN_FEATURE_END_DATE
EVER_PSTN_MONTH_APPLY_CANCEL_FLAG
DISC_TYPE_AM_IND
DISC_TYPE_AW_IND
DISC_TYPE_AD_IND
DISC_TYPE_DS_IND
DISC_TYPE_DM_IND
DISC_TYPE_DB_IND
DISC_TYPE_DO_IND
DISC_TYPE_DR_IND
DISC_TYPE_DU_IND
DISC_TYPE_DC_IND
DISC_TYPE_DP_IND
VIP_EXPIRY_DATE
VIP_BEFORE_EXP_MONTH
VIP_MSISDN_CHG_IND
PAY_PENALTY_DATE
DIRECT_STORE_PYMT_IND
CVS_PYMT_IND
VIRTUAL_CHANNEL_PYMT_IND
L3M_DIRECT_STORE_PYMT_IND
L3M_CVS_PYMT_IND
L3M_VIRTUAL_CHANNEL_PYMT_IND
HG_SEGMENT
P6M_MO_ONNET_CNT
P6M_MO_ONNET_DUR
P6M_MO_OFFNET_CNT
P6M_MO_OFFNET_DUR
P6M_MO_PSTN_CNT
P6M_MO_PSTN_DUR
L1M_CHANNEL_CHURN_INDEX
RETAIL_STORE_CHURN_FLAG
RETAIL_STORE_CHURN_SRV_DATE
RETAIL_STORE_CHURN_DEPUTY_FALG
RETAIL_STORE_CHURN_STOP_REASON
HS_USE_MONTH
CURR_DEVICE_MAKER
CURR_DEVICE_MODEL
CURR_DEVICE_PRICE_TIER
L1M_DEVICE_TENURE
L1M_DEVICE_MAKER
L1M_DEVICE_MODEL
L1M_DEVICE_PRICE_TIER
L1M_DEVICE_TYPE
L2M_DEVICE_TENURE
L2M_DEVICE_MAKER
L2M_DEVICE_MODEL
L2M_DEVICE_PRICE_TIER
L2M_DEVICE_TYPE
ZONE_ACTV_IVR_COUNTRY
ZONE_ACTV_IVR_REGION
STORE_TYPE
SPAUTH_IND
PTY_EVER_PO_CNT
PTY_EVER_PP_CNT
ANOTHER_ACTIVE_VD
ANOTHER_ACTIVE_D
PTY_CBU_EBU_PO_CNT
PTY_CBU_PO_CNT
PTY_CBU_PO_V_CNT
PTY_CBU_PO_VD_CNT
PTY_CBU_PO_D_CNT
PTY_EBU_PO_CNT
PTY_PO_ALL_CNT
L6M_AVG_NET_INV_AMT
L1M_NET_INV_AMT
L2M_NET_INV_AMT
W2P_SMS_MO_INT_CNT
SMS2P_SMS_MO_CNT
DATA_RATING_USAGE_MB
P6M_AVG_NET_INV_AMT
L1M_GPRS_AMT
L2M_GPRS_AMT
L6M_AVG_GPRS_AMT
L6M_AVG_VAS_MB
W2P_SMS_MO_CNT
W2P_SMS_MO_ONNET_CNT
W2P_SMS_MO_OFFNET_CNT
L1M_DATA_USAGE_MB
L2M_DATA_USAGE_MB
P6M_AVG_DATA_USAGE_MB
P1M_MO_ONNET_CNT
P1M_MO_ONNET_DUR
P1M_MO_OFFNET_CNT
P1M_MO_OFFNET_DUR
P1M_MO_PSTN_CNT
P1M_MO_PSTN_DUR
CURR_BILL_PLAN_NAME
"""


# In[12]:


# 因為之後telegram的會併入新的表 原本的有問題
drop_str += telegram_str
drop_list = drop_str.split("\n")
drop_list = [x for x in drop_list if x != ""]


# In[13]:

# for col in drop_list:
#     try:
#         df = df.drop(col, axis = 1)
#     except:
#         print("col = %s is not in this table" % col)


# In[14]:

want_cols = list(set(df.columns)-set(drop_list))


# In[13]:

try:
    # read csv file and print cost time
    t0 = time.time()
    # df = pd.read_csv(relative_filename, error_bad_lines=False)
    # df = pd.read_csv(relative_filename, usecols = wants_cols, sep  = '\t', error_bad_lines=False)
    logger.info("QUERY STR => %s" % query_str + query_where)
    logger.info("START QUERY => %s" % query_str + query_where)
    print("START QUERY => %s" % query_str + query_where)
    df = pd.read_sql(query_str + query_where, con)
    # df = pd.read_csv(MDS_FILE, sep  = ',', error_bad_lines=False, usecols=want_cols)

    logger.info("time for read csv: %.2f" % (time.time()-t0))
    logger.info("finish read MDS csv")
except Exception as e:
    logger.error(e) #写入错误日志


# In[14]:

df = df.fillna('?')


# # replace space/? to random value

# In[15]:

logger.info("start replace space/? to random value")

random_fill_str = """
GENDER_CODE
IMEI_MFG_NAME
IMEI_MKT_NAME
ZONE_ACTIVATION_IVR
ACTV_STORE_ID
MOST_MO_OPERATOR
MOST_MT_OPERATOR
PROM_CURR_EXP_MONTH_CNT
PROM_CURR_PROM_CODE
"""
random_fill_list = random_fill_str.split("\n")
random_fill_list = [x for x in random_fill_list if x != ""]
# random_fill_list


# In[16]:

try:
    question_item = ["?", " "]
    for col in random_fill_list:
        for q_item in question_item:
            q_item_count = len(df[df[col] == q_item])
    #         print("'"+ q_item + "' count =", q_item_count)
            if q_item_count > 0:
                sample_list = df[df[col] != q_item].sample(q_item_count)
                df.loc[df[df[col] == q_item].index, col] = sample_list[col].values
    #     print("? count =", len(df[df[col] == "?"]))
    #     print("space count =", len(df[df[col] == " "]))
    #     print(col, "done")
except Exception as e:
    logger.error(e) #写入错误日志


# # fill up the specific value

# In[17]:

# specific_fill_str = """
# PROM_CURR_PROMOTION_TYPE
# PROM_CURR_PROMOTION_SUB_TYPE
# PROM_ACTV_PROM_SUB_TYPE
# LAST_CHANNEL_TYPE
# IMEI_BAND
# IMEI_TYPE
# """
# specific_fill_str = specific_fill_str.split("\n")
# specific_fill_list = [x for x in specific_fill_list if x != ""]
# specific_fill_list

specific_dict = {
    "PROM_CURR_PROMOTION_TYPE" : "others",
    "PROM_CURR_PROMOTION_SUB_TYPE" : "others",
    "PROM_ACTV_PROM_SUB_TYPE" : "others",
    "LAST_CHANNEL_TYPE" : "others",
    "IMEI_TYPE" : "Smart Phone",
    "VIP_TENURE" : 0,
    "P3M_MO_PSTN_DUR" : 0,
    "HS_CHG_CNT" : 0,
    "AVG_HS_USE_MONTH_EX_CURR" : 0,
    "PAY_PENALTY_AMT" : 0,
    "P3M_AVG_DATA_USAGE_MB" : 0,
    "P3M_MO_ONNET_CNT" : 0,
    "P3M_MO_ONNET_DUR" : 0,
    "P3M_MO_OFFNET_CNT" : 0,
    "P3M_MO_OFFNET_DUR" : 0,
    "P3M_MO_PSTN_CNT" : 0,
    "AVG_HS_USE_MONTH" : 0
#     "跟價格有關的負數補0" : 0
    
}


# In[18]:

try:
    logger.info("start fill up the specific value")
    for col, value in specific_dict.items():
        df.loc[df[df[col] == "?"].index, col] = value   
except Exception as e:
    logger.error(e) #写入错误日志


# In[ ]:




# # IMEI_BAND fill up 3G or 4G

# In[19]:

logger.info("start IMEI_BAND fill up 3G or 4G")
try:
    col = "IMEI_BAND"
    q_item_count = len(df[df[col] == "?"])
    if(q_item_count > 0):
        sample_list = df[(df[col] == "3G") | (df[col] == "4G")].sample(q_item_count)
        df.loc[df[df[col] == "?"].index, col] = sample_list 
except Exception as e:
    logger.error(e) #写入错误日志


# # TODO:ORIG_OPR_ID merge telegram 

# In[20]:

OPR_ID_dict = {
    "QWR" : "遠傳電信",
    "QW3" : "遠傳電信",
    "ARC" : "遠傳電信",
    "AMT" : "亞太電信",
    "AP4" : "亞太電信",
    "APT" : "亞太電信",
    "APW" : "亞太電信",
    "CH3" : "中華電信",
    "CH4" : "中華電信",
    "CHM" : "中華電信",
    "CHT" : "中華電信",
    "FE4" : "遠傳電信",
    "FET" : "遠傳電信",
    "KGT" : "遠傳電信",
    "MBT" : "台灣大哥大",
    "SPQ" : "遠傳電信",
    "TAT" : "台灣大哥大",
    "TFN" : "台灣大哥大",
    "TSC" : "台灣之星",
    "TW3" : "台灣大哥大",
    "TW4" : "台灣大哥大",
    "TWM" : "台灣大哥大",
    "VBT" : "台灣之星",
    "YZT" : "台灣之星"
}


# In[21]:

col = "ORIG_OPR_ID"
# d = dict(zip(unique_list, values))
df[col] = df[col].map(OPR_ID_dict)


# In[22]:

df[col] = df[col].fillna("?")


# In[ ]:




# # 補眾數欄位

# In[23]:

col = "BILL_CITY_NAME"
df.loc[df[df[col] == "?"].index, col] = df[col].describe().top


# In[24]:

col = "AGENCY_FLAG"
df.loc[df[df[col] == "?"].index, col] = df[col].describe().top


# # 補平均值

# In[25]:

logger.info("start age fill up avg")
col = "AGE"
try:
    avg = sum(df[df[col] != "?"][col].apply(np.int64)) / len(df[df[col] != "?"])
    df.loc[df[df[col] == "?"].index, col] = avg
except Exception as e:
    logger.error(e) #写入错误日志


# # AMT 如果是負數的話 補0

# In[26]:

logger.info("start age fill up avg")
try:
    for col in df.columns:
        if(col.endswith("AMT")):
    #         print(col)
    #         print(df[col].describe())
            df[col] = df[col].apply(np.float64)
            df.loc[df[df[col] < 0].index, col] = 0
except:
    logger.error(e) #写入错误日志


# # drop VAS

# In[27]:

logger.info("start drop vas") #写入错误日志

try:
    df = df.drop('VAS_AMT', axis = 1)
    df = df.drop('L3M_AVG_VAS_MB', axis = 1)
except:
    logger.error(e) #写入错误日志


# # combine 3大2小

# In[15]:

logger.info("start combine 3大2小")


# In[29]:

try:
    telegram_df = pd.read_csv(TELEGRAM_MT_FILE, error_bad_lines=False)
    telegram_df = telegram_df.drop("DATA_MONTH", axis = 1)
    df = pd.merge(df, telegram_df, on='MINING_DW_SUBSCR_NO', how='left')
except Exception as e:
    logger.error(e) #写入错误日志
#     write_to_log("telegram_mt_df  no month")


# In[28]:

try:
    telegram_df = pd.read_csv(TELEGRAM_MO_FILE, error_bad_lines=False)
    telegram_df = telegram_df.drop("DATA_MONTH", axis = 1)
    df = pd.merge(df, telegram_df, on='MINING_DW_SUBSCR_NO', how='left')
except Exception as e:
    logger.error(e) #写入错误日志
#     write_to_log("telegram_mo_df  no month")



# # 語音 mo + mt 

# In[25]:

try:
    logger.info("start combine CWC") #写入错误日志
    month_col_name = "DATA_MONTH"
    query_str = "sel * from CSM_PROJECT." + "CWC_CATG_CNT_VW"
    query_where = ' where  DATA_MONTH = ' + year + '%02d' % month
    logger.info("QUERY STR => %s" % query_str + query_where)
    logger.info("START QUERY => %s" % query_str + query_where)
    print("START QUERY => %s" % query_str + query_where)

    cwc_df = pd.read_sql(query_str + query_where, con)
    # cwc_df = pd.read_csv(CWC_FILE, error_bad_lines=False)
    # cwc_df = cwc_df[cwc_df["DATA_MONTH"] == int(DATA_MONTH)]
    logger.info("START Drop CURR_SUBSCR_ID and DATA_MONTH")
    cwc_df = cwc_df.drop("CURR_SUBSCR_ID", axis = 1)
    cwc_df = cwc_df.drop("DATA_MONTH", axis = 1)

    # if("Groups" in list(df.columns)):
    #     df = df.drop("Groups", axis = 1)
    df = pd.merge(df, cwc_df, on='MINING_DW_SUBSCR_NO', how='left')
except Exception as e:
    logger.error(e) #写入错误日志


# # Transfer to 相等深度(Equal-Frequency-Interval)裝箱法

# In[29]:

def tranferEFI(df_col, div_num = 3):
    return pd.qcut(df_col, div_num, labels=["L","M","H"], retbins = True)


# In[30]:

qcut_info = ""


# In[31]:

logger.info("START q_cut_cols")
try:
    q_cut_cols = ['DATA_USAGE_MB', 'MOC_DUR', 'MTC_DUR']
    for col in q_cut_cols:
        df[col], cut_info = tranferEFI(df[col])
        qcut_info += col + "\n" +str(cut_info) + "\n"
except Exception as e:
    logger.error(e) #写入错误日志


# In[32]:

# with open("./marketing_q_cut.txt", "w") as text_file:
#     text_file.write(qcut_info)


# # 0804信件說要刪除的部分

# In[37]:

write_to_log("start drop some cols")
mail_say_delete_str = """
DATA_RC_AMT
L1M_DATA_MONTHLY_FEE
MO_OFFNET_DUR
MO_ONNET_DUR
MOC_PSTN_DUR
MTC_CNT
NET_INV_AMT
VOICE_RC_AMT
"""
try:
    drop_list = mail_say_delete_str.split("\n")
    drop_list = [x for x in drop_list if x != ""]
    want_cols = list(set(df.columns)-set(drop_list))
    df = df[want_cols]
except Exception as e:
    logger.error(e) #写入错误日志


# In[38]:

logger.info("start load GROUP ID FILE")
try:
    group_df = pd.read_csv(GROUP_ID_FILE, error_bad_lines=False, usecols = ["MINING_DW_SUBSCR_NO", "Groups"])
    if("Groups" in list(df.columns)):
        df = df.drop("Groups", axis = 1)
    df = pd.merge(df, group_df, on='MINING_DW_SUBSCR_NO', how='right')
except Exception as e:
    logger.error(e) #写入错误日志


# In[39]:

# df.to_csv(path + out_filename + "with_id.csv", index=False, encoding='utf-8')


# In[40]:

logger.info("start drop MINING_DW_SUBSCR_NO")
try:
    df = df.drop("MINING_DW_SUBSCR_NO", axis = 1)
except Exception as e:
    logger.error(e) #写入错误日志


# In[42]:

# write_to_log("start output file %s" % OUT_FILENAME)
logger.info("start drop MINING_DW_SUBSCR_NO")
print("start output file %s", OUT_FILENAME)
try:
    t0 = time.time()
    df.to_csv(OUT_FILENAME, index=False, encoding='utf-8')
    logger.info("start drop MINING_DW_SUBSCR_NO")
except Exception as e:
    logger.error(e) #写入错误日志


# In[43]:

print("finish marketing_filter_columns.py")
# write_to_log("finish marketing_filter_columns.py")
logger.info("finish marketing_filter_columns.py")


# In[ ]:

# from mailerWithUtf8 import mail
# test=mail()
# test.main("finished", "")

