import os
from os import listdir
import threading

limit = 5
python_file = 'boxplot.py'
# python_file = 'time_distribution.py'

thread_list = []

for file_name in listdir():
	if file_name.find('.csv') == -1:
		continue
	thread_list.append(threading.Thread(target = (lambda fname: print(os.system('python ' + python_file + ' ' + fname + " TIME"))), args = [file_name]))
	thread_list.append(threading.Thread(target = (lambda fname: print(os.system('python ' + python_file + ' ' + fname + " CNT"))), args = [file_name]))

started = []
for i in range(len(thread_list)):
	if len(started) < limit:
		started.insert(0, i)
		thread_list[i].start()
	else:
		thread_list[started.pop()].join()
		started.insert(0, i)
		thread_list[i].start()