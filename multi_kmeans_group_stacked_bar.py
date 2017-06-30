
# coding: utf-8
import pandas as pd
import numpy as np
import plotly.offline as py
import plotly.graph_objs as go
import sys

# py.offline.init_notebook_mode()
output_path = "./CDR_CONCAT_ANALYZE_GRAPH/"

path = "./CDR_ANALYZE/"
# filename = "TABLE_4_MOC_TELEGRAM_TIME_COLS.csv"
filename = sys.argv[1]
df_src = pd.read_csv(path + filename, error_bad_lines = False)

df_group = pd.read_csv('DNA_KMEANS_RESULT_ID.csv', error_bad_lines = False)

groups_name = ['1', '2', '3', '4', '5', '6', '7', '8', 'seldom', 'None']

norm = "max_min"
df_src['Groups'] = df_group['Groups']

for K in range(3, 6):
	for group in groups_name:
		df = df_src[df_src['Groups'] == group]

		label_path = "./kmean_label/"
		label_name = "label_K" + str(K) + "__" + group + "_" + norm + ".npy"
		labels_ = np.load(label_path + label_name)

		# df.loc['label',list(map(str, df.index))] = labels_
		df['label'] = labels_
		grouped = df.groupby('label')

		# get count
		group_count = grouped['MINING_DW_SUBSCR_NO'].count().values

		# get mean
		group_mean = grouped.mean()

		data = []

		for c in group_mean.columns[1:]:
			trace = go.Bar(
				# x = list(map(lambda x: " " + str(x + 1), range(K))),
				x = list(map(lambda x: "G" + str(x), group_count)),
				y = list(map(lambda x: x/30, group_mean[c].values)),
				name = c
			)
			data.append(trace)

		title = ""
		if filename.find("MO") != -1:
			title += "MO "
		if filename.find("MT") != -1:
			title += "MT "

		if filename.find("CNT") != -1:
			title += ("avg %s per day (%s)" % ("count", "times"))
		elif filename.find("TIME") != -1:
			title += ("avg %s per day (%s)" % ("duration", "seconds"))
		layout = go.Layout(barmode = 'stack', title = title)

		fig = go.Figure(data = data, layout = layout)
		output_filename = ("%s_K%d_G%s_%s_bar.html" % (filename[:-4], K, group, norm))
		# py.plot(fig, filename = output_path + output_filename, image_height = 6000, image_width = 8000)
		py.plot(fig, filename = output_path + output_filename, image_height = 6000, image_width = 8000, auto_open = False)
