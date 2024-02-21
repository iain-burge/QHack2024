
import numpy as np
import bitstring as bs
from bitstring import BitArray

def binaryToStr(x: int, n: int = 8) -> str:
    '''
    Prints n bit binary int x.
    Note: if x>=2**n, function prints out more bits

    x (int): integer to be printed
    n (int): number of bits
    '''
    return f"{x:>0{n}b}"

def shiftAdd(
        x: int, y: int, c: int, shift: int, n: int = 8
    ) -> tuple[int, int, int]:
    """
    Adds rightshifted y to x
    """
    x_b = BitArray(int=x, length=n)
    y_b = BitArray(int=y, length=n)
    c_b = BitArray(int=c, length=n)

    print(f"in:  {x_b.bin=}, {y_b.bin=}, {c_b.bin=}")

    c_b.set(c_b[-1] ^ (x_b[-1] and y_b[-1]),  -1)
    x_b.set(x_b[-1] ^ y_b[-1], -1)

    for i in range(1, n):
        # x_b.set(x_b[-1-i] ^ c_b[-i], -1-i)
        c_b.set(
            (c_b[-i] and y_b[-1-i])
            or (c_b[-i] and x_b[-1-i])
            or (y_b[-1-i] and x_b[-1-i]),
            -1-i
        )
        x_b.set((x_b[-1-i] ^ y_b[-1-i]) ^ c_b[-i], -1-i)
        # print(f"{x_b[-1-i]=}  {y_b[-1-i]=}  {c_b[-i]=}")


    print(f"out: {x_b.bin=}, {y_b.bin=}, {c_b.bin=}")
    # print(x_b.int)

    return x_b.int, y_b.int, c_b.int

def main():
    num_bits  = 5
    num_tests = 4

    print(f"{num_bits=}")

    for i in range(num_tests):
        print(f"{i=}")

        x_in  = np.random.randint(-1<<num_bits, 1<<num_bits)//2
        y_in  = np.random.randint(-1<<num_bits, 1<<num_bits)//2
        c_in  = 0
        shift = 0

        x_out, y_out, c_out = shiftAdd(
            x=x_in, y=y_in, c=c_in, shift=shift, n=num_bits
        )

        expected = int(x_in+y_in/(2**shift))
        signed_expected = expected \
            - ((1<<num_bits) if expected > (1<<(num_bits-1)) else 0)

        print(f"\t|Expected = {signed_expected}\t|Result = {x_out}")
        print(f"\t|{x_in =}\t|{y_in =}\t|{c_in =}\t|{shift=}")
        print(f"\t|{x_out=}\t|{y_out=}\t|{c_out=}")

if __name__ == "__main__":
    main()

