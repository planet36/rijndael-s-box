#!/usr/bin/env python3
# SPDX-FileCopyrightText: Terry Jackson
# SPDX-FileCopyrightText: Steven Ward
# SPDX-License-Identifier: OSL-3.0

# pylint: disable=invalid-name
# pylint: disable=missing-function-docstring

'''The Rijndael S-Box'''

# x and y are nonnegative integers
# Their associated binary polynomials are multiplied.
# The associated integer to this product is returned.
def multiply_ints_as_polynomials(x: int, y: int) -> int:
    z = 0
    while x != 0:
        if x & 1 == 1:
            z ^= y
        y <<= 1
        x >>= 1
    return z


# x is a nonnegative integer
# m is a positive integer
def mod_int_as_polynomial(x: int, m: int) -> int:
    m_bit_len = m.bit_length()
    while (d := x.bit_length() - m_bit_len) >= 0:
        x ^= m << d
    return x


# x,y are 8-bits
# The output value is 8-bits
def rijndael_multiplication(x: int, y: int) -> int:
    z = multiply_ints_as_polynomials(x, y)
    m = 0b100011011 # 0x11b
    return mod_int_as_polynomial(z, m)


# x is 8-bits
# The output value is 8-bits
# Here we find the inverse just through a brute force search.
def rijndael_inverse(x: int) -> int:
    for y in range(1, 256):
        if rijndael_multiplication(x, y) == 1:
            return y
    # No multiplicative inverse
    return 0


# x, y are nonnegative integers
# considered as vectors of bits
def dot_product(x: int, y: int) -> int:
    return (x & y).bit_count() % 2


# A is a 64-bit integer that represents a
# 8 by 8 matrix of 0's and 1's
# x and b are 8-bit integers, considered as column vectors
# This function calculates A * x + b
def affine_transformation(A: int, x: int, b: int) -> int:
    y = 0
    for i in range(8):
        row = (A >> 8 * i) & 0xff
        bit = dot_product(row, x)
        y ^= (bit << i)
    return y ^ b


# The input value x and the output value
# of the function are both 8-bit integers
def rijndael_sbox(x: int) -> int:
    x_inv = rijndael_inverse(x)
    A = 0b11111000_01111100_00111110_00011111_10001111_11000111_11100011_11110001
    b = 0b01100011 # 0x63
    y = affine_transformation(A, x_inv, b)
    return y


# Print the Rijndael S-Box as a table of 16 rows,
# with 16 values per row (total of 256 values)
def print_rijndael_sbox():
    for x in range(0, 256):
        s = rijndael_sbox(x)
        print(f'{s:02x}', end=' ')
        if x % 16 == 15:
            print()


print_rijndael_sbox()


print()


# The input value x and the output value
# of the function are both 8-bit integers
def rijndael_inv_sbox(x: int) -> int:
    A = 0b01010010_00101001_10010100_01001010_00100101_10010010_01001001_10100100
    b = 0b00000101 # 0x05
    y = affine_transformation(A, x, b)
    y_inv = rijndael_inverse(y)
    return y_inv


# Print the Rijndael Inverse S-Box as a table of 16 rows,
# with 16 values per row (total of 256 values)
def print_rijndael_inv_sbox():
    for x in range(0, 256):
        s = rijndael_inv_sbox(x)
        print(f'{s:02x}', end=' ')
        if x % 16 == 15:
            print()


print_rijndael_inv_sbox()
