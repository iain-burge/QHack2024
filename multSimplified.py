
import numpy as np
from functools import cache

@cache
def fib(i:int) -> int: 
    '''
    Fibonacci numbers { 1,1,3,5,8,13, ... }

    i (int): Index of Fibonacci number

    return (int): i^th Fibonacci number
    '''
    return int(np.round(
        1/(5**.5) * (((1+5**.5)/2)**(i+1)-((1-5**.5)/2)**(i+1))
    ))

def bitshift(x: int, shift: int, n_bits: int) -> int:
    '''
    Does right bitshifting in two's complement.
    Note: The leftmost bit is copied leftwards, i.e., 1010>>1 == 1101.

    x      (int): Value to be bitshifted.
    shift  (int): How far the value is shifted right, shift is non-negative.
    n_bits (int): Number of bits representing x.

    return (int): Right bitshifted x.
    '''
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

def add(
        x: int, y: int, shift: int, n: int = 8, negativeY: bool = False
    ) -> tuple[int, int]:
    '''
    Bitshifts y in two's complement and adds result to x.
    Should be unitary.
    Note: when bitshifting right, copies most significant bit left.
    
    x          (int): Number to be added to
    y          (int): Number adding into x
    shift      (int): Bitshift applied to y before addition
    n          (int): Number of bits
    negativeY (bool): Subtracts y if true
    '''
    N = 2**n
    x%=N; y%=N;

    if negativeY:
        x -= bitshift(y, shift, n)
    else:
        x += bitshift(y, shift, n)

    return x%N, y%N


def originalMult(
        x: int, aux_1: int, aux_2: int, n: int, m: int, 
    ) -> tuple[int, int, int]:
    '''
    In place multiplication integer by 1+2^(-m) with some error depending on 
    how clean the auxiliary registers are.
    Note: the aux_2 register can gain some error

    x     (int): Value being multiplied
    aux_1 (int): First auxiliary register, used to help clean aux_2
    aux_2 (int): Second auxiliary register, stores a copy of x
    n     (int): Number of bits representing x
    m     (int): x is multiplied by 1+2^(-m)

    return (tuple[int, int, int]):
        newX (int): the new value for x
        newAux_1 (int): New value for aux_1, should equal to init value
        newAux_2 (int): New value for aux_2, can be dirtied
    '''

    aux_2, x = add(aux_2, x, 0, n=n)
    x, aux_2 = add(x, aux_2, m, n=n)
    aux_1, x = add(aux_1, x, 0, n=n)
    
    for i in range(int(1+2*np.ceil(np.log(n/m)/np.log((1+5**.5))))):
        if i%2 == 0:
            x, aux_1 = add(x, aux_1, m*fib(i), n, negativeY=(fib(i)%2==1))
        else:
            aux_1, x = add(aux_1, x, m*fib(i), n, negativeY=(fib(i)%2==1))

    aux_2, aux_1 = add(aux_2, aux_1, 0, n=n, negativeY=True)
    
    for i in range(int(1+2*np.ceil(np.log(n/m)/np.log((1+5**.5))))-1, -1, -1):
        if i%2 == 0:
            x, aux_1 = add(x, aux_1, m*fib(i), n, negativeY=not (fib(i)%2==1))
        else:
            aux_1, x = add(aux_1, x, m*fib(i), n, negativeY=not (fib(i)%2==1))

    aux_1, x = add(aux_1, x, 0, n, negativeY=True)

    return x, aux_1, aux_2


def mult(
        x: int, aux_1: int, n: int, m: int, 
    ) -> tuple[int, int]:
    '''
    In place multiplication integer by 1+2^(-m) with some error depending on 
    how clean the auxiliary registers are.
    Note: the aux_2 register can gain some error

    x     (int): Value being multiplied
    aux_1 (int): First auxiliary register, used to help clean aux_2
    aux_2 (int): Second auxiliary register, stores a copy of x
    n     (int): Number of bits representing x
    m     (int): x is multiplied by 1+2^(-m)

    return (tuple[int, int, int]):
        newX (int): the new value for x
        newAux_1 (int): New value for aux_1, should equal to init value
        newAux_2 (int): New value for aux_2, can be dirtied
    '''

    aux_1, x = add(aux_1, x, 0, n=n)
    
    for i in range(int(1+2*np.ceil(np.log(n/m)/np.log((1+5**.5))))-1, -1, -1):
        if i%2 == 0:
            x, aux_1 = add(x, aux_1, m*fib(i), n, negativeY=not (fib(i)%2==1))
        else:
            aux_1, x = add(aux_1, x, m*fib(i), n, negativeY=not (fib(i)%2==1))

    aux_1, x = add(aux_1, x, 0, n, negativeY=True)

    return x, aux_1

def main():
    print(f"{originalMult(34, 0, 0, 10, 2)}")
    print(f"{mult(34, 0, 10, 2)}")

if __name__ == "__main__":
    main()

