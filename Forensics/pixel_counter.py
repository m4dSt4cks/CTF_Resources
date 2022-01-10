from PIL import Image
import collections

IMAGE1 = ""
IMAGE2 = ""
OUTPUT = ""

img1 = Image.open(IMAGE1)
pixels1 = img1.load()
# img2 = Image.open(IMAGE2)
# pixels2 = img2.load()

# img3 = Image.new('RGBa', (img1.size[0],img1.size[1]))
# pixels3 = img3.load()

r_list = []
g_list = []
b_list = []
a_list = []

pixel_count = 0
for row in range(img1.size[1]):
	for col in range(img1.size[0]):
		
		r = pixels1[col, row][0]
		g = pixels1[col, row][1]
		b = pixels1[col, row][2]
		a = pixels1[col, row][3]
		# print("r=", r, ", g=", g, ", b=", b, ", a=", a)
		r_list.append(r)
		g_list.append(g)
		b_list.append(b)
		a_list.append(a)
		pixel_count += 1
		
		# pixels3[col, row] = (r, g, b, a)

print("*" * 20 + " # Pixels " + "#" * 20)
print(pixel_count)
print("*" * 50)
print("*" * 20 + " # Red " + "*" * 20)
print(collections.Counter(r_list))
print("*" * 50)
print("*" * 20 + " # Green " + "*" * 20)
print(collections.Counter(g_list))
print("*" * 50)
print("*" * 20 + " # Blue " + "*" * 20)
print(collections.Counter(b_list))
print("*" * 50)
print("*" * 20 + " # Alpha " + "*" * 20)
print(collections.Counter(a_list))
print("*" * 50)
# img3.save(OUTPUT)
# img3.show()
