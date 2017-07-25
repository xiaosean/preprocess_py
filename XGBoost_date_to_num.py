
# coding: utf-8

# In[1]:

import pandas as pd
import dask.dataframe as dd
import numpy as np
from sklearn import model_selection
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import train_test_split
from matplotlib import pyplot
from time import time
from datetime import datetime
import feather


# In[2]:

from xgboost import *


# # data preparation

# In[3]:

path = "C:/Users/VIPLAB/Desktop/preprocess_py/marketing_analyze/"
filename = "mkt_with_11_group_id_20170712.csv"
train_df = pd.read_csv(path + filename, error_bad_lines=False)


# In[4]:

# train_df[train_df.columns[24]]
for i in (24,28,76,97,98,99,100,101,102):
    train_df[train_df.columns[i]] = train_df[train_df.columns[i]].apply(pd.to_numeric, errors = 'coerce')
    train_df[train_df.columns[i]] = train_df[train_df.columns[i]].fillna(0)


# In[ ]:

def DATE_to_num(date_str):
    try:
        date = datetime.strptime(date_str, "%Y/%m/%d")
    except:
        return 0
    else:
        date_pivot = datetime.strptime('2017/4/1', "%Y/%m/%d")
        delta = date_pivot - date
        return delta.days


# In[ ]:

for c in train_df.columns:
    if 'DATE' in c and train_df[c].dtypes == np.object:
        train_df[c] = train_df[c].apply(DATE_to_num)
        train_df[c] = train_df[c].apply(pd.to_numeric, errors = 'coerce')
    elif ('CNT' in c or 'DUR' in c or 'AMT' in c) and train_df[c].dtypes == np.object:
        train_df[c] = train_df[c].apply(pd.to_numeric, errors = 'coerce')
        train_df[c] = train_df[c].fillna(0)


# In[ ]:

for c in train_df.columns:
    if 'ID' in c:
        train_df = train_df.drop(c, 1)


# In[ ]:

# path = 'D:/date_to_num.feather'
# feather.write_dataframe(train_df, path)
# train_df = feather.read_dataframe(path)
path = 'D:/date_to_num.csv'
train_df.to_csv(path, encoding = "utf-8")
