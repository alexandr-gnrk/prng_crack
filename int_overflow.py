
def int_overflow(val):
    return (val + 2**31) % 2**32 - 2**31