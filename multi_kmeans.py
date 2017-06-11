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
path = "./CDR_CONCAT/"
filename = "CDR_CONCAT_TABLE_4"
relative_filename = path + filename + ".csv"
# out_filename = "mds_mly_minus20160901"
# after the numeric_st_idx's number will be tranform to int64
numeric_st_idx = 1
n_clusters = 8

# read revise csv file and print cost time
# just load 5 data 
t0 = time()
df = pd.read_csv(relative_filename, error_bad_lines=False)
print("time for read csv: %.2f" % (time()-t0))

# select columns
df = df[['VOICE_MO_HOUR_0_TIME','VOICE_MO_HOUR_1_TIME','VOICE_MO_HOUR_2_TIME','VOICE_MO_HOUR_3_TIME','VOICE_MO_HOUR_4_TIME','VOICE_MO_HOUR_5_TIME','VOICE_MO_HOUR_6_TIME','VOICE_MO_HOUR_7_TIME','VOICE_MO_HOUR_8_TIME','VOICE_MO_HOUR_9_TIME','VOICE_MO_HOUR_10_TIME','VOICE_MO_HOUR_11_TIME','VOICE_MO_HOUR_12_TIME','VOICE_MO_HOUR_13_TIME','VOICE_MO_HOUR_14_TIME','VOICE_MO_HOUR_15_TIME','VOICE_MO_HOUR_16_TIME','VOICE_MO_HOUR_17_TIME','VOICE_MO_HOUR_18_TIME','VOICE_MO_HOUR_19_TIME','VOICE_MO_HOUR_20_TIME','VOICE_MO_HOUR_21_TIME','VOICE_MO_HOUR_22_TIME','VOICE_MO_HOUR_23_TIME']]
# df = df[['mo_workday_time','mo_holiday_time','mt_workday_time','mt_holiday_time']]


for K in range(8, 9):
	n_clusters = K
	kmeans = KMeans(n_clusters=n_clusters, max_iter = 3000).fit(df.values)

	# data count in each cluster
	cluster_result = {}
	for i in range(n_clusters):
	    cluster_result[i] = 0

	for l in kmeans.labels_:
	    cluster_result[l] += 1
	pp.pprint(cluster_result)

	df['label'] = kmeans.labels_

	# aggregate display data
	data = {}
	grouped = df.groupby('label')
	for i in range(n_clusters):
		data[str(cluster_result[i])] = grouped.mean().values[i]

	print(df.columns)

	# select label
	xl = "hour"
	# if sys.argv[1].find("HOUR") == -1:
	# 	xl = "week day"

	# draw
	# set line colors
	mycolors = Spectral11[0:n_clusters - 1]
	line = Line(data, ylabel = 'mean ' + 'time', xlabel = xl, line_color = mycolors)
	# line = Line(data, ylabel = 'mean ' + sys.argv[2], xlabel = xl)

	# save file
	output_file("test_K" + str(i + 1) + ".html")
	# output_file(sys.argv[1][:-4] + "_" + sys.argv[2] + "_distribution.html")

	# save(line)
	show(line)