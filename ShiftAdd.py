
import numpy as np

def binary(x: int, n: int = 8) -> str:
    '''
    Prints n bit binary int x.
    Note: if x>=2**n, function prints out more bits

    x (int): integer to be printed
    n (int): number of bits
    '''
    return f"{x:>0{n}b}"

def add(
        x: int, y: int, shift: int, n: int = 8, debug: bool = False
    ) -> tuple[int, int]:
    '''
    Bitshifts y in two's complement and adds result to x.
    Should be unitary.
    Note: when bitshifting right, copies most significant bit left.
    
    x       (int): Number to be added to
    y       (int): Number adding into x
    shift   (int): Bitshift applied to y before addition
    n       (int): Number of bits
    debug  (bool): Prints some extra stuff when set to True
    '''

    N = 2**n
    x%=N; y%=N;

    leftBit = lambda z: (z&(1<<(n-1)))>>(n-1)

    if debug:
        print(f"Step 1: {binary((y%(N))>>shift, n)}")
        print(f"Step 2: {binary((((1<<(shift))-leftBit(y))<<(n-shift))%N, n)}")
        print(f"Total : {binary((((y%(N))>>shift)+(((1<<(shift))-leftBit(y))<<(n-shift)))%N, n)} \t{((y%(N))>>shift)+(((1<<(shift))-leftBit(y))<<(n-shift))} \t(shifted y)")
        print(f"      + {binary(x, n)} \t{x} \t(x)")
        print(f"      = {binary(x+(y//(2**shift))%(N), n)} \t{(x+(y//(2**shift))%(N//2))} \t(new x)")
        print(f"{binary((y//(2**shift))%N, n)=}, {(y//(2**shift))%N}")

    x += (y%N)>>shift
    x += (((1<<shift)-leftBit(y))<<(n-shift))%N

    return x%N, y%N

def main():
    '''
    Tests out the add function.
    '''
    n = 8

    for i in range(4):
        (x, y, shift) = (
            np.random.randint(2**n),
            np.random.randint(2**n),
            np.random.randint(n)
        )

        print(
            f"{i=}\n\t{binary(x)=} | {binary(y)=} | {shift=} "
            +f"\n\t{binary(add(x,y,shift,n,False)[0])  =}"
            # +f"\n\t{binary((x+(y//(2**shift)))%(2**n)) =}\n"
        )

if __name__ == "__main__":
    main()

