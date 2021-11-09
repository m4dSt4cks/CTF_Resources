NUM_VARIABLES = 10
BIT_LEN = 8 # 8 for int/char, 1 for bool
PROBLEM_NAME = "A"
RANGES = [(48, 57), (65, 90), (97, 122)] # Only numbers and letters
RANGES = [(32, 126)] # Special characters, numbers, and letters

script = "#http://ericpony.github.io/z3py-tutorial/guide-examples.htm\n\nfrom z3 import *\n\n"
script += "solver = Solver()\nfor i in range({}):\n\tglobals()['v%i' % i] = BitVec('v%i' % i, {})".format(NUM_VARIABLES, BIT_LEN)
for r in RANGES:
	script += "\n\tsolver.add(globals()['b%i' % i] >= {})\n\tsolver.add(globals()['b%i' % i] <= {})".format(r[0], r[1])
script += "\n\n"
for i in range(NUM_VARIABLES):
	script += "solver.add(b{} == )\n".format(i)
script += "\nprint('Solving...')\n\nsolver.check()\nmodl = solver.model()\n\nres = ''\n"
script += "for i in range({}):\n\tobj = globals()['b%i' % i]\n\tc = modl[obj].as_long()\n\tprint('b%i: %x' % (i, c))\n\tres = res + chr(c)\n\n".format(NUM_VARIABLES)
script += "print('Result: ' + res)"

with open(PROBLEM_NAME + "_solver.py", "w+") as d:
	d.write(script)
