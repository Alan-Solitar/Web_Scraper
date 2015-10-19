#Copyright 2015, Alan Solitar, All rights reserved.
import pickle
import os
def write_list(text_file, a_list):
	writer = open(text_file,'wb')
	pickle.dump(a_list,writer)
	writer.close()
def read_list(text_file):
	a_list= []
	if os.stat(text_file).st_size == 0:
		return a_list
	else:	
		reader = open(text_file,'rb')
		a_list = pickle.load(reader)
		reader.close()
		a_list.sort()
		return a_list
