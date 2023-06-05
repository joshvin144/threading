import os
import sys
import time

def function_run_time(function):
	def record_function_run_time(*args, **kwargs):
		entry_time = time.time()
		print(f"Entered {function.__name__} @ {entry_time}")
		return_value = function(*args, **kwargs)
		exit_time = time.time()
		print(f"Exit {function.__name__}  @ {exit_time}")
		return return_value
	return record_function_run_time

