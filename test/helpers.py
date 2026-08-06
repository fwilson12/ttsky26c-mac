"""
Simple helper functions that instantiate randomized test vectors and calculates their dot products 
to test the chip against. 

If you couldn't tell by their names, dotProd() calculates and returns the dot product of two vectors (list[int])
and randomVecs() initializes two randomized vectors whose values fall within the range of the signed int8s that the
chip is designed to process.
"""

import random 
from cocotb.types import LogicArray


def dotProd(vec1: list[int], vec2: list[int]) -> int:
    """
    Calculates and returns the dot product of two vectors

    args:
        vec1: list[int] | first vector, maybe the weight vector for a single neuron in the nth layer
        vec2: list[int] | second vector, maybe the activation vector for the neuron layer n - 1  
    
    returns:
        their dot product 
    """
    assert len(vec1) == len(vec2), f"vectors must be the same size | vec1: {len(vec1)}, vec2: {len(vec2)}"

    return sum(a * b for a, b in zip(vec1, vec2))
    



def randomVecs():
    """ 
    Initializes and returns two vectors (list[int]) with random integer values within 
    the valid signed int8 range

    returns:
        v1, v2: list[int] | two vectors initialized with 5-511 dimensions 
    """
    listlen = random.randint(5, 511)

    v1 = []
    v2 = []
    for _ in range(listlen):
        v1.append(random.randint(-128, 127))
        v2.append(random.randint(-128, 127))

    return v1, v2
        

def merge(hi16: int, lo16: int, name: str) -> int:
    """
    Takes two two-byte numbers that are the high two-bytes and low two-bytes of a 
    three-byte value, and merges them via their shared (middle) byte.

    Name identifies the current test run calling the helper (random vectors, max value, etc.)
    """

    # ensure the low byte of the high 16 bits == the high byte of the low 16 bits. inequality means the FSM phase is bugged 
    assert (hi16 & 0xFF) == (lo16 >> 8), f"phase out of sync during test {name}: hi16={hi16:#06x} lo16={lo16:#06x}" 

    # truncate to only the top byte then shift it back up to its 24 bit positioning, then OR it with the low two bytes 
    # this merges the hi and lo 16bit inputs, which share their lo and hi bytes, respectively
    unsignedMerged = ((hi16 >> 8) << 16) | lo16 

    return LogicArray.from_unsigned(unsignedMerged, 24).to_signed() # unsigned int -> log array -> signed int 
    



