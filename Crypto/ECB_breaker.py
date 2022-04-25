# Sorry this is old and very poorly written

import string
BLOCKSIZE = 8
BLOCKSIZE_MINUS = BLOCKSIZE - 1

# define your dictionary to guess
dictionary = string.ascii_letters + string.digits + " _"

def encrypt_stuff(PT):
	# put the method for encrypting the input here
	CT = ""
	return CT
	
def get_blocks(CT):
	result = []
	for i in range(0, len(CT), BLOCKSIZE):
		result.append(CT[i:i+BLOCKSIZE])
	return result
		
def check_blocks(blocks):
	if not blocks:
		return False
	result = False
	last = ""
	for block in blocks:
		if block == last:
			result = True
		last = block
	return result
	
def get_start_len(blocks, offset):
	last = ""
	total = -1 * offset
	cont = True
	for block in blocks:
		if cont:
			if block == last:
				total -= BLOCKSIZE
				cont = False
			else:
				total += BLOCKSIZE
				last = block
	return total
	
def create_test(pad, guess, known, diff):
	result = "A" * pad
	if len(known) < BLOCKSIZE_MINUS:
		result += "A" * (BLOCKSIZE_MINUS - len(known))
		result += known + guess
	else:
		result += known[-BLOCKSIZE_MINUS:] + guess
	result += "A" * diff
	return result

blocks = []
offset = -1
tests = ["1234567812345678", "aaaaaaa1234567812345678","aaaaaa1234567812345678","aaaaa1234567812345678","aaaa1234567812345678","aaa1234567812345678","aa1234567812345678","a1234567812345678"]

while not check_blocks(blocks):
	offset += 1
	CT = encrypt_stuff(tests[offset])
	if len(CT) % BLOCKSIZE != 0:
		print("The result was invalid!")
		exit(1)
	blocks = get_blocks(CT)
	if offset > BLOCKSIZE_MINUS:
		print("Offset not found!")
		exit(1)

start_len = get_start_len(blocks, offset)
input_len = len(tests[offset])
end_len = len(CT) - start_len - input_len
#end_offset = 8 - (end_len % 8)
print("Secret length: " + end_len)
secret = ""

first_block = (start_len + offset) / BLOCKSIZE
for i in range(end_len):
	second_block = (end_len / BLOCKSIZE) + 1 + first_block
	for letter in dictionary:
		test = create_test(offset, letter, secret, end_len - len(known))
		b = get_blocks(encrypt_stuff(test))
		if b[first_block] == b[second_block]:
			secret += letter
	print(secret)

