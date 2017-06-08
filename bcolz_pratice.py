import os.path
import numpy as np
import pandas as pd
import bcolz
from time import time
from pandas.computation import expressions as expr

# https://github.com/Blosc/bcolz
# $ conda install -c conda-forge bcolz
# or
# $ pip install -U bcolz
# tutorial
# http://nbviewer.jupyter.org/github/Blosc/movielens-bench/blob/master/querying-ep14.ipynb
def bcolz_setting():
	# Global settings for bcolz and pandas (for experimenting, modify some of the lines below)
	bcolz.defaults.cparams['cname'] = 'blosclz'
	bcolz.defaults.cparams['clevel'] = 1
	bcolz.defaults.eval_vm = "numexpr"
	bcolz.blosc_set_nthreads(4)
	bcolz.numexpr.set_num_threads(4)
	expr.set_use_numexpr(True)
	expr.set_numexpr_threads(1)
if __name__ == '__main__':
	# bcolz.print_versions()
	# bcolz_setting()
	# Load the ratings in a pandas dataframe
	t0 = time()
	# pass in column names for each CSV
	wants_cols = ['MINING_DW_SUBSCR_NO', 'VAS_HR06_BYTE']
	path = "../"
	filename = "output_DM_SUBSCR_VAS_VOL_PRD_MLY_2017-04-01_100"
	relative_filename = path + filename + ".xlsx"
	# tags = pd.read_csv(ftags, sep=';', names=t_cols)
#print("Info for tags:", tags.info())

	voice_pd = pd.read_excel(relative_filename)
	print("Time for parsing the data: %.2f" % (time()-t0,)) 

	print("Info for movie_ratings:", voice_pd.info())
	# movie_ratings = pd.merge(movies, ratings)


	# Get a bcolz ctable out of the lens dataframe (using compression by default)
	t0 = time()
	zlens = bcolz.ctable.fromdataframe(voice_pd)
	print("time for ctable conversion: %.2f" % (time()-t0))
	#print repr(zlens)

	# Get rid of the dataframe to cleanup memory
	# del lens

	# Simple query
	t0 = time()
	result = zlens["MINING_DW_SUBSCR_NO == 10001169113"]
	zsmplqtime = time() - t0
	print("time (and length) for simple query with bcolz: %.2f (%d)" %
	      (zsmplqtime, len(result)))
	print(result)
	#print repr(result)
