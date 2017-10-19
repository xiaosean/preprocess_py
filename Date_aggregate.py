
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


# In[15]:

def read_csv(filename):
    # read revise csv file and print cost time
    t0 = time.time()
    df = pd.read_csv(filename, error_bad_lines=False)
    write_to_log("time for read csv file: %.2f" % (time.time()-t0))
    return df


# In[16]:

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


# In[17]:

def save_dataframe(df, out_filename):
   # write to csv and no index
    t0 = time.time()
    # aggr_df.to_csv(out_filename + ".csv", index=False, encoding='utf-8')
    df.to_csv(out_filename + ".csv", encoding='utf-8')
#     print("time for output csv file: %.2f" % (time.time()-t0))
    write_to_log("time for output csv file: %.2f" % (time.time()-t0))


# In[18]:

def get_table_path():
    with open('./preprocess_path_file.txt') as f:
        read_data = f.read()
        read_data = read_data.replace("\r","")
        read_data = read_data.replace('"',"")
        read_data = read_data.replace("\n","")
    table_list = read_data.split(",")
    table_dict = {}
    for table in table_list:
        table_name, table_path = table.split("=")
        table_dict[table_name] = table_path
    return table_dict


# In[19]:

def write_to_log(msg):
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(time.time()))
    with open("log.txt", "a") as log_file:
        log_file.write(current_time + "\t" + msg + "\n")


# In[ ]:




# In[20]:

print("Start Date_aggregate.py")
write_to_log("Start Date_aggregate.py")
write_to_log("Start load path configure")
table_dict = get_table_path()
NEED_AGGR_CSV_PATH = table_dict["NEED_AGGR_CSV_PATH"]
month = table_dict["MONTH"]
write_to_log("Finish load path configure")


# In[21]:

con = pyodbc.connect('Driver=Teradata;DBCName=10.68.64.141;UID=V_CSM;PWD=qazwsx')
con.setencoding(encoding = 'utf-8')


# In[22]:

# set configure
# path = "../DATA_FULL/"
# path = "./CDR_MONTHLY/"
path = NEED_AGGR_CSV_PATH
# filename = "dm_subscr_moc_mly_COMPLETED_revise_month_4"
# relative_filename = path + filename + ".csv"

out_path = "./CDR_MONTHLY_AGGR/"
if not os.path.exists(out_path):
    print("no dir -> CDR_MONTHLY_AGGR  make a dir")
    os.mkdir(out_path)


# In[ ]:




# In[27]:

# for filename in file_csv_list(path):
#     if ".csv" in filename:

month_col_name = "DATA_MONTH"
query_str = "sel * from CSM_PROJECT." + "dm_subscr_moc_mly"
query_where = ' where extract(month from DATA_MONTH) = ' + month
# filename_none_postfix = filename[:-4]
out_filename =  out_path + "dm_subscr_moc_mly_COMPLETED_month"
# df = read_csv(path + filename)
df = pd.read_sql(query_str + query_where, con)
# df = remove_date_column(df)
df = df.groupby('MINING_DW_SUBSCR_NO').sum()
save_dataframe(df, out_filename)


# In[25]:

month_col_name = "DATA_MONTH"
query_str = "sel * from CSM_PROJECT." + "dm_subscr_mtc_mly"
query_where = ' where extract(month from DATA_MONTH) = ' + month
# filename_none_postfix = filename[:-4]
out_filename =  out_path + "dm_subscr_mtc_mly_COMPLETED_month"
df = pd.read_sql(query_str + query_where, con)
# df = read_csv(path + filename)
# df = remove_date_column(df)
df = df.groupby('MINING_DW_SUBSCR_NO').sum()
save_dataframe(df, out_filename)


# In[26]:

print("Finish Date_aggregate.py")
write_to_log("Finish Date_aggregate.py")


# In[ ]:



