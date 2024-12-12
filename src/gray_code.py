# gray code is a binary numeral system where two successive values differ in only one bit

def gray_code(n):
    return n ^ (n >> 1)

def gray_code_dif_bit(a, b): # a and b are gray codes of two adjacent integers
    dif = a ^ b
    dif_pos = 0 # position of the different bit from LSB
    while (dif > 0):
        if (dif & 1):
            return dif_pos
        dif = dif >> 1
        dif_pos += 1
    return -1

def get_Nth_bit(bin, N): # get Nth bit from LSB
    return (bin >> N) & 1