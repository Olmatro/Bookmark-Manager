'''
Author 	: Jay Rambhia
email 	: jayrambhia777@gmail.com
Git 	: https://github.com/jayrambhia
gist 	: https://gist.github.com/jayrambhia
=============================================
Name	: bookmarkreader
Repo    : Bookmark-Manager
git     : https://github.com/jayrambhia/Bookmark-Manager
version	: 0.2
gist 	: https://gist.github.com/1719957 # old gist. Supports version 0.1. Does not support chrome.
'''

import gdbm
import pickle
import os

def __getDB():
	'''
	Returns bookmark gdbm databse if found
	'''
	filename = __getFilename()
	if not filename:
		return
	if os.path.isfile(filename):
		db = gdbm.open(filename,'c')
		if db.has_key('@author@'):
			name, email, add_date = pickle.loads(db['@author@'])
			if name == 'Jay Rambhia'and email == 'jayrambhia777@gmail.com':
				return db
				
	print 'Bookmark database not found'
	return None
	
def __getFilename():
	'''
	Returns path of the bookmark database if found
	'''
	dirs = os.listdir('.')
	if 'bookmarkDB' in dirs:
		filename = 'bookmarkDB'
		file_path = os.path.join(os.path.abspath('.'),filename)
		print file_path
		
		return file_path
	else:
		print 'bookmark database not found'
		print '1. Search for bookmark database'
		print '2. Enter bookmark database name'
		print '3. Exit'
		n = int(raw_input())
		if n == 1 :
			for path, dirs, filenames in os.walk(os.environ['HOME']):
				if 'bookmarkDB' in filenames:
					break
			
			file_path = os.path.join(path,'bookmarkDB')
			return file_path
		elif n == 2:	
			filename = str(raw_input('File Name: '))
			print filename
			if os.path.isfile(filename):
				path, file_name = os.path.split(filename)
				print path
				if path:
					return filename
				file_path = os.path.join(os.path.abspath('.'),filename)
				return file_path
			else:
				print 'Bookamrk database not found'
				return None
		elif n==3:
			print 'Exit'
			return None
		else:
			__getFilename()
			
def bookmarkReader(db):
	'''
	Prints all the bookmarks from the bookmark database
	'''
	if not db:
		return
	keys = db.keys()
	
	author_tuple = pickle.loads(db['@author@'])
	name, email, add_date = author_tuple
	print 'Author:',name
	print 'email:',email
	
	keys.remove('@author@')
	bookmark_list = []
	for key in keys:
		bookmark_tuple = (key,pickle.loads(db[key]))
		bookmark_list.append(bookmark_tuple)
		
	bookmark_list.sort(key = lambda b:b[1][1])
	for bookmark in bookmark_list:
		print bookmark[1][0],'tag:',bookmark[1][1]
		print bookmark[0]
		print ''
	
	return
	
if __name__ == '__main__':
	db = __getDB()
	bookmarkReader(db)	
		
