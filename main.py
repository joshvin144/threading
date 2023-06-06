
import os
import sys
import time
import queue
import threading

#### BEGIN USER DEFINED MODULES ####
import utilities
#### END USER DEFINED MODULES ####

# BEGIN CONSTANTS ####
MESSAGE_QUEUE_CAPACITY = 10
NUM_MESSAGES = 1000
TIME_DELAY_BETWEEN_MESSAGES = 0.001 # [s]
TIME_DELAY_WITHIN_THREAD = 0.025 # [s]
# END CONSTANTS ####

# Instantiate a queue to pass messages between threads
message_queue = queue.Queue(MESSAGE_QUEUE_CAPACITY)

# Helper function for receiver_1_worker
@utilities.function_run_time
def receiver_1_worker_execution(results_dict = None):
	message = message_queue.get()
	print(f"Reciever 1 retrieved a message from the message queue: {message}")
	if(None != results_dict):
		results_dict["receiver_1_results"].append(message)
	time.sleep(TIME_DELAY_WITHIN_THREAD)

# Helper function for receiver_2_worker
@utilities.function_run_time
def receiver_2_worker_execution(results_dict = None):
	message = message_queue.get()
	print(f"Reciever 2 retrieved a message from the message queue: {message}")
	if(None != results_dict):
		results_dict["receiver_2_results"].append(message)

# Loop to continuously check the queue for messages
# If we wrap the receiver_1_worker in the utilities.function_run_time decorator,
# any and all console output will appear after the receiver_1_thread is terminated.
# Therefore, we need a helper function, receiver_1_worker_execution, to call from within receiver_1_worker.
# We may wrap this helper function in the function_run_time decorator.
# Now, any and all console output will appear when receiver_1_worker_execution is called.
def receiver_1_worker(results_dict = None):
	while(True):
		receiver_1_worker_execution(results_dict)

# Loop to continuously check the queue for messages
def receiver_2_worker(results_dict = None):
	while(True):
		receiver_2_worker_execution(results_dict)

@utilities.function_run_time
def print_function():
	print("This is how long it takes to print to the terminal through Python3.11")
	return 0

def main(arg = None, argv = None):
	# What is the run time of print() in python?
	return_value = print_function()

	# Results dictionary to pass between threads
	results_dict = {"receiver_1_results" : [], "receiver_2_results" : []}

	receiver_1_thread = threading.Thread(target = receiver_1_worker, args = (results_dict,), daemon = True)
	receiver_2_thread = threading.Thread(target = receiver_2_worker, args = (results_dict,), daemon = True)
	
	receiver_1_thread.start()
	receiver_2_thread.start()

	# Send messages
	for i in range(NUM_MESSAGES):
		message = f"Message {i}"
		message_queue.put(message)
		time.sleep(TIME_DELAY_BETWEEN_MESSAGES)

	print(results_dict)
	return 0

if __name__ == '__main__':
	_ = main()

