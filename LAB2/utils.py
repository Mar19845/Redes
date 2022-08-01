from bitarray import bitarray


def parity_kr(bit_array):
    
    num_bit = 0
    parity = True
    for bit in bit_array:
        if bit == 1:
            num_bit += 1
    
    if num_bit % 2 == 0:
        parity = False
        
    return num_bit,parity