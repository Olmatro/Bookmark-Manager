'''
Author 	: Jay Rambhia
email 	: jayrambhia777@gmail.com
Git 	: https://github.com/jayrambhia
gist 	: https://gist.github.com/jayrambhia
=============================================
Name	: bookmarkFirefox
Repo    : Bookmark-Manager
version	: 0.2
gist 	: https://gist.github.com/1719957 # old gist. Supports version 0.1
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
		if 'bookmarkbackups' in dirs:
			break
			
	dir_path = os.path.join(path,'bookmarkbackups')
	
	if os.path.isdir(dir_path):
		return dir_path
	else:
		return None
	
def __getFile():
	'''
	eturns filename with absoulte path of the browser bookmark backup if found
	'''
	path = __getPath()
	filename = None
	if path:
		files = os.listdir(path)
		files.sort()
		filename = os.path.join(path, files[-1])
	
	return filename
	
def getBookmarks():
	'''
	If browser bookmark backup file found,
	Returns a dictionary object with bookmark url as key and (title, tag, add_date) tuple as value. 
	'''
	filename = __getFile()
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
			f[key] = pickle.dumps(bookmark_dict[key])
	
	if f.keys():		
		bookmark_dict = {}
	for key in f.keys():
		bookmark_dict[key] = pickle.loads(f[key])
	if f.has_key('@author@'):
		name, email, add_date = pickle.loads(f['@author@'])
		modified_date = time.time()
		f['@author@'] = pickle.dumps((name, email, add_date))
	else:
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
	f = open(filename)
	con = json.load(f)
	f.close()
	bookmark_dict = {}
	# Get Bookmarks Menu / Bookmarks toolbar / Tags / Unsorted Bookmarks
	con_list = con['children'] # this list will have all of the above mentioned things
    
	for i in range(len(con_list)):
		con_sub_list = con_list[i]['children']  # Access them individually
		for tags in con_sub_list:
			if tags.has_key('children'): # Accessing Tags # get tag list
				bookmarks = tags['children'] # get all the bookmarks corresponding to the tag
				if bookmarks:
					for bookmark in bookmarks: # Access each bookmark
						Tag = tags['title']
						uri = bookmark['uri']
						title = bookmark['title']
						dateAdded =  bookmark['dateAdded'] # it gives a long int eg. 1326378576503359L
						add_date = dateAdded/1000000  # The output of time.time() would be 1326378576.503359
						#lastModified = bookmark['lastModified']
						#modified_date = lastModified/1000000
						bookmark_dict[uri] = (repr(title), Tag, add_date)
						
			else:
				if (tags['title'] != 'Recently Bookmarked' 
                        and tags['title'] != 'Recent Tags' 
                        and tags['title'] != 'Most Visited' 
                        and con_list[i]['title'] != 'Bookmarks Menu'):
                    # Accessing Unsorted Bookmarks
					Tag = con_list[i]['title']
					title = tags['title']
					uri = tags['uri']
					
					dateAdded =  tags['dateAdded']
					add_date = dateAdded/1000000
                    
					#lastModified = tags['lastModified']
					#modified_date = lastModified/1000000
					
					bookmark_dict[uri] = (repr(title), Tag, add_date)	
    
	return bookmark_dict

if __name__ == '__main__':
	getBookmarks()
