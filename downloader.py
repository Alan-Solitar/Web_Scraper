from selenium import webdriver
from bs4 import BeautifulSoup
import  urllib.request
import os
import time
import subprocess
import signal
class downloader:
	__files_to_search_for = [] #list of titles you are looking for
	__file_providers=[] #provider of file
	__url = "" # url of rss feed

	#initialize member variables
	def __init__(self,url,search_for,providers):
		self.__url = url
		self.__files_to_search_for = search_for
		self.__file_providers = providers

	def run(self):
		while True:
			code = self.get_code()
			t_data = self.parse_code(code)
			t_list = self.create_t_list(t_data)
			t_to_download = self.search_t_list(t_list)
			files = self.retrieve_t_files(t_to_download)
			self.download_t(files)
		
	#create a browser session and retrieve the html
	def get_code(self):
		browser = webdriver.Firefox()
		browser.get(self.__url)
		code = browser.page_source #returns pages source code
		browser.close() #cleanup
		return code
	#takes in html code and finds all anchor tags with a an href
	def parse_code(self,html):
		parser = BeautifulSoup(html,"html.parser")
		t_data = parser.findAll('a',href=True)
		return t_data
	#takes in the t_data which contains a title and link
	def create_t_list(self,t_data):
		t_dict = {}
		for t in t_data: 
			title = t.text
			link = t['href']
			t_dict.update({title:link})	
		return t_dict
	#searches dictionary of t_files to find what the user wants
	def search_t_list(self,t_dict):
		t_to_download = {}
		for key in t_dict:
			for provider in self.__file_providers: #iterates through providers
				for title in self.__files_to_search_for: #iterates through titles
					if provider in key and title in key:
						t_to_download.update({key:t_dict[key]})
		return t_to_download
	#uses urllib.request to retrieve the file
	def retrieve_t_files(self,t_to_download):
		files = []
		for key in t_to_download:
			file_name = key + '.extension' #save file as file_name (enter extension you want)
			files.append(file_name) #keeps track of all files
			urllib.request.urlretrieve(t_to_download[key],file_name)
		print(files)
		return files
	#This function allows you execute a console command with your files
	def download_t(self,files):
		if not files:
			print("No files found. Taking a break")
			time.sleep(600)
		else:
			command = 'yourCommand'
			for f in files:
				print(f)
				name = '"' + f +'"'
				command = command + ' ' + name
			print(command)
			'''
			p1=subprocess.Popen('exec '+command, shell=True)
			time.sleep(20*60)
			p1.kill()
			'''
			
			proc = subprocess.Popen(command, shell=True, preexec_fn=os.setsid)
			time.sleep(1200)
			os.killpg(proc.pid, signal.SIGTERM)
			
