'''
Author 	: Jay Rambhia
email 	: jayrambhia777@gmail.com
Git 	: https://github.com/jayrambhia
gist 	: https://gist.github.com/jayrambhia
=============================================
Name	: bookmarkChrome
Repo    : Bookmark-Manager
Git     : https://github.com/jayrambhia/Bookmark-Manager
version	: 0.2
'''

import os
import json
import pickle
import gdbm
import time

def __getPath():
	'''
	Returns directory path of browser bookmark backup if found
	'''
	for path, dirs, files in os.walk(os.environ['HOME']):
		if 'Default' in dirs:
			if os.path.split(path)[-1] == 'google-chrome':
				break
			
	dir_path = os.path.join(path,'Default')
	
	if os.path.isdir(dir_path):
		return dir_path
	else:
		return None
	
def __getFile():
	'''
	Returns filename with absoulte path of the browser bookmark backup if found
	'''
	path = __getPath()
	if path:
		#files = os.listdir(path)
		#files.sort()
		filename = os.path.join(path, 'Bookmarks')
	
	return filename
	
def getBookmarks():
	'''
	If browser bookmark backup file found,
	Returns a dictionary object with bookmark url as key and (title, tag, add_date) tuple as value. 
	'''
	filename = __getFile()
	print filename
	if not filename:
		print 'No bookmark backup found!'
		return
	bookmark_dict = getBookmarkDict(filename)
	return bookmark_dict

def getBookmarkDict(filename):
	'''
	Input: Absolute path of browser bookmark backup file
	Creates/Updates Bookamrk-Manager database
	Returns a dictionary object with bookmark url as key and (title, tag, add_date) tuple as value. 
	'''
	f = gdbm.open('bookmarkDB','c')
	bookmark_dict = fetchBookmarks(filename)
	
	if bookmark_dict:
		for key in bookmark_dict:
			if not f.has_key(key):
				f[key] = pickle.dumps(bookmark_dict[key])
	
	if f.keys():		
		bookmark_dict = {}
	for key in f.keys():
		bookmark_dict[key] = pickle.loads(f[key])
	if not f.has_key('@author@'):
		name = 'Jay Rambhia'
		email = 'jayrambhia777@gmail.com'
		add_date = time.time()
		f['@author@'] = pickle.dumps((name, email, add_date))
	print 'bookmarks saved'
	f.close()	
	return bookmark_dict
		
	

def fetchBookmarks(filename):
	'''
	Decodes browser bookmark backup files using json
	Returns a dictionary with bookmark url as key and (title, tag, add_date) tuple as value
	'''
	f = open(filename,'r')
	con = json.load(f)
	f.close()
	bookmark_dict = {}
    # bookmark_bar
	con_list = con['roots'] # Access the roots
    
	bookmark_bar = con_list['bookmark_bar']
	tags = bookmark_bar['children'] # Contains unsorted bookmarks and Tags
	for tag in tags:
		if tag.has_key('children'):  # Tags / or stored in folder
			Tag = tag['name']
			bookmarks = tag['children']
			for bookmark in bookmarks:
				if bookmark['type'] == 'url':
					uri = bookmark['url']
					title = bookmark['name']
					dateAdded = int(bookmark['date_added'])
					add_date = dateAdded/10000000
				
					#print Tag, title 
					#print 'saved on:',time.ctime(add_date)
					#print uri
					#print ''
			
					bookmark_dict[uri] = (repr(title), Tag, add_date)
			
		else:	# Unsorted Bookmarks
			if tag['type'] == 'url':
				bookmark = tag
				uri = bookmark['url']
				title = bookmark['name']
				dateAdded = int(bookmark['date_added'])
				add_date = dateAdded/10000000
				Tag = 'Unsorted Bookmarks'
			
			#print Tag, title 
			#print 'saved on:',time.ctime(add_date)
			#print uri
			#print ''
			
				bookmark_dict[uri] = (repr(title), Tag, add_date)

	return bookmark_dict

if __name__ == '__main__':
	getBookmarks()

