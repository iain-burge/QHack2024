
import numpy as np
from functools import cache

@cache
def fib(i:int) -> int: 
    return int(np.round(
        1/(5**.5) * (((1+5**.5)/2)**(i+1)-((1-5**.5)/2)**(i+1))
    ))

def mult(
        x: int, aux: int, n: int, m: int, modulo: bool = False, 
        debug: bool = False,
    ) -> tuple[int, int]:
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


def multImproved(
        x: int, aux_1: int, aux_2: int, n: int, m: int, 
        modulo: bool = False, debug: bool = False,
    ) -> tuple[int, int, int]:

    if debug:
        print(f"Init: \n\t{(x,aux_1,aux_2)=}")
   
    aux_2 += x
    x     += aux_2>>m
    aux_1 += x
    
    for i in range(int(1+2*np.ceil(np.log(n/m)/np.log((1+5**.5))))):
        if debug:
            print(f"{i=} | {x=} | {aux_1=}")
        if i%2 == 0:
            x       += ((-1)**(fib(i))) * (aux_1>>(m*fib(i)))
        else:
            aux_1   += ((-1)**(fib(i))) * (x>>(m*fib(i)))

    aux_2 -= aux_1
    
    for i in range(int(1+2*np.ceil(np.log(n/m)/np.log((1+5**.5))))-1, -1, -1):
        if debug:
            print(f"{i=} | {x=} | {aux_1=}")
        if i%2 == 0:
            x       -= ((-1)**(fib(i))) * (aux_1>>(m*fib(i)))
        else:
            aux_1   -= ((-1)**(fib(i))) * (x>>(m*fib(i)))

    aux_1 -= x

    if modulo:
        x, aux_2 = x%(1<<n), aux_2%(1<<n)
    
    if debug:
        print(f"Result: \n\t{(x,aux_1,aux_2)=}")

    return x, aux_1, aux_2


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
        print(f"in={inputs[i]} | expect={expected_outputs[i]}"
            +f" | out={outputs[i]} | err={errors[i]}")

def testMultImproved(n_bits: int = 8, n_tests: int = 16):
    ran: int = 2**n_bits
    err: int = 2**(n_bits//2)
    mr:  int = n_bits//2

    inputs = [
        (np.random.randint(ran), np.random.randint(err), 
         np.random.randint(err), np.random.randint(1,mr))
        for _ in range(n_tests)
    ]
    expected_outputs = [
        ((x+(x>>m)), aux_1, aux_2)
        for x, aux_1, aux_2, m in inputs
    ]
    outputs = [
        multImproved(x, aux_1, aux_2, n_bits, m)
        for x, aux_1, aux_2, m in inputs
    ]
    errors = [
        (outputs[i][0]-expected_outputs[i][0], 
         outputs[i][1]-expected_outputs[i][1],
         outputs[i][2]-expected_outputs[i][2])
        for i in range(len(inputs))
    ]

    for i in range(len(inputs)):
        print(f"in={inputs[i]}|expect={expected_outputs[i]}"
            +f"\n\t|out={outputs[i]}|err={errors[i]}")

def main():
    n_bits:     int = 8
    n_tests:    int = 32
    testMultImproved(n_bits, n_tests)

    # x: int = 55
    #
    # print(mult(x, 0, n_bits, 1))
    # print(multImproved(x, 0, 0, n_bits, m=1))

    
if __name__ == '__main__':
    main()

