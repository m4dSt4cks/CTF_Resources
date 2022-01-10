import sys
try:
    fn1 = sys.argv[1]
    fn2 = sys.argv[2]
    fn3 = sys.argv[3]
except:
    print(f"Usage: python {sys.argv[0]} [file1] [file2] [output_file]")
    exit()
try:
    d1 = open(fn1, "rb").read()
    d2 = open(fn2, "rb").read()
    of = open(fn3, "w+b")
except:
    print("Check input files exist and output file can be written")
    exit()
result = list(x ^ y for x, y in zip(d1, d2))
if len(d1) > len(d2):
    remainder = d1[len(result):]
else:
    remainder = d2[len(result):]
of.write(bytes(result))
of.write(bytes(remainder))
print("Finished.")
