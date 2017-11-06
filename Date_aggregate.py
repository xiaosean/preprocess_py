
# coding: utf-8

# In[13]:

import os.path
import numpy as np
import pandas as pd
import time
import os
from os import listdir
from os.path import isfile, join
import pyodbc


# In[14]:

def file_csv_list(target_path):
    return [f for f in listdir(target_path) if isfile(join(target_path, f))]


# In[3]:

def read_csv(filename):
    logger.info("start read filename %s" % filename) #写入错误日志

    # read revise csv file and print cost time
    t0 = time.time()
    df = pd.read_csv(filename, error_bad_lines=False)
    write_to_log("time for read csv file: %.2f" % (time.time()-t0))
    logger.info("time for read csv file: %.2f" % (time.time()-t0)) #写入错误日志

    return df


# In[4]:

def remove_date_column(df):
    # we don't use VOICE_DATE/VOICE_MONTH bcz it is a monthly data
    if("VOICE_DATE" in df.columns):
        df = df.drop('VOICE_DATE', 1)
#         print("Drop VOICE_DATE")
    if("VOICE_MONTH" in df.columns):
        df = df.drop('VOICE_MONTH', 1)
#         print("Drop VOICE_MONTH")
    if("DATA_MONTH" in df.columns):
        df = df.drop('DATA_MONTH', 1)
#         print("Drop DATA_MONTH")
    return df


# In[5]:

def save_dataframe(df, out_filename):
    logger.info("start save dataframe %s" % filename) #写入错误日志

   # write to csv and no index
    t0 = time.time()
    # aggr_df.to_csv(out_filename + ".csv", index=False, encoding='utf-8')
    df.to_csv(out_filename + ".csv", encoding='utf-8')
#     print("time for output csv file: %.2f" % (time.time()-t0))
    write_to_log("time for output csv file: %.2f" % (time.time()-t0))
    logger.info("time for output csv file: %.2f" % (time.time()-t0)) #写入错误日志


# In[6]:

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
    


# In[19]:

def write_to_log(msg):
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(time.time()))
    with open("log.txt", "a") as log_file:
        log_file.write(current_time + "\t" + msg + "\n")


# # Logger config

# In[1]:


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


# In[20]:

print("Start Date_aggregate.py")
logger.info("Start Date_aggregate.py")
logger.info("Date_csv_config")
write_to_log("Start Date_aggregate.py")
write_to_log("Start load path configure")
table_dict = get_table_path()
NEED_AGGR_CSV_PATH = table_dict["NEED_AGGR_CSV_PATH"]
month = table_dict["MONTH"]
write_to_log("Finish load path configure")


# In[7]:

logger.info("Start connect ODBC")
try:
    con = pyodbc.connect('Driver=Teradata;DBCName=10.68.64.141;UID=V_CSM;PWD=qazwsx')
    con.setencoding(encoding = 'utf-8')
except Exception as e:
    logger.error(e) #写入错误日志


# In[22]:

# set configure
# path = "../DATA_FULL/"
# path = "./CDR_MONTHLY/"
# path = NEED_AGGR_CSV_PATH
# filename = "dm_subscr_moc_mly_COMPLETED_revise_month_4"
# relative_filename = path + filename + ".csv"
logger.info("check out path")

out_path = "./CDR_MONTHLY_AGGR/"
if not os.path.exists(out_path):
    logger.info("no dir -> CDR_MONTHLY_AGGR  make a dir")
    print("no dir -> CDR_MONTHLY_AGGR  make a dir")
    os.mkdir(out_path)


# In[ ]:




# In[27]:

# for filename in file_csv_list(path):
#     if ".csv" in filename:
try:
    month_col_name = "DATA_MONTH"
    query_str = "sel * from CSM_PROJECT." + "dm_subscr_moc_mly"
    query_where = ' where extract(month from DATA_MONTH) = ' + month
    # filename_none_postfix = filename[:-4]
    out_filename =  out_path + "dm_subscr_moc_mly_COMPLETED_month"
    # df = read_csv(path + filename)
    logger.info("QUERY STR => %s" % query_str + query_where)
    logger.info("START QUERY => %s" % query_str + query_where)
    print("START QUERY => %s" % query_str + query_where)
    df = pd.read_sql(query_str + query_where, con)
    # df = remove_date_column(df)
    logger.info("START groupby MINING_DW_SUBSCR_NO sum")
        print("START groupby by=> MINING_DW_SUBSCR_NO")

    df = df.groupby('MINING_DW_SUBSCR_NO').sum()
    save_dataframe(df, out_filename)
except Exception as e:
    logger.error(e) #写入错误日志


# In[25]:

try:

    month_col_name = "DATA_MONTH"
    query_str = "sel * from CSM_PROJECT." + "dm_subscr_mtc_mly"
    query_where = ' where extract(month from DATA_MONTH) = ' + month
    # filename_none_postfix = filename[:-4]
    out_filename =  out_path + "dm_subscr_mtc_mly_COMPLETED_month"
    logger.info("QUERY STR => %s" % query_str + query_where)
    logger.info("START QUERY => %s" % query_str + query_where)
    print("START QUERY => %s" % query_str + query_where)
    df = pd.read_sql(query_str + query_where, con)
    # df = read_csv(path + filename)
    # df = remove_date_column(df)
    logger.info("START groupby MINING_DW_SUBSCR_NO sum")
    print("START groupby by=> MINING_DW_SUBSCR_NO")
    df = df.groupby('MINING_DW_SUBSCR_NO').sum()
    save_dataframe(df, out_filename)
except Exception as e:
    logger.error(e) #写入错误日志


# In[26]:

print("Finish Date_aggregate.py")
# write_to_log("Finish Date_aggregate.py")
logger.info("Finish Date_aggregate.py")


# In[ ]:



