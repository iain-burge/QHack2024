
import numpy as np
from ModuloBitShift import bitshift


def binary(x: int, n: int = 8) -> str:
    '''
    Prints n bit binary int x.
    Note: if x>=2**n, function prints out more bits

    x (int): integer to be printed
    n (int): number of bits
    '''
    return f"{x:>0{n}b}"


def add(
        x: int, y: int, shift: int, n: int = 8, 
        negativeY: bool = False, debug: bool = False
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

    if debug:
        print(f"Step 1: {binary((y%(N))>>shift, n)}")
        print(f"Step 2: {binary((((1<<(shift))-leftBit(y))<<(n-shift))%N, n)}")
        print(f"Total : {binary((((y%(N))>>shift)+(((1<<(shift))-leftBit(y))<<(n-shift)))%N, n)} \t{((y%(N))>>shift)+(((1<<(shift))-leftBit(y))<<(n-shift))} \t(shifted y)")
        print(f"      + {binary(x, n)} \t{x} \t(x)")
        print(f"      = {binary(x+(y//(2**shift))%(N), n)} \t{(x+(y//(2**shift))%(N//2))} \t(new x)")
        print(f"{binary((y//(2**shift))%N, n)=}, {(y//(2**shift))%N}")

    # if negativeY:
    #     y = (~y+1)%N
    # x += bitshift(y, shift, n)
    # if negativeY:
    #     y = (~y+1)%N

    if negativeY:
        x -= bitshift(y, shift, n)
    else:
        x += bitshift(y, shift, n)

    return x%N, y%N


def main():
    '''
    Tests out the add function.
    '''
    n = 8

    for i in range(4):
        (x, y, shift, negY) = (
            np.random.randint(2**n),
            np.random.randint(2**n),
            np.random.randint(n),
            np.random.randint(2) == 1
        )

        x_signed = x if x&(1<<(n-1))==0 else x-(1<<n)
        y_signed = y if y&(1<<(n-1))==0 else y-(1<<n)

        output = add(x,y,shift,n,negY)[0]
        output_signed = output if output&(1<<(n-1))==0 else output-(1<<n)

        print(
            f"{i=}\n\t{x=} | {y=} | {shift=} | {negY=}"
            f"\n\t{binary(x)=} | {binary(y)=}"
            +f"\n\t{x_signed=} | {y_signed=} | "
            +f"x+y>>shift={x_signed+(y_signed//(2**shift))}"
            +f"\n\t{binary(add(x,y,shift,n,negY)[0])  =}"
            +f" ({output_signed})"
            # +f"\n\t{binary((x+(y//(2**shift)))%(2**n)) =}\n"
        )


if __name__ == "__main__":
    main()

