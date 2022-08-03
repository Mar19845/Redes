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
    import socket	
    def xor(a, b):

        # initialize result
        result = []
        # Traverse all bits, if bits are
        # same, then XOR is 0, else 1
        for i in range(1, len(b)):
            if a[i] == b[i]:
                result.append('0')
            else:
                result.append('1')

        return ''.join(result)



"""
https://www.geeksforgeeks.org/cyclic-redundancy-check-python/
https://github.com/iamhimanshu0/CRC/blob/master/CRC.py


    def posRedundantBits(data, r):
     
    # Redundancy bits are placed at the positions
    # which correspond to the power of 2.
    j = 0
    k = 1
    m = len(data)
    res = ''
 
    # If position is power of 2 then insert '0'
    # Else append the data
    for i in range(1, m + r+1):
        if(i == 2**j):
            res = res + '0'
            j += 1
        else:
            res = res + data[-1 * k]
            k += 1
 
    # The result is reversed since positions are
    # counted backwards. (m + r+1 ... 1)
    return res[::-1]
 
 
def calcParityBits(arr, r):
    n = len(arr)
 
    # For finding rth parity bit, iterate over
    # 0 to r - 1
    for i in range(r):
        val = 0
        for j in range(1, n + 1):
 
            # If position has 1 in ith significant
            # position then Bitwise OR the array value
            # to find parity bit value.
            if(j & (2**i) == (2**i)):
                val = val ^ int(arr[-1 * j])
                # -1 * j is given since array is reversed
 
        # String Concatenation
        # (0 to n - 2^r) + parity bit + (n - 2^r + 1 to n)
        arr = arr[:n-(2**i)] + str(val) + arr[n-(2**i)+1:]
    return arr
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

