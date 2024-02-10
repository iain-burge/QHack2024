
import numpy as np
import plotext as plt

from Mult import multImproved as mult


def isneg(value: int, n_bits: int) -> bool:
    """
    Returns true if negative
    """
    # print(value)
    # print(f"\t{(value & (1<<n_bits))}")
    # return ((value%(n_bits+1)) & (1<<n_bits)) != 0
    return value < 0


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
    """
    Unitary version of double rotation CORDIC algorithm (TODO: cite the paper)
    t (int) [0,1]: input angle written in fixed point notation
    n_bits (int): number of bits used to describe t
    """
    theta_i:    int = 0
    x_i:        int = (1<<n_bits)-1
    y_i:        int = 0
    t_i:        int = t
    aux_1:      int = 0
    aux_2:      int = 0
    d:   list[bool] = [False] #Note, first index not used

    for i in range(1, n_bits):
        d.append(not(isneg(x_i, n_bits) != (y_i <= t_i)))

        if d[i]:
            x_i, y_i = y_i, x_i
        for _ in range(2):
            x_i -= y_i>>i
            y_i, aux_1, aux_2 = mult(
                y_i, aux_1, aux_2, n_bits, 2*i, modulo=False
            )
            y_i += x_i>>i

        if d[i]:
            x_i, y_i = y_i, x_i

        theta_i += 2*(-1 if d[i] else 1)*np.arctan(2**(-i))
        t_i, aux_1, aux_2 = mult(
            t_i, aux_1, aux_2, n_bits, 2*i, modulo=False
        )

    return theta_i


def main():
    n_bits  = 10

    # t       = -181
    # expected = np.arcsin(t/(2**n_bits))
    # predicted = qasinCORDIC(t, n_bits)
    # print(f"{t, n_bits=}\t({t/(2**n_bits)})")
    # print("\tExpected:   ", expected)
    # print("\tPredicted:  ", predicted)
    # print("\tDifference: ", predicted-expected)

    test = np.linspace(-(1<<n_bits), (1<<n_bits), num=128, dtype=np.int32)
    expected  = np.arcsin(test/(1<<n_bits))
    predicted = np.array([qasinCORDIC(t, n_bits) for t in test])
    plt.plot(test, expected, label="Expected", marker='hd')
    plt.plot(test, predicted, label="Predicted", marker="hd")
    plt.title("CORDIC Approx")
    plt.show()

    print(f"{np.max(np.abs(expected-predicted))   = :.6f}")
    print(f"{np.argmax(np.abs(expected-predicted))= }")
    print(f"{np.mean(np.abs(expected-predicted))  = :.6f}")
    print(f"{np.median(np.abs(expected-predicted))= :.6f}")

if __name__ == '__main__':
    main()

