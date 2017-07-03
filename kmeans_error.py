import numpy as np
import pandas as pd
from time import time
from sklearn.cluster import KMeans
from pandas.computation import expressions as expr
# from bokeh.charts import Line, show, output_file, save
import pprint as pp
import sys
import ast
from bokeh.palettes import Spectral11, Category20
from bokeh.plotting import figure, show, output_file, save
from bokeh.models import Legend
from bokeh.models import LinearAxis, Range1d

output_filename = "./kmeans_error_graph/"

data =  ast.literal_eval(sys.argv[1])

df = pd.DataFrame()
df['K_clusters'] = list(data.keys())
df['error'] = list(data.values())

p = figure(toolbar_location = "right", title = "K clusters performence")
p.line(list(df['K_clusters'].values), df['error'].values, line_width = 2)
p.circle(df['K_clusters'].values, df['error'].values, fill_color = "white", size = 8)
p.xaxis.axis_label_text_font_size = '20px'
p.yaxis.axis_label_text_font_size = '20px'
p.xaxis.axis_label = "K_clusters"
p.yaxis.axis_label = "error"
p.title.text_font_size = '30px'
output_file(output_filename + "K_cluster_error_" + sys.argv[2] + ".html")
save(p)
# show(p)