# https://github.com/mwielgoszewski/python-paddingoracle
from paddingoracle import BadPaddingException, PaddingOracle

import binascii
import hashlib
from pwn import *

class PadBuster(PaddingOracle):  
    def __init__(self, **kwargs):
        super(PadBuster, self).__init__(**kwargs)

    def oracle(self, data, **kwargs):
        print("[*] Trying: {}".format(binascii.hexlify(data)))

        # Example for using data to send to oracle and raise exception
        r = remote("2018shell2.picoctf.com", 22666)
        r.recvuntil("verify")
        r.recvline()
        r.sendline("S")
        r.recvuntil(": ")
        h = hashlib.sha1()
        h.update(data)
        r.sendline(binascii.hexlify(data)+binascii.hexlify(h.digest()))
        r.interactive()
        res = r.recvline()
        print(res)
        if 'Ooops' in res:
            r.close()
            #print ("[*] Padding error!")
            raise BadPaddingException
        else:
            r.close()
            #print ("[*] No padding error")
        

if __name__ == '__main__':
    encrypted_value = '09ce080ae396c673331f79957c87f1fa91a8707580e96a0e0772ad8840fc71e5dadf36ef8c526d27136b1094d5afac99764bd142a8ee619a5a4d1786d4d35348d1dfca729bce9018e202099f267f578e28f0c83c895cd0c92f8733486a4fb38929ec082065c1e83201c9e47d1855c5a436acb425dc794515b5f768eeee526871e299ffb2f1df834fa2838b7d7817edfa5949df41f3a2adfb2d74848cc800b31801ee65e5d087ca50e5bc8d3b73508e230fe77586cc33ca8b2e54606286d2627a'
    padbuster = PadBuster()
    # val = padbuster.encrypt('{"username": "guest", "expires": "2020-01-07", "is_admin": "true"}', block_size=16, iv=bytearray.fromhex(encrypted_value[:32]))
    val = padbuster.decrypt(bytearray.fromhex(encrypted_value[32:]), block_size=16, iv=bytearray.fromhex(encrypted_value[:32]))
    print(val)
    res = [v for v in val]
    print(res)
