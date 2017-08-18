
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
import pickle
from sklearn.metrics import confusion_matrix
import os
import requests

# In[2]:

from xgboost import *





# # categorical feature encoding without one hot encode

# In[39]:
date = "0805"
sample_path = 'D:/' + date + '_sample_SMOTE/'
model_path = './XGB_models/'

# group_names = ['all']
# group_names = ['Adult', 'Game', 'HomeLife', 'InstantMessage-High', 'InstantMessage-SuperHigh', 'Map', 'No_ignificant_preference(instant_message)', 'No_ignificant_preference', 'Portal', 'Social-media', 'Infrequent_User', 'all']
group_names = os.listdir(sample_path)

text_file = open(model_path + "accuracy.txt", "w")
for group_name in group_names[:4]:

    col_rank = pd.DataFrame()
    accs = []

    for sample in range(1):
        # sample = 4
        path = sample_path + group_name + "/"
        filename = ""
        # if group_name == 'all':
            # filename = "0731_marketing_with_picked_group11_numeric_max_min_sample_" + group_name + "_" + str(sample) + ".csv"
        # else:
            # filename = "0731_marketing_with_picked_group11_numeric_max_min_sample_" + group_name + "_others_" + str(sample) + ".csv"
        filename =  date + "_marketing_with_picked_group11_numeric_max_min_sample_" + group_name + "_others" + ".csv"
        # filename = "0725_april_marketing_anylze_select_294_table_group11_max_min_sample_" + group_name + "_others_" + str(sample) + ".csv"
        # filename = "0719_april_marketing_anylze_full_table_group11_max_min_train.csv"
        print(group_name, sample)
        train_df = pd.read_csv(path + filename, error_bad_lines=False)



        # In[41]:

        X_train = train_df.iloc[:, 0:-1].values
        y_train = train_df.iloc[:, -1].values


        # In[42]:
        max_depth = 4

        param_grid = {
        #     'max_depth':[3, 5],
        #     'learning_rate':[0.1, 0.05, 0.2],
        #     'n_estimators':[50, 100, 200]
        #     'max_depth':[10],
        #     'learning_rate':[0.05],
        #     'n_estimators':[100],
            'max_depth':[max_depth],
            'min_child_weight':[10],
            # 'colsample_bytree':[0.8],
            # 'seed':[5],
            'gamma':[0.5]
        #     'silent':[False]
        #     'min_child_weight':[2]
        }


        # In[43]:

        t0 = time()
        # model = XGBClassifier(n_jobs = -1, **{"updater": "grow_gpu"})
        model = XGBClassifier(n_jobs = -1)
        # kfold = StratifiedKFold(n_splits=4, shuffle=True, random_state=7)
        gs = GridSearchCV(estimator=model, param_grid=param_grid, scoring='accuracy', cv=5, n_jobs=1)
        gs.fit(X_train, y_train)
        print("training time:  %.2f" % (time()-t0))


        # print(gs.best_score_)
        # print(gs.best_params_)
        best_model = gs.best_estimator_


        # In[45]:

        # print(gs.cv_results_)


        print("Train Accuracy: %.2f%%" % (gs.best_score_ * 100.0))
        accs.append(gs.best_score_ * 100.0)


        col_rank['importance' + str(sample)] = best_model.feature_importances_
        col_rank.index = train_df.columns[:-1]

        # col_rank_sort = col_rank.sort_values('importance', ascending = False)

    

        # ## save model

        # In[54]:

        model_name = 'xgboost_without_infre_' + group_name + '_' + str(sample) + '_' + date
        best_model._Booster.save_model(model_path + model_name + '.model')

        pickle.dump(best_model, open(model_path + model_name + ".dat", "wb"))


        # In[56]:
        pred = best_model.predict(X_train)

        # labels = ['Adult', 'Game', 'HomeLife', 'InstantMessage-High', 'InstantMessage-Low', 'Map', 'News', 'No_ignificant_preference', 'Portal', 'Social-media']
        labels = train_df['Groups'].unique()
        cnf_matrix = confusion_matrix(y_train, pred, labels=labels)
        # cnf_matrix


        # In[57]:

        cnf_pd = pd.DataFrame(cnf_matrix)
        cnf_pd.columns = labels
        cnf_pd.index = labels
        cnf_pd.to_csv(model_path + model_name + "_cnf.csv", index=True, encoding='utf-8')


    col_rank['mean'] = col_rank.mean(axis=1)
    col_rank = col_rank.sort_values('mean', ascending = False)
    col_rank.to_csv(model_path + model_name + "_rank.csv", encoding='utf-8')

    importance_sum = 0
    n_importance = 0
    for i in range(len(col_rank['mean'])):
        importance_sum += col_rank['mean'].values[i]
        if importance_sum > 0.8:
            n_importance = i
            break
    print("the most important %d features can have a importance of %.2f%%" % (n_importance, importance_sum * 100))

    # n_test = max_depth
    # curr_score = 0
    # while gs.best_score_ - curr_score > 0.01:
    #     n_test += 1
    #     t0 = time()
    #     test_model = XGBClassifier(n_jobs = -1, **{"updater": "grow_gpu"})
    #     # test_model = XGBClassifier(n_jobs = -1)
    #     # kfold = StratifiedKFold(n_splits=4, shuffle=True, random_state=7)
    #     test_gs = GridSearchCV(estimator=test_model, param_grid=param_grid, scoring='accuracy', cv=5, n_jobs=1)
    #     X_train_test = train_df[col_rank.index[:n_test]].iloc[:, 0:-1].values
    #     test_gs.fit(X_train_test, y_train)
    #     print("training time(%d features):  %.2f" % (n_test, time()-t0))
    #     curr_score = test_gs.best_score_
    #     print("accuracy: %.2f%%" % (curr_score * 100))
    # print("%d features can represent %.2f%% of all the features" % (n_test, (curr_score / gs.best_score_)*100))

    text_file.write(group_name + ":\n")
    text_file.write("%s\nTrain Accuracy: %.2f%%" % (str(accs), np.mean(accs)))
    text_file.write("the most important %d features can have a importance of %.2f%%" % (n_importance, importance_sum * 100))
    # text_file.write("\n%d features can represent %.2f%% of all the features" % (n_test, (curr_score / gs.best_score_)*100))
text_file.close()
    # requests.post(
    #     "https://api.mailgun.net/v3/sandboxe9bb891a60414f4bae93f2cc55daa963.mailgun.org/messages",
    #     auth=("api", "key-a007a22faf334a3510137b6cc03c21a6"),
    #     data={"from": "Mailgun Sandbox <postmaster@sandboxe9bb891a60414f4bae93f2cc55daa963.mailgun.org>",
    #           "to": "Toby <atch84@gmail.com>",
    #           "subject": "XGBoost Result",
    #           "text": group_name + " " + str(sample) + "\n" + str(np.mean(accs))})

