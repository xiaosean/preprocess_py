
# coding: utf-8
import pandas as pd
import numpy as np
import plotly.offline as py
import plotly.graph_objs as go
import sys

# py.offline.init_notebook_mode()
output_path = "./CDR_CONCAT_ANALYZE_GRAPH/"

# path = "./CDR_ANALYZE/"
path = "./CDR_FINAL/"
filename = "hours_divide.csv"
# filename = sys.argv[1]
df_src = pd.read_csv(path + filename, error_bad_lines = False)

df_group = pd.read_csv('DNA_KMEANS_RESULT_ID_NEW.csv', error_bad_lines = False)
# -------------------------
for c in df_src.columns[1:]:
	if not "CNT" in c:
		df_src = df_src.drop(c, 1)
# ----------------------------

groups_name = ['1', '2', '3', '4', '5', '6', '7', '8', 'seldom', 'None']
# groups_name = ['1', '2', '3', '4', '5', '6', '7', '8']

Ks = [6, 5, 5, 5, 5, 5, 5, 5]
# Ks = [8, 7, 6, 7, 5, 6, 6, 8, 7, 7]


date = "06281"
df_src['Groups'] = df_group['Groups']

# for K in range(7, 10):
# 	for group in groups_name:
for i in range(8):
	K = Ks[i]
	group = groups_name[i]
	df = df_src[df_src['Groups'] == group]
	# group = filename[15:-4]

	label_path = "./kmean_label/"
	label_name = "label_K" + str(K) + "_de_with_kid_" + group + "_" + date + ".npy"
	labels_ = np.load(label_path + label_name)

	# df.loc['label',list(map(str, df.index))] = labels_
	print(group)
	df['label'] = labels_
	grouped = df.drop(['MINING_DW_SUBSCR_NO', 'Groups'], 1).groupby('label')
	# grouped = df.groupby('label')

	# get count
	group_count = grouped[df.columns[1]].count().values
	# df = df.drop('MINING_DW_SUBSCR_NO', 1)	

	# get mean
	group_mean = grouped.mean()

	trace = go.Heatmap(
		# x = list(map(lambda x: " " + str(x + 1), range(K))),
		# z = np.delete(group_mean.values, 0, 1),
		z = group_mean.values,
		x = df.columns[1:-1],
		y = list(map(lambda x: "G " + str(x), group_count)),
		colorscale = 'Jet'
	)

	data = [trace]

	title = ("Group %s" % (group))
	layout = go.Layout(title = title)

	fig = go.Figure(data = data, layout = layout)
	output_filename = ("%s_K%d_G%s_%s_heat.html" % (filename[:-4], K, group, date))
	# py.plot(fig, filename = output_path + output_filename, image_height = 6000, image_width = 8000)
	py.plot(fig, filename = output_path + output_filename, image_height = 6000, image_width = 8000, auto_open = False)
