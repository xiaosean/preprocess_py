from bokeh.charts import Donut, show, output_file, save
import pandas as pd
import numpy as np
from bokeh.palettes import Pastel1
import sys

# py.offline.init_notebook_mode()
output_path = "./CDR_CONCAT_ANALYZE_GRAPH/"

# path = "./CDR_ANALYZE/"
# filename = "TABLE_4_MOC_TELEGRAM_TIME_COLS.csv"
path = "./CDR_FINAL/"
filename = "hours_divide.csv"

df_group = pd.read_csv('DNA_KMEANS_RESULT_ID_NEW.csv', error_bad_lines = False)

groups_name = ['1', '2', '3', '4', '5', '6', '7', '8', 'seldom', 'None']
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

for j in range(8):
	K = Ks[j]
	group = groups_name[j]

	df = df_group[df_group['Groups'] == group]

	label_path = "./kmean_label/"
	label_name = "label_K" + str(K) + "_de_with_kid_" + group + "_" + norm + ".npy"
	labels_ = np.load(label_path + label_name)

	# df.loc['label',list(map(str, df.index))] = labels_
	df['label'] = labels_
	grouped = df.groupby('label')

	# get count
	group_count = grouped['MINING_DW_SUBSCR_NO'].count().values

	value = group_count
	index = []
	for i in range(K):
		index.append(cluster_name[j][group_count[i]])
	total = 0
	for i in range(len(value)):
	    total += value[i]
	for i in range(len(value)):
	    percent_str = str(value[i]/total*100)
	    index[i] += "(" + percent_str[:percent_str.find(".")] + "%)"
	data = pd.Series(value, index = index)


	pie_chart = Donut(data, color = Pastel1[8], text_font_size='12pt')
	# show(pie_chart)

	output_filename = ("K%d_G%s_%s_pie.html" % (K, group, norm))
	output_file(output_path + output_filename)

	save(pie_chart)

# df = pd.read_csv('output_FYSP_HTTPDR_CATG_WEEKOF_MLY_2017-04-01_aggregate.csv')

# df = pd.melt(df, id_vars = ['DNA_CATG_DESC'],
#             value_vars=['HTTPDR_DATA_W1_CNT','HTTPDR_DATA_W2_CNT','HTTPDR_DATA_W3_CNT','HTTPDR_DATA_W4_CNT','HTTPDR_DATA_W5_CNT','HTTPDR_DATA_W6_CNT','HTTPDR_DATA_W7_CNT'],
#              value_name='usage_count', var_name='day')

# def shorten_name(s):
#     return s[12:14]

# df['day'] = df['day'].apply(shorten_name)

# df = df[df['total'] > 5000000]
# df

# # original example
# d = Donut(df, label=['DNA_CATG_DESC'], values='total',
#           text_font_size='8pt', hover_text='DNA_CATG_DESC')
# show(d)



