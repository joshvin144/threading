
import os
import sys
import argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

keyword_list = ["receiver_1_worker_execution", "receiver_2_worker_execution"]
ENTRY_WORD = "Entered"
ESCAPE_WORD = "Exited"
ESCAPE_CHAR = '@'
DELIMITER_1 = "\\n"
DELIMITER_2 = ' '

def import_text_as_string(fpath = None):
	string_representation = ""
	with open(fpath, "rb") as fobject:
		string_representation = fobject.read()
		string_representation = str(string_representation)
	return string_representation

def initialize_empy_dict(keyword_list):
	empty_dict = {}
	for keyword in keyword_list:
		empty_dict[keyword] = []
	return empty_dict

def parse_string_to_dict(string_representation = None):
	parsed_dict = initialize_empy_dict(keyword_list)
	lines = string_representation.split(DELIMITER_1)
	num_lines = len(lines)
	for line_idx in range(num_lines):
		entry_words = lines[line_idx].split(DELIMITER_2)
		entry_word = entry_words[0]
		if(ENTRY_WORD == entry_word):
			entry_function = entry_words[1]
			entry_time = entry_words[-1]
			entry_time = float(entry_time)

			escape_time = 0.0
			escape_word_found = False
			while((not escape_word_found) and ((num_lines - 1) > line_idx)):
				line_idx += 1
				escape_words = lines[line_idx].split(DELIMITER_2)
				if(1 < len(escape_words)):
					escape_word = escape_words[0]
					escape_function = escape_words[1]
					if((ESCAPE_WORD == escape_word) and (entry_function == escape_function)):
						escape_word_found = True
						escape_time = escape_words[-1]
						escape_time = float(escape_time)

			diff_time = escape_time - entry_time
			if(diff_time >= 0):
				parsed_dict[entry_function].append(diff_time)

	return parsed_dict

def calculate_histogram(dictionary, keyword, plot):
	arr = np.array(dictionary[keyword], dtype = np.float32)
	n = arr.shape[0]
	num_bins = np.sqrt(n)
	num_bins = int(num_bins)
	hist, bin_edges = np.histogram(arr, num_bins)

	if(plot):
		pmf = np.divide(hist, np.sum(hist, dtype = np.float32), dtype = np.float32)
		plt.figure()
		plt.bar(x = np.arange(num_bins), height = pmf, tick_label = bin_edges[:-1])
		plt.title(keyword + " Run Time [s]")
		plt.xlabel("Run Time [s]")
		plt.ylabel("PMF")
		plt.tight_layout()
		plt.show()

	return hist

def plot_time_series(dictionary, keyword, plot):
	arr = np.array(dictionary[keyword], dtype = np.float32)
	time = np.cumsum(arr)
	if(plot):
		plt.figure()
		plt.plot(time, arr)
		plt.title(keyword + " Run Time [s]")
		plt.xlabel("Time [s]")
		plt.ylabel("Function Run Time [s]")
		plt.tight_layout()
		plt.show()
	return 0

def create_argument_parser():
	parser = argparse.ArgumentParser()
	parser.add_argument("--plot", "-p", action = "store_true")
	return parser

def main(arg = None, argv = None):
	parser = create_argument_parser()
	args = parser.parse_args()

	fpath = "./console_output.txt"
	string_representation = import_text_as_string(fpath)
	parsed_dict = parse_string_to_dict(string_representation)
	for keyword in keyword_list:
		_ = calculate_histogram(parsed_dict, keyword, args.plot)
		_ = plot_time_series(parsed_dict, keyword, args.plot)

	return 0

if __name__ == '__main__':
	_ = main()

