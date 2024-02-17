
import numpy as np
import plotext as plt

from Mult import multImproved as mult
from ShiftAdd import add


def isneg(value: int, n_bits: int, modulo: bool = False) -> bool:
    """
    Returns true if negative
    """
    if modulo:
        return (value & (1<<(n_bits-1))) != 0
    return value < 0


def asinCORDICClassical(t, n_bits):
    theta_i:    int = 0
    x_i:        int = (1<<n_bits)-1
    y_i:        int = 0
    t_i:        int = t
    d:    list[int] = [0]

    # tempX = []; tempY = []
    for i in range(1, n_bits):
        # tempX.append(x_i); tempY.append(y_i)
        d.append(np.sign(x_i) if y_i < t_i else -np.sign(x_i))

        for _ in range(2):
            x_i, y_i = (
                x_i - d[i]*(y_i>>i),
                y_i + d[i]*(x_i>>i),
            )

        theta_i += 2*d[i]*np.arctan(2**(-i))
        t_i     *= (1+2**(-2*i))

    # # plt.scatter(tempX, label="x", marker='hd')
    # # plt.scatter(tempY, label="y", marker="hd")
    # plt.scatter([(1<<(n_bits-1)) if s else 0 for s in d], label="d", marker="hd")
    # plt.title("Classical")
    # plt.show()

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

    # tempX = []; tempY = []
    for i in range(1, n_bits):
        # tempX.append(x_i); tempY.append(y_i)
        d.append(not(isneg(x_i, n_bits, False) != (y_i < t_i)))

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

    # # plt.scatter(tempX, label="x", marker='hd')
    # # plt.scatter(tempY, label="y", marker="hd")
    # plt.scatter([(1<<(n_bits-1)) if s else 0 for s in d], label="d", marker="hd")
    # plt.title("Non-Modulo")
    # plt.show()

    return theta_i


def qasinModuloCORDIC(t, n_bits):
    """
    Unitary version of double rotation CORDIC algorithm (TODO: cite the paper)
    t (int) [0,1]: input angle written in fixed point notation
    n_bits (int): number of bits used to describe t
    """
    n:          int = n_bits + 2
    theta_i:    int = 0
    x_i:        int = (1<<n_bits)-1
    y_i:        int = 0
    t_i:        int = t
    aux_1:      int = 0
    aux_2:      int = 0
    d:   list[bool] = [False] #Note, first index not used

    # tempX = []; tempY = []
    for i in range(1, n_bits):
        # tempX.append(x_i); tempY.append(y_i)
        d.append(not(isneg(x_i, n, modulo=True) != (y_i < t_i)))

        if d[i]:
            x_i, y_i = y_i, x_i
        for _ in range(2):
            x_i, y_i = add(x_i, y_i, i, n=n, negativeY=True)
            y_i, aux_1, aux_2 = mult(
                y_i, aux_1, aux_2, n, 2*i, modulo=True
            )
            y_i, x_i = add(y_i, x_i, i, n=n, negativeY=False)

        if d[i]:
            x_i, y_i = y_i, x_i

        theta_i += 2*(-1 if d[i] else 1)*np.arctan(2**(-i))
        t_i, aux_1, aux_2 = mult(
            t_i, aux_1, aux_2, n, 2*i, modulo=True
        )

    # # plt.scatter(tempX, label="x", marker='hd')
    # # plt.scatter(tempY, label="y", marker="hd")
    # plt.scatter([(1<<(n-1)) if s else 0 for s in d], label="d", marker="hd")
    # plt.title("Modulo")
    # plt.show()

    return theta_i

def main():
    n_bits  = 8
    t       = 252

    expected  = np.arcsin(t/(2**n_bits))
    predicted = qasinModuloCORDIC(t, n_bits)
    print(f"{t, n_bits=}\t({t/(2**n_bits)})")
    print("\tExpected:   ", expected)
    print("\tPredicted:  ", predicted)
    print("\tDifference: ", predicted-expected)

    test = np.linspace(0, (1<<n_bits), num=256, dtype=np.int32)
    expected = np.arcsin(test/(2**n_bits))
    predicted = np.array([qasinModuloCORDIC(t, n_bits) for t in test])
    plt.scatter(test, expected, label="Expected", marker='hd')
    plt.scatter(test, predicted, label="Predicted", marker="hd")
    plt.title("CORDIC Approx")
    plt.show()

    print(f"{np.max(np.abs(expected-predicted))   = :.6f}")
    print(f"{np.argmax(np.abs(expected-predicted))= }")
    print(f"{np.mean(np.abs(expected-predicted))  = :.6f}")
    print(f"{np.median(np.abs(expected-predicted))= :.6f}")

if __name__ == '__main__':
    main()

