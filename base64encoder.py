import base64
import binascii

file = "static/categories/category1/smiling.jpg"
f = open(file, 'r')
string = f.read()
print(string)
encodedString = base64.b64encode(string)
print(encodedString)
