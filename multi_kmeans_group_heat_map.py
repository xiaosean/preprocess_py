
# coding: utf-8
import pandas as pd
import numpy as np
import plotly.offline as py
import plotly.graph_objs as go
from plotly import tools
import sys

# py.offline.init_notebook_mode()
output_path = "./CDR_CONCAT_ANALYZE_GRAPH/"

# path = "./CDR_ANALYZE/"
path = "./CDR_FINAL/"
filename = "0703normalize_65_cols.csv"
# filename = sys.argv[1]
df_src = pd.read_csv(path + filename, error_bad_lines = False)

df_group = pd.read_csv('DNA_KMEANS_RESULT_ID_NEW.csv', error_bad_lines = False)
# -------DROP COLUMNS------
# for c in df_src.columns[1:]:
# 	if not "CNT" in c:
# 		df_src = df_src.drop(c, 1)

df_src = df_src.drop(df_src.columns[26:40], 1)

df_voice = pd.DataFrame()
df_DNA = pd.DataFrame()
df_voice[df_src.columns[0]] = df_src[df_src.columns[0]]
df_DNA[df_src.columns[0]] = df_src[df_src.columns[0]]
for c in df_src.columns[1:]:
	if "DNA" in c or "dna" in c:
		df_DNA[c] = df_src[c]
	elif "voice" in c or "VOICE" in c:
		df_voice[c] = df_src[c]
# ----------------------------

groups_name = ['1', '2', '3', '4', '5', '6', '7', '8', 'seldom', 'None']
# groups_name = ['1', '2', '3', '4', '5', '6', '7', '8']

# Ks = [6, 5, 5, 5, 5, 5, 5, 5]
# Ks = [8, 7, 6, 7, 5, 6, 6, 8, 7, 7]
Ks = [6, 4, 6, 7, 7, 6, 8, 7, 7, 7]


date = "0704"


df_voice['Groups'] = df_group['Groups']
df_DNA['Groups'] = df_group['Groups']
# -------------------DNA------------------------------------

# for K in range(7, 10):
# 	for group in groups_name:
for i in range(len(Ks)):
	traces = []
	K = Ks[i]
	group = groups_name[i]
	df = df_DNA[df_DNA['Groups'] == group]
	# group = filename[15:-4]

	label_path = "./kmean_label/"
	label_name = "label_K" + str(K) + "__" + group + "_" + date + ".npy"
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

	traces.append(trace)
	# data = [trace]

	# title = ("Group %s" % (group))
	# layout = go.Layout(title = title)

	# fig = go.Figure(data = data, layout = layout)
	
	# output_filename = ("%s_K%d_G%s_%s_heat_DNA.html" % (filename[:-4], K, group, date))
	# py.plot(fig, filename = output_path + output_filename, image_height = 6000, image_width = 8000, auto_open = False)


# --------------------VOICE---------------------------------

# for K in range(7, 10):
# 	for group in groups_name:
# for i in range(len(Ks)):
	# K = Ks[i]
	# group = groups_name[i]
	df = df_voice[df_voice['Groups'] == group]
	# group = filename[15:-4]

	label_path = "./kmean_label/"
	label_name = "label_K" + str(K) + "__" + group + "_" + date + ".npy"
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

	traces.append(trace)

	# data = [trace]

	# title = ("Group %s" % (group))
	# layout = go.Layout(title = title)

	# fig = go.Figure(data = data, layout = layout)

	# output_filename = ("%s_K%d_G%s_%s_heat_voice.html" % (filename[:-4], K, group, date))
	# py.plot(fig, filename = output_path + output_filename, image_height = 6000, image_width = 8000, auto_open = False)

	title = ("Group %s" % (group))

	combined_fig = tools.make_subplots(rows = 2, cols = 1)
	# print(type(combined_fig))
	for i in range(len(traces)):
		combined_fig.append_trace(traces[i], i+1, 1)
	# combined_fig.append_trace(traces[0], 1, 1)
	# combined_fig.append_trace(traces[1], 2, 1)
	combined_fig['layout'].update(title = title)
		
	output_filename = ("%s_K%d_G%s_%s_heat.html" % (filename[:-4], K, group, date))
	py.plot(combined_fig, filename = output_path + output_filename, image_height = 6000, image_width = 8000, auto_open = False)


# ----------------VOICE + DNA----------------------------------
# df_src['Groups'] = df_group['Groups']

# # for K in range(7, 10):
# # 	for group in groups_name:
# for i in range(10):
# 	K = Ks[i]
# 	group = groups_name[i]
# 	df = df_src[df_src['Groups'] == group]
# 	# group = filename[15:-4]

# 	label_path = "./kmean_label/"
# 	label_name = "label_K" + str(K) + "__" + group + "_" + date + ".npy"
# 	labels_ = np.load(label_path + label_name)

# 	# df.loc['label',list(map(str, df.index))] = labels_
# 	print(group)
# 	df['label'] = labels_
# 	grouped = df.drop(['MINING_DW_SUBSCR_NO', 'Groups'], 1).groupby('label')
# 	# grouped = df.groupby('label')

# 	# get count
# 	group_count = grouped[df.columns[1]].count().values
# 	# df = df.drop('MINING_DW_SUBSCR_NO', 1)	

# 	# get mean
# 	group_mean = grouped.mean()

# 	trace = go.Heatmap(
# 		# x = list(map(lambda x: " " + str(x + 1), range(K))),
# 		# z = np.delete(group_mean.values, 0, 1),
# 		z = group_mean.values,
# 		x = df.columns[1:-1],
# 		y = list(map(lambda x: "G " + str(x), group_count)),
# 		colorscale = 'Jet'
# 	)

# 	data = [trace]

# 	title = ("Group %s" % (group))
# 	layout = go.Layout(title = title)

# 	fig = go.Figure(data = data, layout = layout)
# 	output_filename = ("%s_K%d_G%s_%s_heat.html" % (filename[:-4], K, group, date))
# 	# py.plot(fig, filename = output_path + output_filename, image_height = 6000, image_width = 8000)
# 	py.plot(fig, filename = output_path + output_filename, image_height = 6000, image_width = 8000, auto_open = False)
