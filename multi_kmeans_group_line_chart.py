import numpy as np
import pandas as pd
from time import time
from sklearn.cluster import KMeans
from pandas.computation import expressions as expr
from bokeh.charts import Line, show, output_file, save
import pprint as pp
import sys
from bokeh.palettes import Spectral11, Category10

# set configure
# path = "./CDR_NORMALIZE_CONCAT/"
path = "./CDR_FINAL/"
filename = "hours_divide.csv"
# path = "./CDR_ANALYZE/"
# path = "./CDR_CONCAT/"
# filename = sys.argv[1]
# filename = "CDR_CONCAT_TABLE_4_max_min.csv"
# filename = "CDR_CONCAT_TABLE_4.csv"
relative_filename = path + filename  #+ ".csv"
# out_filename = "mds_mly_minus20160901"
# after the numeric_st_idx's number will be tranform to int64
# numeric_st_idx = 1
# K = 8
label_path = "./kmean_label/"
output_path = "./CDR_CONCAT_ANALYZE_GRAPH/"
# output_path = "./CDR_CONCAT_ANALYZE_GRAPH_MINI/"

# read revise csv file and print cost time
# just load 5 data 
t0 = time()
df_src = pd.read_csv(relative_filename, error_bad_lines=False)
print("time for read csv: %.2f" % (time()-t0))


# -------------------------
for c in df_src.columns[1:]:
	if not "CNT" in c:
		df_src = df_src.drop(c, 1)
# ----------------------------

# df = df.drop('MINING_DW_SUBSCR_NO', 1)
df_group = pd.read_csv('DNA_KMEANS_RESULT_ID_NEW.csv', error_bad_lines = False)

groups_name = ['1', '2', '3', '4', '5', '6', '7', '8', 'seldom', 'None']
# groups_name = ['1', '2', '3', '4', '5', '6', '7', '8']

# Ks = [8, 7, 6, 7, 5, 6, 6, 8, 7, 7]
Ks = [6, 5, 5, 5, 5, 5, 5, 5]

evening = "Evening user"
moring = "Morning user"
midnight = "Midnight user"
lunch = "Lunch time user"
All = "All day user"
dinner = "Dinner time user"
afternoon = "Afternoon user"

cluster_name = [
	{107141:moring, 121153:midnight, 17176:lunch, 59992:afternoon, 32089:evening, 70046:dinner},
	{25449:evening, 30950:dinner, 5441:lunch, 59944:midnight, 62860:All},
	{20553:afternoon, 20809:dinner, 26798:moring, 32848:midnight, 4801:lunch},
	{17959:evening, 24518:dinner, 33790:moring, 35510:midnight, 5181:lunch},
	{17238:evening, 25183:dinner, 32834:moring, 31327:midnight, 3892:lunch},
	{14298:midnight, 21404:"Late midnight user", 35439:moring, 35802:dinner, 39104:"Office time user"},
	{19744:evening, 24966:afternoon, 33129:"Night user", 41770:moring, 44540:midnight},
	{106596:dinner, 124046:moring, 146613:midnight, 21343:lunch, 91568:afternoon}
]

norm = "06281"

df_src['Groups'] = df_group['Groups']

for j in range(8):
	K = Ks[j]
	group = groups_name[j]
		

	df = df_src[df_src['Groups'] == group]

	label_path = "./kmean_label/"
	label_name = "label_K" + str(K) + "_de_with_kid_" + group + "_" + norm + ".npy"
	labels_ = np.load(label_path + label_name)

	# df.loc['label',list(map(str, df.index))] = labels_
	df['label'] = labels_
	grouped = df.groupby('label')

	print(group)
	df['label'] = labels_
	grouped = df.drop(['MINING_DW_SUBSCR_NO', 'Groups'], 1).groupby('label')
	# grouped = df.groupby('label')

	# get count
	group_count = grouped[df.columns[1]].count().values
	# df = df.drop('MINING_DW_SUBSCR_NO', 1)	

	# get mean
	group_mean = grouped.mean()


	# cluster_name = {1012:'每通通話量長', 	1470990:'幾乎不用', 	23626:'高度使用', 	283083:'有在使用', 	48456:'夜貓族', 	3601:'超高度使用',	68665:'中度使用', 	697364:'稍微使用'}

	# aggregate display data
	data = {}
	for i in range(K):
		# data[str(i)] = grouped.mean().values[i]
		# if "HOUR" in filename:
		# 	# data[cluster_name[cluster_result[i]] + "(" + str(cluster_result[i]) + ")"] = list(map(lambda x: x/30,grouped.mean().values[i]))
		# 	# data["(" + str(group_count[i]) + ")"] = list(map(lambda x: x/30, group_mean.values[i][1:]))
		# else:
		# 	# data[cluster_name[cluster_result[i]] + "(" + str(cluster_result[i]) + ")"] = list(map(lambda x: x/4,grouped.mean().values[i]))
		# 	data["(" + str(group_count[i]) + ")"] = list(map(lambda x: x/4, group_mean.values[i][1:]))

		data[cluster_name[j][group_count[i]] + "(" + str(group_count[i]) + ")"] = group_mean.values[i]
		# data["(" + str(group_count[i]) + ")"] = group_mean.values[i]
		# data[str(cluster_name[i])] = grouped.mean().values[i]

	pp.pprint(df.columns[1:-2])

	# select label
	# xl = str(df.columns)
	# xl = "MO_0_24 MT_0_24 MO_SUN_SAT_w_h MT_SUN_SAT_w_h"
	xl = "hour"
	if filename.find("WORK") != -1:
		xl = str(df.columns[1:])
	elif filename.find("hours") == -1:
		xl = "SUN      ~      SAT"

	# yl = "time"
	# if filename.find("TIME") == -1:
	# 	yl = "count"

	yl = "percentage"

	# draw
	# # set line colors
	# mycolors = []
	# # if K > 5:
	# # 	mycolors = Spectral11[0:5] + Spectral11[6:K + 1]
	# # else:
	# # 	mycolors = Spectral11[0:K]
	# for i in range(K):
	# 	mycolors.append(Spectral11[i * 2])

	title = "Group " + group


	line = Line(data, ylabel = yl, xlabel = xl, color = Category10[10], title = title, legend = "top_center")
	# line = Line(data, ylabel = 'mean ' + sys.argv[2], xlabel = xl)
	# line.legend.orientation = 'horizontal'
	legend = line.legend
	legend.plot = None
	legend.location = (0 , 300)
	line.add_layout(legend[0], "right")
	line.xaxis.axis_label_text_font_size = '20px'
	line.yaxis.axis_label_text_font_size = '20px'
	line.title.text_font_size = '30px'

	# save file
	# output_file("test_K" + str(i + 1) + ".html")
	output_filename = ("%s_K%d_G%s_%s_line.html" % (filename[:-4], K, group, norm))
	output_file(output_path + output_filename)
	# output_file(output_path + filename[:-4] + "_K" + str(K) + "_NAME_distribution.html")

	save(line)
	# show(line)	


	# # save file
	# # output_file("test_K" + str(i + 1) + ".html")
	# line.title.text = title + " DETAIL"
	# output_file(output_path + filename[:-4] + "_K" + str(K) + "_NAME_LARGE_distribution.html")

	# save(line)
	# # show(line)