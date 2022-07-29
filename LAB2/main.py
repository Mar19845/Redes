from bitarray import bitarray
a = bitarray()
v = 'Hello'
a.frombytes(v.encode('utf-8'))
#print(a)

#convertir bitarray a string
l = a.tolist()

#print(bitarray(l).tobytes().decode('utf-8'))


import random
random.random() # Gives you a number BETWEEN 0 and 1 as a float
err = 0.1
#print(round(random.random(),1)) # Gives you a number EITHER 0 and 1 
prob = round(random.random(),2)


if prob == err:
    print('hay error')
else:
    print(prob,err)