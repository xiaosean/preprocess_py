
# coding: utf-8

# In[1]:

import pandas as pd
import numpy as np
from sklearn import model_selection
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.model_selection import *
from matplotlib import pyplot
from time import time

import requests

# In[2]:

from xgboost import *





# # categorical feature encoding without one hot encode

# In[39]:

group_names = ['Adult', 'Game', 'HomeLife', 'InstantMessage-High', 'InstantMessage-Low', 'Map', 'News', 'No_ignificant_preference', 'Portal', 'Social-media']

for group_name in group_names:

    col_rank = pd.DataFrame()
    accs = []

    for sample in range(5):
        # sample = 4
        path = "C:/Users/VIPLAB/Desktop/preprocess_py/marketing_analyze/0725_sample/" + group_name + "/"
        filename = "0725_april_marketing_anylze_select_294_table_group11_max_min_sample_" + group_name + "_others_" + str(sample) + ".csv"
        # filename = "0719_april_marketing_anylze_full_table_group11_max_min_train.csv"
        print(group_name, sample)
        train_df = pd.read_csv(path + filename, error_bad_lines=False)



        # In[41]:

        X_train = train_df.iloc[:, 0:-1].values
        y_train = train_df.iloc[:, -1].values


        # In[42]:

        param_grid = {
        #     'max_depth':[3, 5],
        #     'learning_rate':[0.1, 0.05, 0.2],
        #     'n_estimators':[50, 100, 200]
        #     'max_depth':[10],
        #     'learning_rate':[0.05],
            'n_estimators':[50],
            'max_depth':[3],
            'min_child_weight':[7]
        }


        # In[43]:

        t0 = time()
        model = XGBClassifier(n_jobs = -1, **{"updater": "grow_gpu"})
        # kfold = StratifiedKFold(n_splits=4, shuffle=True, random_state=7)
        gs = GridSearchCV(estimator=model, param_grid=param_grid, scoring='accuracy', cv=5, n_jobs=1)
        gs.fit(X_train, y_train)
        print("training time:  %.2f" % (time()-t0))


        # print(gs.best_score_)
        # print(gs.best_params_)
        best_model = gs.best_estimator_


        # In[45]:

        print(gs.cv_results_)


        print("Train Accuracy: %.2f%%" % (gs.best_score_ * 100.0))
        accs.append(gs.best_score_ * 100.0)


        col_rank['column_name' + str(sample)] = train_df.columns[:-1]
        col_rank['importance' + str(sample)] = best_model.feature_importances_

        # col_rank = col_rank.sort_values('importance', ascending = False)

        # ## save model

        # In[54]:

        path = './XGB_models/'
        model_name = 'xgboost_without_infre_' + group_name + '_' + str(sample) + '_0725'
        best_model._Booster.save_model(path + model_name + '.model')

        import pickle
        pickle.dump(best_model, open(path + model_name + ".dat", "wb"))


        # In[56]:
        pred = best_model.predict(X_train)

        from sklearn.metrics import confusion_matrix
        # labels = ['Adult', 'Game', 'HomeLife', 'InstantMessage-High', 'InstantMessage-Low', 'Map', 'News', 'No_ignificant_preference', 'Portal', 'Social-media']
        labels = train_df['Groups'].unique()
        cnf_matrix = confusion_matrix(y_train, pred, labels=labels)
        # cnf_matrix


        # In[57]:

        cnf_pd = pd.DataFrame(cnf_matrix)
        cnf_pd.columns = labels
        cnf_pd.index = labels
        cnf_pd.to_csv(path + model_name + '_' + str(sample) + "_cnf.csv", index=False, encoding='utf-8')


    col_rank['mean'] = col_rank.mean(axis=1)
    col_rank.to_csv(path + model_name + "_rank.csv", index=False, encoding='utf-8')

    text_file = open(path + model_name + "_accuracy.txt", "w")
    text_file.write("%s\nTrain Accuracy: %.2f%%" % (str(accs), np.mean(accs)))
    text_file.close()
    requests.post(
        "https://api.mailgun.net/v3/sandboxe9bb891a60414f4bae93f2cc55daa963.mailgun.org/messages",
        auth=("api", "key-a007a22faf334a3510137b6cc03c21a6"),
        data={"from": "Mailgun Sandbox <postmaster@sandboxe9bb891a60414f4bae93f2cc55daa963.mailgun.org>",
              "to": "Toby <atch84@gmail.com>",
              "subject": "XGBoost Result",
              "text": group_name + " " + str(sample) + "\n" + str(np.mean(accs))})

