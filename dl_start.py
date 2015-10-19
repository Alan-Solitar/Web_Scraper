#Copyright 2015, Alan Solitar, All rights reserved.
from downloader import downloader
import downloader_settings
import pickle
import time
import os
import sys
import inspect
import signal

#Get a list of providers and titles from text files
def get_info():
	providers = downloader_settings.read_list('providers.txt')
	searching_for = downloader_settings.read_list('searching_for.txt')
	return providers, searching_for

file_providers, searching_for = get_info()
url ='http://www.AnRSSFeed.com' # dummy name ( replace it if you want to test this out)
#Uses the inspect library to return the number of arguments of a given function
def number_of_arguements(function):
	num_args = len(inspect.getargspec(function).args)
	return num_args

#Write providers and titles to text files
def write_info():
	downloader_settings.write_list('providers.txt',file_providers)
	downloader_settings.write_list('searching_for.txt',searching_for)

def display_titles():
	print(searching_for)
def display_providers():
	print(file_providers)
def add_titles(titles):
	for title in titles:
		searching_for.append(title)
	searching_for.sort()
def add_providers(providers):
	for provider in providers:
		file_providers.append(provider)
	file_providers.sort()
def del_titles(titles):
	for title in titles:
		searching_for.remove(title)
	searching_for.sort()
def del_providers(providers):
	for provider in providers:
		file_providers.remove(provider)
	file_providers.sort()
def clear_all():
	del file_providers[:]
	del searching_for[:]
def clear_titles():
	del searching_for[:]
def clear_providers():
	del file_providers[:]
def save():
	write_info()
def exit_program():
	sys.exit()
#Start Downloader
def run_downloader():
	d = downloader(url,searching_for,file_providers)
	write_info()
	d.run()
def switch(command,arguements):
	switch_statement = {
	"run":run_downloader,
	"add_title":add_titles,
	"remove_title":del_titles,
	"add_provider":add_providers,
	"remove_provider":del_providers,
	"clear_all":clear_all,
	"clear_providers":clear_providers,
	"clear_titles":clear_titles,
	"providers":display_providers,
	"titles":display_titles,
	"save":save,
	"exit":exit_program
	}
	if command in switch_statement.keys():
		number_args = number_of_arguements(switch_statement[command])
		if number_args ==0:
			return switch_statement[command]()
		else:
			return switch_statement[command](arguements)
	else:
		print("Command not recognized")

main_command = ""
while main_command!="run_auto":
	user_string = input(">>> ")
	arguements = user_string.split()
	main_command = arguements[0]
	del arguements[0]
	switch(main_command,arguements)
run_downloader()


