from bitarray import bitarray
a = bitarray()
v = 'Hello'
a.frombytes(v.encode('utf-8'))
print(a)
