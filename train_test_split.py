
# coding: utf-8

# # Read & Clear Data

# In[1]:

import os.path
import numpy as np
import pandas as pd
from time import time
from sklearn.model_selection import train_test_split


# In[2]:

# set configure
# path = "./CDR_MONTHLY_AGGR/"
# path = "D:/0625_fet_analyze/CDR_FINAL/"
# path = "C:/Users/VIPLAB/Downloads/Spark_data/"
path = "./marketing_analyze/"
filename = "april_marketing_anylze_numeric_and_bool_max_min"
# path = "./"
# filename = "dm_subscr_mtc_mly_COMPLETED_revise"
relative_filename = path + filename + ".csv"
# relative_filename = path + filename + ".txt"


# In[3]:

t0 = time()
df = pd.read_csv(relative_filename, error_bad_lines=False)
print("time for read csv: %.2f" % (time()-t0))


# In[4]:

df.head()


# In[5]:

# delete questionable rows
df_clear = df.drop(df[df['Groups'] == 'kid'].index)
df_clear = df_clear.drop(df_clear[df_clear['Groups'] == 'single'].index)


# In[6]:

# verify deletion
df_clear.groupby('Groups').count()


# In[7]:

# train, test = train_test_split(df, test_size = 0.4, random_state = 200)
train, test = train_test_split(df_clear, test_size = 0.4, random_state = 200)


# In[8]:

train_x, train_y = train.iloc[:, 0:-1], train.iloc[:, -1]


# In[9]:

test_x, test_y = test.iloc[:, 0:-1], test.iloc[:, -1]


# In[10]:

len(train_x)


# In[11]:

len(test_x)


# In[12]:

train.groupby('Groups').count()


# In[13]:

test.groupby('Groups').count()


# In[14]:

df_clear.groupby('Groups').count()


# In[15]:

del df


# # SVM

print('start training.')

# In[16]:

from sklearn import svm


# In[ ]:

clf = svm.LinearSVC(max_iter = 300000)


# In[ ]:

clf.fit(train_x, train_y)


# In[ ]:



