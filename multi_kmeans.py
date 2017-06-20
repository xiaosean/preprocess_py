import numpy as np
import pandas as pd
from time import time
from sklearn.cluster import KMeans
from pandas.computation import expressions as expr
from bokeh.charts import Line, show, output_file, save
import pprint as pp
import sys
from bokeh.palettes import Spectral11

# set configure
# path = "./CDR_NORMALIZE_CONCAT/"
path = "./CDR_ANALYZE/"
# path = "./CDR_CONCAT/"
filename = sys.argv[1]
# filename = "CDR_CONCAT_TABLE_4_max_min.csv"
# filename = "CDR_CONCAT_TABLE_4.csv"
relative_filename = path + filename  #+ ".csv"
# out_filename = "mds_mly_minus20160901"
# after the numeric_st_idx's number will be tranform to int64
# numeric_st_idx = 1
# n_clusters = 8

# read revise csv file and print cost time
# just load 5 data 
t0 = time()
df = pd.read_csv(relative_filename, error_bad_lines=False)
print("time for read csv: %.2f" % (time()-t0))

# select columns
# df = df[['VOICE_MO_HOUR_0_TIME','VOICE_MO_HOUR_1_TIME','VOICE_MO_HOUR_2_TIME','VOICE_MO_HOUR_3_TIME','VOICE_MO_HOUR_4_TIME','VOICE_MO_HOUR_5_TIME','VOICE_MO_HOUR_6_TIME','VOICE_MO_HOUR_7_TIME','VOICE_MO_HOUR_8_TIME','VOICE_MO_HOUR_9_TIME','VOICE_MO_HOUR_10_TIME','VOICE_MO_HOUR_11_TIME','VOICE_MO_HOUR_12_TIME','VOICE_MO_HOUR_13_TIME','VOICE_MO_HOUR_14_TIME','VOICE_MO_HOUR_15_TIME','VOICE_MO_HOUR_16_TIME','VOICE_MO_HOUR_17_TIME','VOICE_MO_HOUR_18_TIME','VOICE_MO_HOUR_19_TIME','VOICE_MO_HOUR_20_TIME','VOICE_MO_HOUR_21_TIME','VOICE_MO_HOUR_22_TIME','VOICE_MO_HOUR_23_TIME']]
# df = df[['mo_workday_time','mo_holiday_time','mt_workday_time','mt_holiday_time']]
df = df.drop('MINING_DW_SUBSCR_NO', 1)
# drop_col_list = []
# for col in df.columns:
#     if str(col).find("TIME") == -1 and str(col).find("time") == -1:
#         drop_col_list.append(str(col))
# df = df.drop(drop_col_list, 1)

"""
for K in range(6, 15):
	n_clusters = K
	kmeans = KMeans(n_clusters=n_clusters, max_iter = 30000).fit(df.values)
	np.save("label_K" + str(K) + ".npy", kmeans.labels_)
"""
# """		get label marker
for K in range(6, 15):
	n_clusters = K
	labels_ = np.load("label_K" + str(K) + ".npy")
	# data count in each cluster
	cluster_result = {}
	for i in range(n_clusters):
	    cluster_result[i] = 0

	# for l in kmeans.labels_:
	for l in labels_:
	    cluster_result[l] += 1
	# pp.pprint(cluster_result)

	df['label'] = labels_
	# df['label'] = kmeans.labels_

	# aggregate display data
	data = {}
	grouped = df.groupby('label')
	for i in range(n_clusters):
		data[str(cluster_result[i])] = grouped.mean().values[i]

	pp.pprint(df.columns)

	# select label
	# xl = str(df.columns)
	# xl = "MO_0_24 MT_0_24 MO_SUN_SAT_w_h MT_SUN_SAT_w_h"
	xl = "hour"
	if filename.find("WORK") != -1:
		xl = str(df.columns)
	elif filename.find("HOUR") == -1:
		xl = "SUN ~ SAT"

	yl = "time"
	if filename.find("TIME") == -1:
		yl = "count"

	# draw
	# set line colors
	mycolors = []
	if n_clusters > 5:
		mycolors = Spectral11[0:5] + Spectral11[6:n_clusters]
	else:
		mycolors = Spectral11[0:n_clusters]
	line = Line(data, ylabel = 'mean ' + yl, xlabel = xl, color = mycolors)
	# line = Line(data, ylabel = 'mean ' + sys.argv[2], xlabel = xl)

	# save file
	# output_file("test_K" + str(i + 1) + ".html")
	output_file("./CDR_CONCAT_ANALYZE_GRAPH/" + filename[:-4] + "_K" + str(K) + "_distribution.html")

	save(line)
	# show(line)
# """		#get label marker