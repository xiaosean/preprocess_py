def to_numerical():
	# clean non numeric data
	# iteration avoid memory leak
	for col in df.columns[numeric_st_idx:]:
	    df[col] = pd.to_numeric(df[col], errors='coerce')
	    # let nan == 0
	#     print(col)
	    df[col] = df[col].fillna(0)
	    df[col] = df[col].astype(np.int64)
	# df = df.fillna(0)
	# # df[df.columns[numeric_st_idx:]] = df[df.columns[numeric_st_idx:]].apply(np.int64)
	# for col in df.columns[numeric_st_idx:]:
	#     df[col] = df[col].apply(np.int32)

if __name__ == '__main__':
	# set configure
	# path = "../DATA_FULL/"
	path = "D:/NEW_DATA_FULL_2017_6_14/"
	filename = "CDR_USAGE_MO_HOUR_COMPLETED"
	# relative_filename = path + filename + ".csv"
	relative_filename = path + filename + ".txt"
	out_filename = filename + "_revise.csv"
	numeric_st_idx = 2
	# chunks=pd.read_table(relative_filename ,chunksize=1000000,sep=';',\
 #       names=['lat','long','rf','date','slno'],index_col='slno',\
 #       header=None,parse_dates=['date'])
	chunks=pd.read_table(relative_filename ,chunksize=1000000,sep=';',\
		index_col='MINING_DW_SUBSCR_NO',parse_dates=['VOICE_DATE'])
	for chunk in chunks:

	del chunks
		