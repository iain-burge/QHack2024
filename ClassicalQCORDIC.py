
import numpy as np
from Mult import mult


def isneg(value: int, n_bits: int) -> bool:
    """
    Returns true if negative
    """
    # print(value)
    # print(f"\t{(value & (1<<n_bits))}")
    # return ((value%(n_bits+1)) & (1<<n_bits)) != 0
    return value < 0

def asinCORDIC(
        t: int, n_bits: int
    ) -> int:
    """
    Unitary version of double rotation CORDIC algorithm (TODO: cite the paper)
    t (int) [0,1]: input angle written in fixed point notation
        between 0 and 1
    n_bits (int): number of bits used to describe t
    """
    theta_i = 0; x_i = (1<<(n_bits+1)); y_i = 0; t_i = t;
    aux = 0
    d = [False]

    for i in range(1, n_bits):
        d.append(isneg(x_i, n_bits) != (y_i <= t_i))

        print(f"{i=}")
        print(f"\t{theta_i=}")
        print(f"\t{isneg(x_i, n_bits)=} || {y_i=}, {t_i=} || {d[i]=}")
        print(f"\t{aux=}")

        if d[i]: #swap;
            x_i, y_i = y_i, x_i
        for _ in range(2): #Rotate twice
            x_i -= y_i>>i
            y_i, aux = mult(y_i, aux, n_bits, 2*i)
            y_i += x_i>>i
        if d[i]: #swap;
            x_i, y_i = y_i, x_i

        #Record rotation
        theta_i += (-1 if d[i] else 1)*2*np.arctan(1/(2**i))
        #Update t_i
        t_i, aux = mult(t_i, aux, n_bits, 2*i)
    
    return theta_i


def main():
    t       = 128
    n_bits  = 8

    print(f"{t, n_bits=}\t({t/(2**n_bits)})")
    print("\tExpected:  ",np.arcsin(t/(2**n_bits)))
    print("\tPredicted: ",asinCORDIC(t, n_bits))

if __name__ == '__main__':
    main()

