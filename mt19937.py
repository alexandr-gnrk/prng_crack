from int_overflow import int_overflow

# https://jazzy.id.au/2010/09/22/cracking_random_number_generators_part_3.html
class MT19937():
    """MT19937
    Implementation of the general Mersenne Twister algorithm (32-bit MT19937)
    https://en.wikipedia.org/wiki/Mersenne_Twister
    """
    # Set w, n, m, r, a, u, d, s, b, t, c, l, and f  
    # coefficients for 32-bit MT19937 
    
    # word size, state size, shift size, mask bits
    w, n, m, r = (32, 624, 397, 31)
    
    # XOR mask
    a = 0x9908B0DF
    # tempering
    u, d = 11, 0xFFFFFFFF
    s, b = 7, 0x9D2C5680
    t, c = 15, 0xEFC60000
    l = 18
    # initialization multiplier
    f = 1812433253

    LOWER_MASK = (1 << r) - 1
    UPPER_MASK = ~LOWER_MASK & (1 << w) - 1

    def __init__(self, seed=None, state=None, with_negative=True):
        # to use int overflow or not
        self.with_negative = with_negative

        if seed:
            self.mt = [0] * self.n
            self.index = self.n + 1
            self.__seed_mt19937(seed)
        elif state:
            self.mt = state[:self.n]
            self.index = self.n
        else:
            raise AttributeError("seed or state wasn't passed to constructor")


    @classmethod
    def __lower_bits(cls, val, bits_num):
        """Gets lower bits_mum of val"""
        mask = (1 << bits_num) - 1
        return val & mask


    def __seed_mt19937(self, seed):
        """Initialize the generator from a seed."""
        self.index = self.n
        self.mt[0] = seed
        
        for i in range(1, self.index):
            val = self.mt[i - 1] ^ (self.mt[i - 1] >> (self.w - 2))
            
            self.mt[i] = self.__lower_bits(self.f * val + i, self.w)


    def __twist(self):
        """Generate the next n values from the series x_i."""
        for i in range(len(self.mt)):
            x = (self.mt[i] & self.UPPER_MASK) + \
                (self.mt[(i + 1) % self.n] & self.LOWER_MASK)
            
            xa = x >> 1
            if x % 2 != 0: # lowest bit of x is 1
                xa = xa ^ self.a
            
            self.mt[i] = self.mt[(i + self.m) % self.n] ^ xa

        self.index = 0


    def get_generator(self):
        """Returns generator of random numbers"""
        if self.index > self.n:
                raise("Generator wasn't seeded")
        while True:
            if self.index >= self.n:
                self.__twist()

            y = self.mt[self.index]
            y ^= (y >> self.u) & self.d
            y ^= (y << self.s) & self.b
            y ^= (y << self.t) & self.c
            y ^= y >> self.l

            self.index += 1
            
            # pseudo random number
            prn = self.__lower_bits(y, self.w)

            
            if self.with_negative:
                yield int_overflow(prn)
            else:
                yield prn


def crack(sample):
    sample = sample[:MT19937.n]
    mt_state = list()
    for num in sample:
        mt_state.append(get_state_by_number(num))

    return MT19937(state=mt_state)



def get_state_by_number(num):
    num = un_bitshift_right_xor(num, MT19937.l)
    num = un_bitshift_left_xor(num, MT19937.t, mask=MT19937.c)
    num = un_bitshift_left_xor(num, MT19937.s, mask=MT19937.b)
    num = un_bitshift_right_xor(num, MT19937.u, mask=MT19937.d)
    return num


def un_bitshift_right_xor(val, shift, int_size=32, mask=None):
    """Returns source value of operation val ^= (val >> shift) & mask"""
    max_int = 2**int_size
    full_mask = (1 << int_size) - 1 
    if mask is None:
        mask = full_mask
    part_num = 0
    result = 0
    while (part_num * shift < int_size):
        # mask for current part of number
        part_mask = ((full_mask << (int_size - shift)) % max_int) >> (shift * part_num)
        # get current part
        part = val & part_mask
        # unapply xor for next part of number
        val ^= (part >> shift) & mask
        # add part to result
        result |= part
        part_num += 1

    return result


def un_bitshift_left_xor(val, shift, int_size=32, mask=None):
    """Returns source value of operation val ^= (val << shift) & mask"""
    full_mask = (1 << int_size) - 1 
    if mask is None:
        mask = full_mask
    part_num = 0
    result = 0
    while (part_num * shift < int_size):
        # mask for current part of number
        part_mask = ((1 << shift) - 1) << (part_num * shift)
        # get current part
        part = val & part_mask
        # unapply xor for next part of number
        val ^= (part << shift) & mask
        # add part to result
        result |= part
        part_num += 1

    return result