# coding=UTF-8
import pandas as pd
import numpy as np
from scipy import stats
import math 
global x_max
global x_min
global x_mean
global x_std

def log10(x):
    if(x > 0):
        x = math.log(x, 10)
    return x
def max_min_normalize(x):
    # print(x, x_max, x_min)
    return (x - x_min) / (x_max - x_min)

def z_normalize(x):
    # print(x, x_mean, x_std)
    return (x - x_mean) / x_std

if __name__ == '__main__':
    # 讀取xlsx data frame 並秀出資料
    # path = "../DATA_FULL/"
    path = "../"
    filename = "output_DM_SUBSCR_VAS_VOL_PRD_MLY_2017-04-01_100"
    relative_filename = path + filename + ".xlsx"
    
    # print(df)

    # 列出欄位名稱
    # print(df.columns)
    # df = pd.read_excel(relative_filename)
    # normalize_cols = ['VAS_HR00_BYTE', 'VAS_HR06_BYTE', 'VAS_HR12_BYTE', 'VAS_HR18_BYTE', 'VAS_WORKDAY_BYTE', 'VAS_WEEKEND_BYTE']
    # normalize_funcs = [log10, lambda x: (x - np.mean(x)) / (np.max(x) - np.min(x)]
    normalize_funcs = {"log10" : log10, "max_min" : max_min_normalize, "z_norm" : z_normalize}
    for normalize_key, normalize in normalize_funcs.items(): 
        df = pd.read_excel(relative_filename)
        normalize_cols = df.columns[2:]
        for col in normalize_cols:
            # df[col] = df[col].apply(np.int64)
            print(normalize)
            x_max, x_min ,x_mean ,x_std = df[col].max(), df[col].min(), df[col].mean(), df[col].std(ddof=0) 
            df[col] = df[col].apply(normalize)
            print("column = %s normalize has finished" % col)
        # df.to_csv(filename + "_" + normalize_key + ".csv", index=False)
        df[2:].to_csv(filename + "_" + normalize_key + ".csv", index=False)




