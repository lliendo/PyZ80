""" 
    This file is part of PyZ80.

    PyZ80 is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    PyZ80 is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with PyZ80.  If not, see <http://www.gnu.org/licenses/>.

    Copyright 2010-2011 Lucas Liendo.
"""

def ones_complement_byte(byte) :
    """ Computes the ones complement of a byte (8 bits). """
    return ~byte & 0xFF

def ones_complement_word(word) :
    """ Computes the ones complement of a word (16 bits). """
    return ~byte & 0xFFFF

def twos_complement_byte(byte) :
    """ Computes the twos complement of a byte (8 bits). """
    return (~byte + 1) & 0xFF

def twos_complement_word(word) :
    """ Computes the twos complement of a word (16 bits). """
    return (~word + 1) & 0xFFFF

def test_byte_sign(byte) :
    """ Tests the most significat bit of a byte (8 bits). """
    if (byte & 0xFF) & 0x80 :
        return 1

    return 0

def test_word_sign(word) :
    """ Tests the most significat bit of a word (16 bits). """
    if (word & 0xFFFF) & 0x8000 :
        return 1

    return 0

def compute_indexed_address(ho_base_addr, lo_base_addr, d) :
    """ Computes an indexed address : base_addr + d. d is +127/-128 (displacement or offset).
    """
    if test_byte_sign(d) :
        addr = compose_word(ho_base_addr, lo_base_addr) - \
            twos_complement_byte(d)
    else :
        addr = compose_word(ho_base_addr, lo_base_addr) + d

    ho_addr, lo_addr = decompose_word(addr)

    return ho_addr, lo_addr

def compose_byte(ho_nibble, lo_nibble) :
    """ Returns the composition of two nibbles into one byte. """
    return ((ho_nibble & 0xF) << 4) + (lo_nibble & 0xF)

def compose_word(ho_byte, lo_byte) :
    """ Returns the composition of two bytes into one word. """
    return ((ho_byte & 0xFF) << 8) + (lo_byte & 0xFF)

def decompose_word(word) :
    """ Splits a word into its high and low order bytes. """
    word &= 0xFFFF 
    ho_byte = word >> 8
    lo_byte = word - (ho_byte << 8)

    return ho_byte, lo_byte

def decompose_byte(byte) :
    """ Splits a byte into its high and low order nibbles. """
    byte &= 0xFF
    ho_nibble = byte >> 4
    lo_nibble = byte - (ho_nibble << 4)

    return ho_nibble, lo_nibble

def shift_left_byte(byte, n) :
    """ Shifts a byte left n times. """
    byte &= 0xFF
    while n :
        byte <<= 1
        n -= 1

    return byte & 0xFF

def shift_right_byte(byte, n) :
    """ Shifts a byte right n times. """
    byte &= 0xFF
    while n :
        byte >>= 1
        n -= 1

    return byte & 0xFF

def rotate_right_byte(byte, n) :
    """ Rotates a byte right n times. """
    byte &= 0xFF

    while n :
        if byte & 0x1 :
            byte = (byte >> 1) + 0x80
        else :
            byte = byte >> 1

        n -= 1

    return byte

def rotate_left_byte(byte, n) :
    """ Rotates a byte left n times. """
    byte &= 0xFF

    while n :
        if byte & 0x80 :
            byte = ((byte - 0x80) << 1) + 0x1
        else :
            byte = byte << 1

        n -= 1

    return byte

def rotate_right_word(word, n) :
    """ Rotates a word right n times. """
    word &= 0xFFFF

    while n :
        if word & 0x1 :
            word = (word >> 1) + 0x8000
        else :
            word = word >> 1

        n -= 1

    return word

def rotate_left_word(word, n) :
    """ Rotates a word left n times. """
    word &= 0xFFFF

    while n :
        if word & 0x8000 :
            word = ((word - 0x8000) << 1) + 0x1
        else :
            word = word << 1

        n -= 1

    return word

def test_byte_overflow(byte) :
    if (byte > 0xFF) or (byte < 0) :
        return 1

    return 0

def test_word_overflow(word) :
    if (word > 0xFFFF) or (word < 0) :
        return 1

    return 0

def binary(n, bits_alignment=8) :
    """ Returns a string with the binary representation of n. """

    return bin(n)[2:].zfill(bits_alignment)

def dec_to_bin(x, bits_alignment=8) :
    """ Converts a decimal number to its twos complement
        representation. """

    b = binary(x)
    return x - (1 << len(b) if b[0] == '1' else 0)

def test_signed_byte_overflow(n, m, op="ADD") :
    n = dec_to_bin(n)
    m = dec_to_bin(m)

    if op == "ADD" :
        l = n + m
    else :
        l = n - m

    if (l > 0x7F) or (l < -0x80) :
        return 1

    return 0

# Replacement. Needs testing.
#def test_signed_byte_overflow(l, op="ADD") :
#    l = map(dec_to_bin, l)
#    
#    if op == "ADD" :
#        f = lambda x, y : x + y
#    elif op == "SUB" :
#        f = lambda x, y : x - y
#
#    n = reduce(f, l)
#
#    if (n > 0x7F) or (n < -0x80) :
#        return 1
#
#    return 0

def test_signed_word_overflow(n, m, op="add") :
    n = dec_to_bin(n)
    m = dec_to_bin(m)

    if op == "add" :
        l = n + m
    else :
        l = n - m

    if (l > 0x7FFF) or (l < -0x8000) :
        return 1

    return 0

# Replacement. Needs testing.
#def test_signed_word_overflow(l, op="ADD") :
#    l = map(dec_to_bin, l)
#    
#    if op == "ADD" :
#        f = lambda x, y : x + y
#    elif op == "SUB" :
#        f = lambda x, y : x - y
#
#    n = reduce(f, l)
#
#    if (n > 0x7FFF) or (n < -0x8000) :
#        return 1
#
#    return 0

def test_byte_zero(byte) :
    """ Tests if byte is zero. """

    if (byte & 0xFF) == 0 :
        return 1

    return 0

def test_word_zero(word) :
    """ Tests if word is zero. """

    if (word & 0xFFFF) == 0 :
        return 1

    return 0

def test_even(n) :
    """ Tests if n is even. """

    if (n & 0x1) :
        return 0

    return 1

def byte_parity(byte) :
    """ Returns the byte's parity. """

    byte &= 0xFF
    return test_even(bin(byte).count('1', 2))

def word_parity(word) :
    """ Returns the word's parity. """

    word &= 0xFFFF
    return test_even(bin(word).count('1', 2))

def test_carry_from_bit_n_on_add(word1, word2, n) :
    n = pow(2, n) - 1 
    if ((word1 & n) + (word2 & n)) > n :
        return 1

    return 0

def test_half_carry_on_add(byte1, byte2) :
    # Test if there is a carry from bit 3 to
    # bit 4.
    if ((byte1 & 0xF) + (byte2 & 0xF)) > 0xF :
        return 1

    return 0

def test_half_carry_on_substract(byte1, byte2) :
    # Test if there is a borrow from bit 4 to
    # bit 3.
    if (byte1 & 0xF) < (byte2 & 0xF) :
        return 1

    return 0

def test_half_carry_on_add_word(word1, word2) :
    # Test if there is a carry from bit 11 to
    # bit 12.
    if ((word1 & 0xFFF) + (word2 & 0xFFF)) > 0xFFF :
        return 1

    return 0

def test_half_carry_on_substract_word(word1, word2) :
    # Test if there is a borrow from bit 12 to
    # bit 11.
    if (word1 & 0xFF) < (word2 & 0xFF) :
        return 1

    return 0

def sub_bytes(*bytes) :
    bytes = list(bytes)
    bytes.reverse()
    n = bytes.pop()
    return n + sum(map(twos_complement_byte, bytes)) & 0xFF

def sub_words(*words) :
    words = list(words)
    words.reverse()
    n = words.pop()
    return n + sum(map(twos_complement_word, words)) & 0xFFFF
