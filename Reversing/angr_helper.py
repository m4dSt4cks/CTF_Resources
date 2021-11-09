#!/usr/bin/python3

# run angr (sudo docker run -v "$(pwd)"/files:/mnt -it angr/angr)
# place this and binary in ./files/

# https://docs.angr.io/examples
import angr
import claripy
import sys

PROGRAM = "./binary"
LENGTH = 0

# https://docs.angr.io/built-in-analyses/cfg#shared-libraries
# proj = angr.Project(PROGRAM)
proj = angr.Project(PROGRAM, load_options={"auto_load_libs": False})

argv1 = claripy.BVS("argv1", LENGTH * 8)

# https://docs.angr.io/appendix/options#options
# initial_state = proj.factory.entry_state(args=[PROGRAM, argv1]) 
initial_state = proj.factory.entry_state(args=[PROGRAM, argv1], add_options={angr.options.LAZY_SOLVES})
# initial_state = proj.factory.entry_state(args=[PROGRAM, argv1], add_options={angr.options.LAZY_SOLVES, "BYPASS_UNSUPPORTED_SYSCALL"})

# Default is 60
initial_state.libc.buf_symbolic_bytes=LENGTH + 1

# Make sure none of the input bytes are NULL
for byte in argv1.chop(8):
    initial_state.add_constraints(byte != 0)
# Can add more constraints for certain letters if you know the beginning
# initial_state.add_constraints(argv1.chop(8)[0] == 'C')
    
# Simulation managers are a basic building block of the symbolic execution engine.
# They track a group of states as the binary is executed, and allows for easier
# management, pruning, and so forth of those states
sm = proj.factory.simulation_manager(initial_state)

# Can also have lists for arguments
sm.explore(find=0x400830, avoid=0x400850)

"""
# found this for looking for string printout messages: https://pwndiary.com/0ctf-2020-happytree
sm.explore(
        find=lambda s: b"Success!" in s.posix.dumps(1),
        avoid=lambda s: b"Failure!" in s.posix.dumps(1),
        step_func=lambda lsm: lsm.drop(stash='avoid'))
"""

"""
# Here's an example of breaking up a big problem into smaller ones
sm.explore(find=0x4016A3).unstash(from_stash='found', to_stash='active')
sm.explore(find=0x4016B7, avoid=[0x4017D6, 0x401699, 0x40167D]).unstash(from_stash='found', to_stash='active')
sm.explore(find=0x4017CF, avoid=[0x4017D6, 0x401699, 0x40167D]).unstash(from_stash='found', to_stash='active')
sm.explore(find=0x401825, avoid=[0x401811])
"""

# might be more items in list, so check
print(len(sm.found))
found = sm.found[0]
print(found)
solution = found.solver.eval(argv1, cast_to=bytes)
print(solution)
# solution = solution[:solution.find(b"}")+1] # Trim off the null bytes at the end of the flag (if any).

# https://docs.angr.io/examples
# https://github.com/angr/angr-doc/blob/master/docs/more-examples.md