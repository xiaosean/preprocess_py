# preprocess_py

preprocess_csv.ipynb:
	it will filter string and apply to int64
	just set some variable and set what's columns u wants!

step1:
	csv_lookhead
		can watch first 10 data
step2:
	preprocess_csv
		let csv or txt to csv
			1.can remove null age[option]
			2.remove id == ?
			3.fill na to 0 in every numeric col 
step3:
	Date_Slice
		let data can be splited by month
		if data is very large, can use Date_Slice_iteration
step3-1:
	Rename column bcz MT and MO table
step4:
	Date_Aggregate
		let data aggregate by id use sum()
step5:
	Date_Aggregate_week
		sum weekday and holiday

