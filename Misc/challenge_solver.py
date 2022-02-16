import hashlib
import string
import itertools

alphabet = string.digits + string.ascii_lowercase
# alphabet = string.printable

def arbitrary_hash_func(hash_func, base, val, front):
    for guess in itertools.combinations_with_replacement(alphabet, 5):
        g = (base + "".join(guess)).encode()
        h = hashlib.new(hash_func)
        h.update(g)
		
        if front:
            if h.hexdigest()[:len(val)] == val:
                return "".join(guess)
        else:
            if h.hexdigest()[-len(val):] == val:
                return "".join(guess)

def arbitrary_hash_func_0bitstart(hash_func, base, nbits):
    for guess in itertools.combinations_with_replacement(alphabet, 5):
        g = (base + "".join(guess)).encode()
        h = hashlib.new(hash_func)
        h.update(g)
		
        hex_data = h.hexdigest()
        full_len = len(hex_data) * 4
        front_slice = int(hex_data, 16) >> (full_len - nbits)
        if not front_slice:
            return "".join(guess)

# print(arbitrary_hash_func("sha1", "ABCD", "00000", False))
print(arbitrary_hash_func_0bitstart("sha256", "ABCD", 26))
