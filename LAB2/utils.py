from bitarray import bitarray
import binascii


class HAMMING:
  def __init__(self, bits=None):
    if (bits is not None):
          self.data = ''.join(str(n) for n in bits)

  def generate(self):
    bits = self.data[:]
    m = len(bits)
    redundat_bits = 0
    for i in range(m):
      if(2**i >= m + i + 1):
        redundat_bits = i
        break

    j = 0
    k = 1
    res = ''
    for i in range(1, m + redundat_bits+1):
      if(i == 2**j):
        res = res + '0'
        j += 1
      else:
        res = res + bits[-1 * k]
        k += 1
    full_bits = res[::-1]
    
    n = len(full_bits)
    for i in range(redundat_bits):
      val = 0
      for j in range(1, n + 1):
        if(j & (2**i) == (2**i)):
          val = val ^ int(full_bits[-1 * j])
      full_bits = full_bits[:n-(2**i)] + str(val) + full_bits[n-(2**i)+1:]
    return full_bits

  def checkError(self, arr):
    n = len(arr)
    num_parity = 0
    res = 0

    for bit_pos in range(n):
      if (2**bit_pos >= n):
        break
      else:
        num_parity += 1
    
    for i in range(num_parity):
      val = 0
      for j in range(1, n + 1):
        if(j & (2**i) == (2**i)):
          val = val ^ int(arr[-1 * j])
      res = res + val*(10**i)
    return int(str(res), 2)

  def get_original(self, bits):
    j = 0
    result = ''
    reversed_bits = bits[::-1]

    for i in range(1, len(bits) + 1):
      if(2**j == i):
        j += 1
      else:
        result += reversed_bits[i-1]
    return result[::-1]


# Import socket module

class CRC32:
    	
	def __init__(self):
		self.cdw = ''

	def xor(self,a,b):
		result = []
		for i in range(1,len(b)):
			if a[i] == b[i]:
				result.append('0')
			else:
				result.append('1')
		return  ''.join(result)



	def crc(self,message, key):
		pick = len(key)
		tmp = message[:pick]

		while pick < len(message):
			if tmp[0] == '1':
				tmp = self.xor(key,tmp)+message[pick]
			else:
				tmp = self.xor('0'*pick,tmp) + message[pick]

			pick+=1

		if tmp[0] == "1":
			tmp = self.xor(key,tmp)
		else:
			tmp = self.xor('0'*pick,tmp)

		checkword = tmp
		return checkword

	def encodedData(self,data,key):
		l_key = len(key)
		append_data = data + '0'*(l_key-1)
		remainder = self.crc(append_data,key)
		codeword = data+remainder
		self.cdw += codeword
		print("Remainder: " ,remainder)
		print("Data: " ,codeword)

	def reciverSide(self,key,data):
		r = self.crc(data,key)
		size = len(key)
		print(r)
		if r == size*0:
			print("No Error")
		else:
			print("Error")



"""
data = '100100'
key = '1001'
c = CRC()
c.encodedData(data)
print('---------------')
c.reciverSide(c.cdw)
print('---------------')
print(c.cdw)


https://www.geeksforgeeks.org/cyclic-redundancy-check-python/
https://github.com/iamhimanshu0/CRC/blob/master/CRC.py
"""
#fletcher
class FLETCHER:
    def __init__(self, message):
        self.message = message
        self.blockCount = int(len(message) / 8)
        self.blocks = []

    def defineBlocks(self):
        messageBlocks = []
        for i in range(0, self.blockCount):
            singleBlock = ''
            for j in range(0, 8):
                singleBlock += str(self.message[i*8 + j])
            messageBlocks.append(int(singleBlock, 2))
        return(messageBlocks)

    def encode(self):
        self.blocks = self.defineBlocks()
        c1, c2 = 0, 0
        for block in self.blocks:
            c1 += block
            c2 += c1
        c1 = c1 % 256
        c2 = c2 % 256
        self.blocks.append(c1)
        self.blocks.append(c2)
        return self.writeOutput()
    
    def writeOutput(self):
        encoded = ''
        for block in self.blocks:
            encoded += str(format(block,'08b'))
        return encoded

