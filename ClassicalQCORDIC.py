
import numpy as np
import plotext as plt

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
    n_bits (int): number of bits used to describe t
    """
    theta_i:    int = 0
    x_i:        int = (1<<(n_bits))-1
    y_i:        int = 0
    aux:        int = 0
    t_i:        int = t % (1<<(n_bits-1))
    d:   list[bool] = [t>=(1<<(n_bits-1))]

    for i in range(1, n_bits):
        d.append(isneg(x_i, n_bits) != (y_i>t_i))

        # print(f"{i=}")
        # print(f"\t{theta_i=}")
        # print(f"\t{isneg(x_i, n_bits)=} || {y_i=}, {t_i=} || {d[i]=}")
        # print(f"\t{x_i=}, {aux=}")

        # for _ in range(2): #Rotate twice
        #     if d[i]:
        #         x_i -= (y_i>>i)
        #         y_i, aux = mult(y_i, aux, n_bits, 2*i)
        #         y_i += (x_i>>i)
        #     else:
        #         y_i -= x_i>>i
        #         x_i, aux = mult(x_i, aux, n_bits, 2*i)
        #         x_i += y_i>>i

        
        for _ in range(2):
            x_i, y_i = (
                x_i-(-1 if d[i] else 1)*(y_i>>i), 
                y_i+(-1 if d[i] else 1)*(x_i>>i)
            )
        # if d[i]: #swap
        #     x_i, y_i = y_i, x_i
        # for _ in range(2): #Rotate twice
        #     y_i -= x_i>>i
        #     x_i, aux = mult(x_i, aux, n_bits, 2*i)
        #     x_i += y_i>>i
        # if d[i]: #swap;
        #     x_i, y_i = y_i, x_i

        #Record rotation
        theta_i += (-1 if d[i] else 1)*2*np.arctan(1/(2**i))
        #Update t_i
        t_i, aux = mult(t_i, aux, n_bits, 2*i)

    return theta_i

def asinCORDICClassical(t, n_bits):
    theta_i:    int = 0
    x_i:        int = (1<<n_bits)-1
    y_i:        int = 0
    t_i:        int = t
    d:    list[int] = [0]

    for i in range(1, n_bits):
        d.append(np.sign(x_i) if y_i <= t_i else -np.sign(x_i))

        for _ in range(2):
            x_i, y_i = (
                x_i - d[i]*(y_i>>i),
                y_i + d[i]*(x_i>>i),
            )

        theta_i += 2*d[i]*np.arctan(2**(-i))
        t_i     *= (1+2**(-2*i))

    return theta_i

def qasinCORDIC(t, n_bits):
    theta_i:    int = 0
    x_i:        int = (1<<n_bits)-1
    y_i:        int = 0
    t_i:        int = t
    aux:        int = 0
    d:   list[bool] = [False] #Note, first index not used

    for i in range(1, n_bits):
        d.append(not(isneg(x_i, n_bits) != (y_i <= t_i)))

        for _ in range(2):
            x_i, y_i = (
                x_i - (-1 if d[i] else 1)*(y_i>>i),
                y_i + (-1 if d[i] else 1)*(x_i>>i),
            )

        theta_i += 2*(-1 if d[i] else 1)*np.arctan(2**(-i))
        t_i, aux = mult(t_i, aux, n_bits, 2*i, modulo=False)

    return theta_i



def main():
    t       = 128
    n_bits  = 16

    # expected = np.arcsin(t/(2**n_bits))
    # predicted = asinCORDICClassical(t, n_bits)
    # print(f"{t, n_bits=}\t({t/(2**n_bits)})")
    # print("\tExpected:   ", expected)
    # print("\tPredicted:  ", predicted)
    # print("\tDifference: ", predicted-expected)

    test = np.linspace(-(1<<n_bits), (1<<n_bits), num=256, dtype=np.int32)
    expected  = np.arcsin(test/(1<<n_bits))
    predicted = np.array([qasinCORDIC(t, n_bits) for t in test])
    plt.plot(test, expected, label="Expected", marker='hd')
    plt.plot(test, predicted, label="Predicted", marker="hd")
    plt.title("CORDIC Approx")
    plt.show()

if __name__ == '__main__':
    main()

