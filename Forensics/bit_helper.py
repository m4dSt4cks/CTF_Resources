import sys
from tqdm import tqdm

BYTE_SIZE = 8   # really shouldn't change


""" Update this to narrow down valid strings """
def valid_range(c):
    return c >= ord(" ") and c <= ord("~")

""" Patterns must be some multiple of byte length """
def valid_pattern(p):
    for x in p:
        for y in x:
            if y >= BYTE_SIZE or y < 0:
                return False
    return len(p) > 0 and sum([len(x) for x in p]) % BYTE_SIZE == 0

def check_bits(fn, min, skip=0, pattern=[[7]] * BYTE_SIZE):
    # verify given pattern
    assert valid_pattern(pattern)
    pattern_len = len(pattern)

    results = ""
    with open(fn, "rb") as f:
        # discard skip # bytes
        f.read(skip)

        # read pattern length bytes
        current_bytes = f.read(pattern_len)
        while len(current_bytes) == pattern_len:

            # extract bits based on pattern
            extracted_bits = ""
            for i in range(pattern_len):
                cb_bits = "{:08b}".format(current_bytes[i])
                for bp in pattern[i]:
                    extracted_bits += cb_bits[bp]

            # convert bits to bytes
            extracted_bytes = [int(extracted_bits[x:x + BYTE_SIZE], 2) for x in range(0, len(extracted_bits), BYTE_SIZE)]

            # while they are valid bytes, just append, once one is invalid, decide to print based on length, reset tally
            for newb in extracted_bytes:
                if valid_range(newb):
                    results += chr(newb)
                else:
                    if len(results) >= min:
                        print(results)
                    results = ""
            
            # read pattern length bytes
            current_bytes = f.read(pattern_len)

""" Takes about 5 minutes """
def common_checks(fn, min):
    for i in tqdm(range(BYTE_SIZE)):  # skip the first 0-7 bytes
        for j in range(BYTE_SIZE):  # check MSB to LSB
            check_bits(fn, min, skip=i, pattern=[[j]] * BYTE_SIZE)

    for i in tqdm(range(BYTE_SIZE * 2)):  # skip values
        check_bits(fn, min, skip=i, pattern=[[0, 1, 2, 3], [4, 5, 6, 7]])
        check_bits(fn, min, skip=i, pattern=[[4, 5, 6, 7], [0, 1, 2, 3]])

    for i in tqdm(range(BYTE_SIZE * 3)):  # skip values
        for j in range(BYTE_SIZE):  # check MSB to LSB
            check_bits(fn, min, skip=i, pattern=[[j], [], []] * BYTE_SIZE)
            check_bits(fn, min, skip=i, pattern=[[], [j], []] * BYTE_SIZE)
            check_bits(fn, min, skip=i, pattern=[[], [], [j]] * BYTE_SIZE)
            check_bits(fn, min, skip=i, pattern=[[j], [j], []] * BYTE_SIZE)
            check_bits(fn, min, skip=i, pattern=[[], [j], [j]] * BYTE_SIZE)
            check_bits(fn, min, skip=i, pattern=[[j], [], [j]] * BYTE_SIZE)
            check_bits(fn, min, skip=i, pattern=[[j], [j], [j]] * BYTE_SIZE)

    for i in tqdm(range(BYTE_SIZE * 4)):  # skip values
        for j in range(BYTE_SIZE):  # check MSB to LSB
            check_bits(fn, min, skip=i, pattern=[[j], [], [], []] * BYTE_SIZE)
            check_bits(fn, min, skip=i, pattern=[[], [j], [], []] * BYTE_SIZE)
            check_bits(fn, min, skip=i, pattern=[[], [], [j], []] * BYTE_SIZE)
            check_bits(fn, min, skip=i, pattern=[[j], [j], [], []] * BYTE_SIZE)
            check_bits(fn, min, skip=i, pattern=[[], [j], [j], []] * BYTE_SIZE)
            check_bits(fn, min, skip=i, pattern=[[j], [], [j], []] * BYTE_SIZE)
            check_bits(fn, min, skip=i, pattern=[[j], [j], [j], []] * BYTE_SIZE)
            check_bits(fn, min, skip=i, pattern=[[], [], [], [j]] * BYTE_SIZE)
            check_bits(fn, min, skip=i, pattern=[[j], [j], [j], [j]] * BYTE_SIZE)

# may not work with PNGs based on how data was hidden (ie row vs column major order, color order, etc), use pixel_counter.py
if len(sys.argv) < 3:
    print(f"Usage: {sys.argv[0]} [filename] [min_str_length]")
    exit()
else:
    filename = sys.argv[1]
    minlen = int(sys.argv[2], 10)
    # check_bits(filename, minlen)   # quick check
    common_checks(filename, minlen) # in-depth check
