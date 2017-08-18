import logging
try:
	print("TESTING PACKAGE IMPORT")
	import os.path
	import numpy as np
	import pandas as pd
	import math
	import random
	from time import time
	from scipy import stats
	from os import listdir
	from os.path import isfile, join
	from collections import Counter
	from imbalanced.imblearn.over_sampling import SMOTE

	from sklearn.model_selection import GridSearchCV
	from sklearn.model_selection import train_test_split
	from sklearn.model_selection import cross_val_score
	from sklearn.model_selection import ShuffleSplit
	from sklearn import preprocessing
	from sklearn.preprocessing import LabelEncoder
	from sklearn.ensemble import RandomForestClassifier
	from sklearn.externals import joblib
	from sklearn.datasets import make_classification
	from sklearn.metrics import confusion_matrix
	from sklearn.utils import shuffle
	from glob import glob
	print("PACKAGE IMPORT SUCCESS!")

	global x_max
	global x_min
	global x_mean
	global x_std

	glob_start_time = time()

	print("TESTING MEMORY")
	start_time = time()
	x = 400
	y = 2000000 * 5
	cols = [ "f{}".format(i) for i in range(x) ]
	labels = [ "L{}".format(i) for i in range(11) ]
	test_df = pd.DataFrame(np.random.random(size=(y,x)), columns=cols)
	test_df['Groups'] = np.random.randint(0, 10, size=(y)).astype(np.str)
	print("MEMORY SUCCESS! - cost %d seconds" % (time() - start_time))

	print("GENSERATING TEST DATA")
	x = 50
	y = 300000
	cols = [ "f{}".format(i) for i in range(x) ]
	labels = [ "L{}".format(i) for i in range(5) ]
	test_df = pd.DataFrame(np.random.random(size=(y,x)), columns=cols)
	test_df['Groups'] = np.random.randint(0, 10, size=(y)).astype(np.str)

	# SMOTE num
	print("TESTING SMOTE")
	start_time = time()
	X, y = test_df.iloc[:, 0:-1], test_df.iloc[:, -1]
	sm = SMOTE(random_state=42, n_jobs=-1)
	X_res, y_res = sm.fit_sample(X, y)
	print("SMOTE SUCCESS! - cost %d seconds" % (time() - start_time))

	print("TESTING RANDOM FOREST")
	start_time = time()
	train_df = pd.DataFrame(data = X_res, columns = test_df.columns[0:-1])
	train_df["Groups"] = y_res

	train_df = shuffle(train_df)

	# train_df = test_df

	train_x, train_y = train_df.iloc[:, 0:-1].values, train_df.iloc[:, -1].values
	le = preprocessing.LabelEncoder()
	le.fit(train_df["Groups"].unique())
	train_numeric_y = le.transform(train_y)
	rf = RandomForestClassifier(max_features='auto',
	                            random_state=42,
	                            n_jobs=-1,
	                            n_estimators = 100)
	param_grid = {
	              "min_samples_leaf" : [10], 
	              "min_samples_split" : [2],
	              "max_depth" : [25],
	              "n_estimators": [100]}
	#     param_grid = {
	#                   "min_samples_leaf" : [10],                   
	#                   "n_estimators": [100]}
	gs = GridSearchCV(estimator=rf, param_grid=param_grid, scoring='accuracy', cv=2, n_jobs=1)
	grid_clf = gs.fit(train_x, train_numeric_y)
	clf = grid_clf.best_estimator_

	clf_info = str(("Accuracy on training set: %f" % gs.cv_results_["mean_test_score"][0])) + '\n'
	# clf_info += str(("Accuracy on test set: %f" % clf.score(test_x, test_numeric_y))) + '\n'
	clf_info += str(('fit time %s seconds' % format(time() - start_time))) + '\n'
	#     print(clf_info)
	important_dict = dict(zip(train_df.columns[:-1],clf.feature_importances_))
	important_list = sorted(important_dict.items(), key=lambda x: x[1])
	important_list.reverse()
	clf_info += '\n\nFeature Importances\n===================\n'
	for row in important_list:
	    clf_info += str(row) + "\n"
	#         print(str(row))
	feature_df = pd.DataFrame(important_list, columns = ["COLUMN", "IMPORTANT_VALUE"])
	t0 = time()
	#     print("time for output csv file: %.2f" % (time()-t0))
	cpy_dict = dict(important_list)
	cpy_dict["Groups"] = "all"
	feature_df = pd.DataFrame(cpy_dict, index = [0])
	accuracy_dict = {}
	accuracy_dict["accuracy"] = gs.cv_results_["mean_test_score"][0]
	accuracy_df = pd.DataFrame(accuracy_dict, index = [0])

	predict_y = clf.predict(train_x)
	cnf_matrix = confusion_matrix(train_numeric_y, predict_y )
	group_encoder = []
	for idx, row in enumerate(cnf_matrix):
	    current_group = str(le.inverse_transform(idx))
	    group_encoder.append(current_group)

	#     idx_count_in_group = len(test_df[test_df["Groups"] == current_group])
	    idx_count_in_group = len(train_df[train_df["Groups"] == current_group])

	    clf_info +=  "\n\n" + str("class = %s count = [%s / %s]" % (current_group, row[idx], idx_count_in_group))
	    clf_info +=  "\n\n" + str("predict %s accurancy = %s" % (current_group, row[idx] / idx_count_in_group))
	#     print("class = %s count = [%s / %s]" % (current_group,row[idx],str(idx_count_in_group)))
	#     print("predict %s accurancy = %s" % (current_group, row[idx] / idx_count_in_group))
	#     print()
	cnf_df = pd.DataFrame(cnf_matrix)
	cnf_df.columns = group_encoder
	cnf_df.index = group_encoder
	md_info = clf_info.replace("\n", "<br>")
	print("RANDOM FOREST SUCCESS! - cost %d seconds" % (time() - start_time))
	path = "./"
	out_path = "./testdir/"
	if not os.path.exists(out_path):
	    os.makedirs(out_path)
	if "testdir" not in os.listdir(path):
	    print("TEST Failed! -os library have some problem.")
	else:
	    print("OS SUCCESS! - ")
	all_file = glob(path)

	print("TEST SUCCESSED! - cost %d seconds" % (time() - glob_start_time))
except Exception as e:
	print("TEST FAILED")
	LOG_FILENAME = 'error_log.txt'
	logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG, filemode='w')
	logging.exception('TEST FAILED')
	raise