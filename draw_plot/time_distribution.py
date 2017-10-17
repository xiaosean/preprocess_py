from bokeh.charts import Line, show, output_file, save
import numpy as np
import pandas as pd
import sys

# usage: python time_distribution.py csv_file TIME/CNT

df = pd.read_csv(sys.argv[1], error_bad_lines = False)

# drop not needed columns
drop_col_list = []
for col in df.columns:
    if str(col).find(sys.argv[2]) == -1:
        drop_col_list.append(str(col))
df = df.drop(drop_col_list, 1)

# aggregate display data
hourly_data = []
cols = []
for col in df.columns:
	hourly_data.append(df[col].mean())
	cols.append(col)
print(cols)

# select label
xl = "hour"
if sys.argv[1].find("HOUR") == -1:
	xl = "week day"

# draw
line = Line(hourly_data, ylabel = 'mean ' + sys.argv[2], xlabel = xl)

# save file
output_file(sys.argv[1][:-4] + "_" + sys.argv[2] + "_distribution.html")

save(line)
# show(line)