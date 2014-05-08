import urllib2
import random
import os
import math

path = os.path.abspath('./imgur_scraper')
string_length = 5 # The length of the ID to generate. 5 seems to work the best.

#Generate a random ID
def RandomID(string_length):
	chars = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
	output = ''
	index = 0
	for i in range(0, string_length):
		index = math.floor(random.random() * len(chars))
		output += chars[int(index):int(index + 1)]
	return output

#Create a folder if it doesn't exist yet
print 'Location of saved images: %s' % path
if not os.path.exists(path):
	os.makedirs(path)
	
while True:
	id = RandomID(string_length)
	filename = ''
	url = 'http://i.imgur.com/' + id + '.jpg'
	try:
		res = urllib2.urlopen(url)
	except urllib2.HTTPError as e:
		print '%s - error %d' % (id, e.code)
		continue
	data = res.read()
	type = res.info()['Content-Type']
	#check if content doesn't exist (removed.png) or if it's something we don't need
	if res.geturl() == 'http://i.imgur.com/removed.png' or type == 'text/html; charset=utf-8' or type == 'binary/octet-stream':
		print '%s - not found' % id
	else:
		if type == 'image/jpeg':
			id += '.jpg'
		elif type == 'image/png':
			id += '.png'
		elif type == 'image/gif':
			id += '.gif'
		elif type == 'image/bmp':
			id += '.bmp'
		else:
			print 'Type could not be recognized!'
			continue
		
		filename = os.path.join(path, id)
		if os.path.exists(filename):
			print 'Already exists: %s' % id
		f = open(filename, 'wb')
		f.write(data)
		f.close()
		print 'Downloaded: %s' % id
