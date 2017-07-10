import numpy as np
import pandas as pd
from time import time
from sklearn.cluster import KMeans
from pandas.computation import expressions as expr
from bokeh.charts import Line, show, output_file, save
import pprint as pp
import sys
from bokeh.palettes import Spectral11, Category20
from bokeh.layouts import row


# set configure
# path = "./CDR_NORMALIZE_CONCAT/"
path = "C:/Users/VIPLAB/Desktop/XIAO SEAN/"
# path = "./dna_Data/"
# path = "./CDR_FINAL/"
# path = "./CDR_ANALYZE/"
# path = "./CDR_CONCAT/"
# filename = sys.argv[1]
# filename = "CDR_CONCAT_TABLE_4_max_min.csv"
# filename = "category_dna_voice_median.csv"
filename = "category_dna_voice_means.csv"
# filename = 'DNA_daily_april_div_30.csv'
# filename = "table_with_kid_all_0625.csv"
# relative_filename = path + filename  #+ ".csv"
relative_filename = filename  #+ ".csv"
# out_filename = "mds_mly_minus20160901"
# after the numeric_st_idx's number will be tranform to int64
# numeric_st_idx = 1
# K = 8
label_path = "./kmean_label/"
output_path = "./CDR_CONCAT_ANALYZE_GRAPH/"
# output_path = "./CDR_CONCAT_ANALYZE_GRAPH_MINI/"

# read revise csv file and print cost time
# just load 5 data_VOICE 
t0 = time()
df = pd.read_csv(relative_filename, error_bad_lines=False)
print("time for read csv: %.2f" % (time()-t0))

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
# for c in df.columns[8:]:
# 	df = df.drop(c, 1)

# # del_col = ['MINING_DW_SUBSCR_NO','VOICE_MT_workday_cnt','VOICE_MT_workday_time','VOICE_MT_holiday_cnt','VOICE_MT_holiday_time']
# del_col = ['MINING_DW_SUBSCR_NO']
# for c in del_col:
# 	df = df.drop(c, 1)
# --------------------------------------


# """		get label marker
# for K in range(8, 16):
# for K in range(12, 13):
K = len(df)
# labels_ = np.load("CDR_CONCAT_ANALYZE_GRAPH_FULL1/" + "label_K" + str(K) + ".npy")
# labels_ = np.load(label_path + "label_K" + str(K) + ".npy")
# labels_ = np.load(label_path + "label_K12__all_max_min_0625_voice.npy")
# labels_ = df['groups']
# labels_ = np.load(label_path + "label_K" + str(K) + "_log10.npy")
# labels_ = np.load(label_path + "label_K" + str(K) + "_mini.npy")
# data_VOICE count in each cluster
# cluster_result = {}
# for i in range(K):
    # cluster_result[i] = 0

# for l in kmeans.labels_:
# for l in labels_:
    # cluster_result[l] += 1
# pp.pprint(cluster_result)

# print("numpy len: ", len(labels_))
# print("df len: ", len(df))
# df['label'] = labels_
# df['label'] = kmeans.labels_

cluster_name = {1012:'每通通話量長', 	1470990:'幾乎不用', 	23626:'高度使用', 	283083:'有在使用', 	48456:'夜貓族', 	3601:'超高度使用',	68665:'中度使用', 	697364:'稍微使用'}

# aggregate display data_VOICE
data_VOICE = {}
data_DNA = {}
grouped = df.groupby('Groups')
group_count = grouped[df.columns[1]].count().values

for i in range(K):
	# data_VOICE[str(i)] = grouped.mean().values[i]
	# if "HOUR" in filename:
		# data_VOICE[cluster_name[cluster_result[i]] + "(" + str(cluster_result[i]) + ")"] = list(map(lambda x: x/30,grouped.mean().values[i]))
		# data_VOICE["(" + str(group_count[i]) + ")"] = list(map(lambda x: x/30,grouped.mean().values[i]))
		# data_VOICE["(" + str(group_count[i]) + ")"] = grouped.mean().values[i][:24]
	# else:
		# data_VOICE[cluster_name[cluster_result[i]] + "(" + str(cluster_result[i]) + ")"] = list(map(lambda x: x/4,grouped.mean().values[i]))
		# data_VOICE["(" + str(group_count[i]) + ")"] = list(map(lambda x: x/4,grouped.mean().values[i]))
		# data_VOICE["(" + str(group_count[i]) + ")"] = grouped.mean().values[i][:24]

	# data_VOICE[str(group_count[i])] = grouped.mean().values[i][:24]
	# data_DNA[str(group_count[i])] = grouped.mean().values[i][24:]

	data_VOICE[str(grouped.mean().index[i])] = grouped.mean().values[i][:24]
	data_DNA[str(grouped.mean().index[i])] = grouped.mean().values[i][24:]

pp.pprint(df.columns)

# select label
# xl = str(df.columns)
# xl = "MO_0_24 MT_0_24 MO_SUN_SAT_w_h MT_SUN_SAT_w_h"
xl = "hour"
# if filename.find("WORK") != -1:
# 	xl = str(df.columns)
# elif filename.find("HOUR") == -1:
# 	xl = "SUN      ~      SAT"

yl = "percentage"
# yl = "time"
# if filename.find("TIME") == -1:
# 	yl = "count"

# draw
# # set line_VOICE colors
# mycolors = []
# # if K > 5:
# # 	mycolors = Spectral11[0:5] + Spectral11[6:K + 1]
# # else:
# # 	mycolors = Spectral11[0:K]
# for i in range(K):
# 	mycolors.append(Spectral11[i * 2])

# if "MO" in filename:
# 	title += "MO "
# if "MT" in filename:
# 	title += "MT "

# if "DAY" in filename:
# 	title += "DAY "
# if "HOUR" in filename:
# 	title += "HOUR "

# if "CNT" in filename:
# 	title += "COUNT"
# if "TIME" in filename:
# 	title += "TIME"

title = "VOICE 24Hr distribution"

line_VOICE = Line(data_VOICE, ylabel = yl, xlabel = xl, color = Category20[20], title = title)
# line_VOICE = line_VOICE(data_VOICE, ylabel = 'mean ' + sys.argv[2], xlabel = xl)
# line_VOICE.legend.orientation = 'horizontal'
# legend = line_VOICE.legend
# legend.plot = None
# legend.location = (0 , 600)
# line_VOICE.add_layout(legend[0], "right")
# line_VOICE.xaxis.axis_label_text_font_size = '20px'
# line_VOICE.yaxis.axis_label_text_font_size = '20px'
# line_VOICE.title.text_font_size = '30px'

title = "DNA 24Hr distribution"

line_DNA = Line(data_DNA, ylabel = yl, xlabel = xl, color = Category20[20], title = title, legend = False)
# line_VOICE = line_VOICE(data_VOICE, ylabel = 'mean ' + sys.argv[2], xlabel = xl)
# line_VOICE.legend.orientation = 'horizontal'
# legend = line_DNA.legend
# legend.plot = None
# legend.location = (0 , 600)
# line_DNA.add_layout(legend[0], "right")
# line_DNA.xaxis.axis_label_text_font_size = '20px'
# line_DNA.yaxis.axis_label_text_font_size = '20px'
# line_DNA.title.text_font_size = '30px'



# save file
# output_file("test_K" + str(i + 1) + ".html")
# output_file(output_path + filename[:-4] + "_K" + str(K) + "_distribution.html")
# output_file("DNA_VOICE_24_median_0707.html")
output_file("DNA_VOICE_24_mean_0707.html")

# save(line_VOICE)
# show(line_VOICE)	

show(row([line_VOICE, line_DNA]))

# # save file
# # output_file("test_K" + str(i + 1) + ".html")
# line_VOICE.title.text = title + " DETAIL"
# output_file(output_path + filename[:-4] + "_K" + str(K) + "_NAME_LARGE_distribution.html")

# save(line_VOICE)
# # show(line_VOICE)