import numpy as np
import pandas as pd
from time import time
from sklearn.cluster import KMeans, MiniBatchKMeans
from pandas.computation import expressions as expr
# from bokeh.charts import Line, show, output_file, save
import pprint as pp
import sys
import os
# from bokeh.palettes import Spectral11

# set configure
# path = "./CDR_FINAL_NORMALIZE/"
path = "./CDR_FINAL/"
# path = "./dna_Data/"
# path = "./CDR_ANALYZE/"
# path = "./CDR_CONCAT/"
filename = sys.argv[1]
# filename = 'DNA_daily_april_div_30.csv'
# filename = 'table_with_kid_all_max_min_0625.csv'
# filename = "CDR_CONCAT_TABLE_4_max_min.csv"
# filename = "CDR_CONCAT_TABLE_4_log10.csv"
# filename = "CDR_CONCAT_TABLE_4_z_norm.csv"
# filename = "CDR_CONCAT_TABLE_4.csv"
relative_filename = path + filename  #+ ".csv"

label_output_path = "./kmean_label/"

# read revise csv file and print cost time
# just load 5 data 
t0 = time()
df = pd.read_csv(relative_filename, error_bad_lines=False)
print("time for read csv %s: %.2f" % (filename, time()-t0))

# for c in df.columns[8:]:
# 	df = df.drop(c, 1)

# del_col = ['MINING_DW_SUBSCR_NO','VOICE_MT_workday_cnt','VOICE_MT_workday_time','VOICE_MT_holiday_cnt','VOICE_MT_holiday_time']
del_col = ['MINING_DW_SUBSCR_NO']
for c in del_col:
	df = df.drop(c, 1)

# # -------------------------
# for c in df.columns:
# 	if "time" in c:
# 		df = df.drop(c, 1)
# # ----------------------------

# df = df.fillna(0)
# df = df.replace(np.inf, 0)

rows = df.iloc

scores = {}
scores_square = {}
# for K in range(12, 13):
for K in range(2, 15):
	t0 = time()
	kmeans = KMeans(n_clusters=K, max_iter = 3000000).fit(df.values)
	# kmeans = MiniBatchKMeans(n_clusters=n_clusters, max_iter = 3000000).fit(df.values)
	# np.save(label_output_path + "label_K" + str(K) + ".npy", kmeans.labels_)
	# np.save(label_output_path + "label_K" + str(K) + "_log10.npy", kmeans.labels_)
	# np.save(label_output_path + "label_K" + str(K) + "_znorm.npy", kmeans.labels_)
	# np.save(label_output_path + "label_K" + str(K) + "_" + filename[14:-4] + ".npy", kmeans.labels_)
	np.save(label_output_path + "label_K" + str(K) + "_" + filename[14:-4] + "_06281.npy", kmeans.labels_)
	np.save(label_output_path + "center_K" + str(K) + "_" + filename[14:-4] + "_06281.npy", kmeans.cluster_centers_)
	# np.save(label_output_path + "label_K" + str(K) + "_mini.npy", kmeans.labels_)
	scores[K] = kmeans.inertia_
	print("time for kmean %d: %.2f" % (K, time()-t0))
	print(kmeans.inertia_)

	sum_of_square = 0
	for i in range(len(df)):
		sum_of_square += np.sum((kmeans.cluster_centers_[:] - rows[i].values[:])**2)

	scores_square[K] = 1/sum_of_square

print("scores: ")
print(scores)

os.system("python kmeans_error.py " + str(scores).replace(" ", "") + " " + filename[:-4])
os.system("python kmeans_error.py " + str(scores_square).replace(" ", "") + " " + filename[:-4] + "_square")