#!/usr/bin/env python3

import argparse
import os
from pwn import *
import subprocess
import sys
import time
import IPython
import signal
import logging
import string


if not sys.warnoptions:
    import warnings
    warnings.simplefilter("ignore")
    
def ff():
    os.system('kill %d' % os.getpid())

def sig_handler(signum, frame):
    IPython.embed(banner1="End the program with ff()", confirm_exit=False)

signal.signal(signal.SIGINT, sig_handler)


# context.aslr = False
# context.arch="amd64"
context.log_level = 'warning'    # 'debug' 'info' 'warning' 'error' 'critical'
# log.info()

EXE = "./binary"
HOSTNAME = "hostname"
PORT = 0
COMMAND_SCRIPT = "./commands"
SSH_USERNAME = ""
SSH_PASSWORD = ""
SSH_HOST = ""
SSH_PORT = 22

def rl(r):
    return r.recvlineS().rstrip()
    
def rb(r, nb):
    return u64(r.recv(nb).rstrip().ljust(8, b'\0'))


def do_stuff(r, is_remote=False):
    # r.settimeout(10)
    # r.sendline()
    # r.recvlineS()
    # r.sendlineafter()
    # recvline_startswithS()
    # recvline_endswithS()
    # There's also regex functions, etc
    
    # r.recvrepeat(timeout)
    # r.stream()
    # r.wait()
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


parser = argparse.ArgumentParser(description="Template PWNtools script.")
group = parser.add_mutually_exclusive_group()
group.add_argument("--remote", action="store_true", help="Connect to remote host", default=False)
group.add_argument("--ssh", action="store_true", help="Connect to remote host through SSH", default=False)
group.add_argument("--attach", action="store_true", help="Attach to the local executable with a given command file", default=False)
group.add_argument("--debug", action="store_true", help="Debug the local executable with a given command file", default=False)
group.add_argument("--start", action="store_true", help="Prints helpful debug info/prepares the executable", default=False)
group.add_argument("--strace", action="store_true", help="Stores strace output in strace_output", default=False)
group.add_argument("--heap", action="store_true", help="Runs heaptracer on binary, stores output in heaptrace_output", default=False)
args = parser.parse_args(sys.argv[1:])

if args.start:
    commands(f"chmod +x {EXE}")
    commands(f"file {EXE}")
    commands(f"ldd {EXE}")
    commands(f"checksec {EXE}")
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
        gdb.attach(p, open(COMMAND_SCRIPT).read())
    else:
        gdb.attach(p)
    do_stuff(p)
    p.close()
elif args.strace:
    r = process(["strace", "-o", "strace_output", "-f", EXE])
    do_stuff(r)
    r.close()
elif args.heap:
    r = process(["/home/madstacks/heaptrace/heaptrace", EXE], stderr=open("heaptrace_output", "w+"))
    do_stuff(r)
    r.close()
else:
    r = process(EXE)
    do_stuff(r)
    r.close()
