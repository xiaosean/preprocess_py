import string
import pandas as pd
import numpy as np
import plotly.offline as py
import plotly.graph_objs as go
import math
import sys

# read csv
df = pd.read_csv(sys.argv[1], error_bad_lines = False)

# drop not needed columns
drop_col_list = []
for col in df.columns:
    if str(col).find(sys.argv[2]) == -1:
        drop_col_list.append(str(col))
df = df.drop(drop_col_list, 1)

# draw box plot
data = []
for col in df.columns:
    trace = go.Box(
        y = df[col].values,
        name = col,
        boxmean = 'sd',
        boxpoints = False,
        showlegend = False
#         boxpoints = 'suspectedoutliers'
    )
    data.append(trace)

# save file
output_name = sys.argv[1][:-4] + "_" + sys.argv[2] + "_boxplot"
py.plot(data, filename = output_name + ".html", auto_open = False)
# py.plot(data, filename = output_name + ".html", auto_open = False, image_filename = output_name, image = 'jpeg', image_width = 800, image_height = 6000)