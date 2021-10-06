import hashlib
import string
import itertools

def arbitrary_hash_func(hash_func, base, val, front):
    letters = string.digits + string.ascii_lowercase
    for guess in itertools.combinations_with_replacement(letters, 5):
        g = (base + "".join(guess)).encode()
        h = hashlib.new(hash_func)
        h.update(g)
        if front:
            if h.hexdigest()[:len(val)] == val:
                return "".join(guess)
        else:
            if h.hexdigest()[-len(val):] == val:
                return "".join(guess)

print(arbitrary_hash_func("sha1", "ABCD", "00000", False))