
# coding: utf-8

# In[10]:

import numpy as np
import pandas as pd
from time import time
from sklearn.cluster import KMeans
from pandas.computation import expressions as expr
from bokeh.charts import Line, show, output_file, save, BoxPlot
import pprint as pp
import sys
from bokeh.palettes import Spectral11, Category10
from bokeh.layouts import row


# In[4]:

# set configure
# path = "./CDR_NORMALIZE_CONCAT/"
path = "./CDR_FINAL/"
# path = "./CDR_ANALYZE/"
# path = "./CDR_CONCAT/"
filename = "table_with_kid_all_0625.csv"
# filename = sys.argv[1]
# filename = "TABLE_4_MT_WORKDAY_AVG_TIME_COLS.csv"
# filename = "CDR_CONCAT_TABLE_4_max_min.csv"
# filename = "CDR_CONCAT_TABLE_4.csv"
relative_filename = path + filename  #+ ".csv"
# out_filename = "mds_mly_minus20160901"
# after the numeric_st_idx's number will be tranform to int64
# numeric_st_idx = 1
# n_clusters = 8
label_path = "./kmean_label/"


# In[5]:

# read revise csv file and print cost time
# just load 5 data 
t0 = time()
df = pd.read_csv(relative_filename, error_bad_lines=False)
print("time for read csv: %.2f" % (time()-t0))


# In[6]:

# select columns
# df = df[['VOICE_MO_HOUR_0_TIME','VOICE_MO_HOUR_1_TIME','VOICE_MO_HOUR_2_TIME','VOICE_MO_HOUR_3_TIME','VOICE_MO_HOUR_4_TIME','VOICE_MO_HOUR_5_TIME','VOICE_MO_HOUR_6_TIME','VOICE_MO_HOUR_7_TIME','VOICE_MO_HOUR_8_TIME','VOICE_MO_HOUR_9_TIME','VOICE_MO_HOUR_10_TIME','VOICE_MO_HOUR_11_TIME','VOICE_MO_HOUR_12_TIME','VOICE_MO_HOUR_13_TIME','VOICE_MO_HOUR_14_TIME','VOICE_MO_HOUR_15_TIME','VOICE_MO_HOUR_16_TIME','VOICE_MO_HOUR_17_TIME','VOICE_MO_HOUR_18_TIME','VOICE_MO_HOUR_19_TIME','VOICE_MO_HOUR_20_TIME','VOICE_MO_HOUR_21_TIME','VOICE_MO_HOUR_22_TIME','VOICE_MO_HOUR_23_TIME']]
# df = df[['mo_workday_time','mo_holiday_time','mt_workday_time','mt_holiday_time']]
# df = df.drop('MINING_DW_SUBSCR_NO', 1)
# drop_col_list = []
# for col in df.columns:
#     if str(col).find("TIME") == -1 and str(col).find("time") == -1:
#         drop_col_list.append(str(col))
# df = df.drop(drop_col_list, 1)


# ---------------------------------
for c in df.columns[8:]:
	df = df.drop(c, 1)

# del_col = ['MINING_DW_SUBSCR_NO','VOICE_MT_workday_cnt','VOICE_MT_workday_time','VOICE_MT_holiday_cnt','VOICE_MT_holiday_time']
del_col = ['MINING_DW_SUBSCR_NO']
for c in del_col:
	df = df.drop(c, 1)
# --------------------------------------



# In[7]:

# for K in range(10, 11):
K = 8
n_clusters = K
labels_ = np.load(label_path + "label_K8__all_max_min_0625_voice.npy")
# labels_ = np.load(label_path + "label_K" + str(K) + ".npy")
# labels_ = np.load(label_path + "label_K" + str(K) + "_mini.npy")
# data count in each cluster
cluster_result = {}
for i in range(n_clusters):
    cluster_result[i] = 0

# for l in kmeans.labels_:
for l in labels_:
    cluster_result[l] += 1
# pp.pprint(cluster_result)

df['label'] = labels_


# In[8]:

# grouped = df.groupby('label')


# In[9]:

# grouped.describe()


# In[ ]:

boxes = []
for c in df.columns[:-1]:
    box = BoxPlot(df, values = c, label = 'label', color = 'label')
    boxes.append(box)

# output_file("./CDR_CONCAT_ANALYZE_GRAPH/" + filename[:-4] + "_K" + str(K) + "_boxplot.html")
output_file("./CDR_CONCAT_ANALYZE_GRAPH_MINI/" + filename[:-4] + "_K" + str(K) + "_boxplot.html")

show(row(boxes))
# save(row(boxes))

# In[ ]:



