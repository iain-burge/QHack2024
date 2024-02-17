
def bitshift(x: int, shift: int, n_bits: int):
    x = x%(2**n_bits)
    leftBit = (x&(1<<(n_bits-1)))>>(n_bits-1)

    if shift > n_bits:
        if leftBit == 0:
            return 0
        else:
            return (1<<n_bits)-1

    x  = x>>shift
    x += (((1<<shift)-leftBit)<<(n_bits-shift))%(2**n_bits)

    return x

def main():
    print(256-bitshift(-113, 4, 8))

if __name__ == '__main__':
    main()

