
import numpy as np

def mult(
        x: int, aux: int, n: int, m: int, modulo: bool = True, 
        debug: bool = False,
    ):
    """
        x   (int): input value
        aux (int): auxiliary register
        n   (int): register size
        m   (int): shift

        Let x and aux be two n bit integers
        This function takes x and approximates (1+2^m)x while minimizing
        error caused to aux.
        This function is most accurate when aux is closer to 0.
    """
    aux += x
    x   += aux>>m

    if debug:
        print(f"{(x,aux)=}")
    for i in range(int(np.ceil(n/m))):
        if debug:
            print(f"{aux} {'-' if i%2==1 else '+'} {x>>(m*i)}")
        aux -= ((-1)**(i)) * (x>>(m*i))
        
    if modulo:
        x, aux = x%(1<<n), aux%(1<<n)

    return x, aux


def testMult(n_bits: int = 8, n_tests: int = 16):
    ran: int = 2**n_bits
    err: int = 2**(n_bits//2)
    mr:  int = n_bits//2

    inputs = [
        (np.random.randint(ran), np.random.randint(err), 
         np.random.randint(1,mr))
        for _ in range(n_tests)
    ]
    expected_outputs = [
        ((x+(x>>m))%(1<<n_bits), aux)
        for x, aux, m in inputs
    ]
    outputs = [
        mult(x, aux, n_bits, m)
        for x, aux, m in inputs
    ]
    errors = [
        (outputs[i][0]-expected_outputs[i][0], 
         outputs[i][1]-expected_outputs[i][1])
        for i in range(len(inputs))
    ]

    for i in range(len(inputs)):
        print(f"{inputs[i]=}\t{expected_outputs[i]=}"
            +f"\t{outputs[i]=}\t{errors[i]=}")


def main():
    n_bits:     int = 8
    n_tests:    int = 32
    testMult(n_bits, n_tests)
    
if __name__ == '__main__':
    main()

