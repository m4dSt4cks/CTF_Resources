import argparse
import os
from pwn import *
import subprocess
import sys
import time


if not sys.warnoptions:
    import warnings
    warnings.simplefilter("ignore")

# context.aslr = False
# context.arch="amd64"

# context.log_level = 'error'	# Not very verbose
# context.log_level = 'debug'	# Very verbose

"""
LOG_LEVEL = logging.INFO
sl = logging.getLogger("script_logger")
sl.setLevel(LOG_LEVEL)
handler = logging.StreamHandler(sys.stderr)
handler.setLevel(LOG_LEVEL)
formatter = logging.Formatter('%(name)s:%(levelname)s - %(message)s')
handler.setFormatter(formatter)
sl.addHandler(handler)
"""

EXE = "./binary"
HOSTNAME = "hostname"
PORT = 0
COMMAND_SCRIPT = "./commands"
SSH_USERNAME = ""
SSH_PASSWORD = ""
SSH_HOST = ""
SSH_PORT = 22


def do_stuff(r, is_remote=False):
	r.interactive()

def do_ssh(s):
	# s['ls']
	# s.download_file('/etc/passwd')
	# s.set_working_directory("~")
	# s.checksec()
	r = s.system("./vuln")
	return r

def commands(c):
	p = subprocess.Popen(c, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	out, err = p.communicate()
	print(out.decode())
	print(err.decode())
	
if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Template PWNtools script.")
	group = parser.add_mutually_exclusive_group()
	group.add_argument("--remote", action="store_true", help="Connect to remote host", default=False)
	group.add_argument("--ssh", action="store_true", help="Connect to remote host through SSH", default=False)
	group.add_argument("--attach", action="store_true", help="Attach to the local executable with a given command file", default=False)
	group.add_argument("--debug", action="store_true", help="Debug the local executable with a given command file", default=False)
	group.add_argument("--start", action="store_true", help="Prints helpful debug info/prepares the executable", default=False)
	args = parser.parse_args(sys.argv[1:])

	if args.start:
		commands(f"chmod +x {EXE}")
		commands(f"file {EXE}")
		commands(f"ldd {EXE}")
		commands(f"checksec {EXE}")
		# TODO: search for certain strings in binary
	elif args.ssh:
		s = ssh(user=SSH_USERNAME, host=SSH_HOST, port=SSH_PORT, password=SSH_PASSWORD)
		r = do_ssh(s)
		do_stuff(r)
		r.close()
		s.close()
	elif args.remote:
		r = remote(HOSTNAME, PORT)
		do_stuff(r, True)
		r.close()
	elif args.debug:
		if COMMAND_SCRIPT:
			r = gdb.debug(EXE, open(COMMAND_SCRIPT).read())
		else:
			r = gdb.debug(EXE)
		do_stuff(r)
		r.close()
	elif args.attach:
			p = process(EXE)
		if COMMAND_SCRIPT:
			r = gdb.attach(p, open(COMMAND_SCRIPT).read())
		else:
			r = gdb.attach(p)
		do_stuff(r)
		r.close()
		p.close()
	else:
		r = process(EXE)
		do_stuff(r)
		r.close()
