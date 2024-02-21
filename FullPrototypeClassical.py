
import numpy as np
from functools import cache

try:
    import matplotlib.pyplot as plt
except ImportError:
    import plotext as plt

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


def mult(
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
    x += bitshift(aux_2, m, n)
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


def isneg(value: int, n_bits: int) -> bool:
    '''
    Returns true if the value is negative in two's complement

    value  (int): The value being assessed
    n_bits (int): Number of bits    

    return (bool): True if value is negative
    '''
    return (value & (1<<(n_bits-1))) != 0


def qasinModuloCORDIC(t: int, n_bits: int) -> float:
    '''
    Unitary version of double rotation CORDIC algorithm (TODO: cite the paper)

    Main source (for classical implementation):
        Computing Functions cos^-1 and sin^-1 Using Cordic
        IEEE Transactions on Computers, VOL. 42, NO. 1, January 1993
        Christophe Mazenc, Xavier Merrheim, and Jean-Michel Muller
    Note: the paper's algorithm seemed to have a bug, but I fixed it for this.

    Returns theta_i which approximates arcsin(t/(2^n_bits))

    t (int) [-(1<<n_bits),1<<n_bits]: Input angle written in 
        fixed point notation two's complement
    n_bits (int): Number of bits used to describe t

    return (float): theta_{n_bits+2}
    '''
    n:          int = n_bits+2
    theta_i:    int = 0
    x_i:        int = (1<<n_bits)-1
    y_i:        int = 0
    t_i:        int = t
    aux_1:      int = 0
    aux_2:      int = 0
    d:   list[bool] = []

    for i in range(1, n):
        #Note: The original paper's equation for d introduced some
        #      errors. This new equation seems to have fixed the issue
        d.append(
            isneg(x_i, n) != (isneg(t_i - (0 if isneg(x_i, n) else y_i), n))
        )

        if d[-1]:
            x_i, y_i = y_i, x_i
        for _ in range(2):
            x_i, y_i = add(x_i, y_i, i, n=n, negativeY=True)
            y_i, aux_1, aux_2 = mult(
                y_i, aux_1, aux_2, n, 2*i
            )
            y_i, x_i = add(y_i, x_i, i, n=n, negativeY=False)
        if d[-1]:
            x_i, y_i = y_i, x_i

        theta_i += 2*(-1 if d[-1] else 1)*np.arctan(2**(-i))
        t_i, aux_1, aux_2 = mult(
            t_i, aux_1, aux_2, n, 2*i
        )

    return theta_i


def main():
    n_bits    = 10
    test      = np.linspace(-(1<<n_bits), (1<<n_bits), num=2048, dtype=np.int32)
    expected  = np.arcsin(test/(2**n_bits))
    predicted = np.array([qasinModuloCORDIC(t, n_bits) for t in test])

    plt.plot(test, expected,  label="Expected")
    plt.plot(test, predicted, label="Predicted")
    plt.title("CORDIC Approx")
    plt.show()

    print(f"{np.max(np.abs(expected-predicted))          = :.6f}")
    print(f"{test[np.argmax(np.abs(expected-predicted))] = }")
    print(f"{np.mean(np.abs(expected-predicted))         = :.6f}")
    print(f"{np.median(np.abs(expected-predicted))       = :.6f}")


if __name__ == "__main__":
    main()

