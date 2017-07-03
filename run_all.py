import os
from os import listdir
import threading

limit = 8
# python_file = 'boxplot.py'
# python_file = 'time_distribution.py'
# python_file = 'boxplot_workday_holiday.py'
# python_file = 'multi_kmeans_get_graph.py'
# python_file = 'kmeans_error.py'
python_file = 'multi_kmeans_get_label.py'
# python_file1 = 'multi_kmeans_group_stacked_bar.py'
# python_file2 = 'multi_kmeans_group_line_chart.py'
# python_file = 'multi_kmeans.py'
# path = "CDR_ANALYZE"
# path = "CDR_FINAL_NORMALIZE"
path = "CDR_FINAL"

thread_list = []

for file_name in listdir(path):
	# filename filter
	# if file_name.find('.csv') == -1 or file_name.find('4') == -1 or file_name.find('WORK') != -1 or file_name.find('HOLI') != -1:
	# if file_name.find('.csv') == -1 or file_name.find('table_with_kid') == -1 or file_name.find('all') != -1 or file_name.find('z_norm') != -1:
	if file_name.find('.csv') == -1 or file_name.find('all') != -1 or file_name.find('z_norm') != -1 or (not "dna_hours_divide_with" in file_name) or "seldom" in file_name or "None" in file_name:
		continue
	# thread_list.append(threading.Thread(target = (lambda fname: print(os.system('python ' + python_file + ' ' + fname + " TIME"))), args = [file_name]))
	# thread_list.append(threading.Thread(target = (lambda fname: print(os.system('python ' + python_file + ' ' + fname + " CNT"))), args = [file_name]))
	thread_list.append(threading.Thread(target = (lambda fname: print(os.system('python ' + python_file + ' ' + fname))), args = [file_name]))
	# if file_name.find('DAY') != -1 or file_name.find('HOUR') != -1:
	# 	thread_list.append(threading.Thread(target = (lambda fname: print(os.system('python ' + python_file2 + ' ' + fname))), args = [file_name]))
	# elif file_name.find('TELEGRAM') != -1 or file_name.find('USAGE') != -1:
	# 	thread_list.append(threading.Thread(target = (lambda fname: print(os.system('python ' + python_file1 + ' ' + fname))), args = [file_name]))

started = []
for i in range(len(thread_list)):
	if len(started) < limit:
		started.insert(0, i)
		thread_list[i].start()
	else:
		thread_list[started.pop()].join()
		started.insert(0, i)
		thread_list[i].start()