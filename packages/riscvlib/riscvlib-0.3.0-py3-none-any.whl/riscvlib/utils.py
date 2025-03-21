
from copy import copy




ZERO_BYTES32 = b"\x00" * 32

def to_hex(value:object):
    """
    value may be int, bytes or other. Convert it to a hex string
    :param value:
    :return: hex string
    """
    bites = b''
    if isinstance(value, int): # int
        bites = value.to_bytes(length=4, byteorder='little', signed=True)
    elif isinstance(value, bytes):
        bites = copy(value)
    else:
        raise ValueError(f"Could Not convert type '{type(value)}' to hex string")

    inter = int.from_bytes(bites, byteorder='little', signed=False)
    return f"{inter:08x}"


def sign_extend_str(bit_str, target_length=32):
    """
    Sign extend bitstring
    :param bit_str: string
    :param target_length: int
    :return: string
    """
    original_length = len(bit_str)
    if original_length >= target_length:
        return bit_str  # No need to extend

    # Extract the most significant bit (MSB)
    msb = bit_str[0]

    # Repeat the MSB to fill the remaining bits
    extended_bits = msb * (target_length - original_length)
    return extended_bits + bit_str


def twos_complement_str(bit_str):
    """
    convert a bitstring -> 2's complement of bitstring
    :param bit_str: str - bitstring
    :return: str - 2's complement of input string
    """
    # if passed a leading '-', replace with a zero, it's a python format thing
    bit_str = bit_str.replace("-", "0", 1)
    bit_str = bit_str.replace('0b',"", 1)

    # Convert the bit string to an integer
    unsigned_value = int(bit_str, 2)
    bit_len = len(bit_str)

    # Calculate the 2's complement
    inverted_value = ~unsigned_value
    twos_complement_value = (inverted_value + 1) & ((1 << bit_len) - 1)

    # Convert back to a bit string
    twos_complement_string = format(twos_complement_value, f"0{bit_len}b")
    return twos_complement_string


def int_frmt(int_val, width=8, sep=":", frmt="bin", signed=False):
    """
    format an integer as a string with given type, sign, legth and seperator
    :param int_val:
    :param width:
    :param sep: string - default is ':'
    :param frmt: string - one of 'bin', 'hex'
    :param signed: bool
    :return: string - formatted string
    """
    # TODO: understand what a negative int_val means in this context
    out, val = "", ""
    byte_len = None
    if frmt == 'bin':
        byte_len = 8
        if signed:
            val = twos_complement_str(format(int_val, f'0{width}b'))
        else:
            val = format(int_val, f'0{width}b')
    elif frmt == "hex":
        byte_len = 2
        val = format(int_val, f'0{width}x')

    for i in range(0, len(val), byte_len):
        out = out + sep + val[i:i + byte_len]
    out = out[1:]
    assert len(out) == width
    return out


def bitstr2Int(bitstr, signed=True):
    """
    Convert a signed bitstring into a python integer.
    Usage: bistr2Int('10000001', signed=True) => -127
    Usage: bistr2Int('10000001', signed=False) => 129
    :param bitstr: string - the bitstring to be converted
    :param signed: bool - bitstring is signed
    :return: int
    """
    if signed:
        if bitstr[0] == '1':
            # negative
            # flip bits
            bsf = "".join(['0' if x == '1' else '1' for x in bitstr])
            # finish uncomplement and sign
            return (int(bsf, 2) + 1) * -1
        else:
            # positive
            return int(bitstr, 2)
    else:
        # unsigned
        # just use built-in
        return int(bitstr, 2)


if __name__ == "__main__":
    # test bin_format
    val = 1308
    print(int_frmt(val, width=16, sep="|", signed=False))
    print(int_frmt(val, width=8, sep=":", frmt='hex'))

    # Example usage:
    bit_string = "00010101"

    result = twos_complement_str(bit_string)
    print(f"Original bit string: {bit_string}")
    print(f"2's complement: {result}")
    print("Sign Extended result 16: ", sign_extend_str(result, 16))
    print()
    res = sign_extend_str(bit_string, 16)
    print(f"Original bit string: {bit_string}")
    print(f"Sign-extended to 16 bits: {res}")

    print()
    print("2'c (-00000010100): ", twos_complement_str('-00000010100'))

    print()
    print("Convert a signed bitstring to a signed int\n-----------------------------------------")

    comp_bitstring = "111111111000"
    print(bitstr2Int(comp_bitstring))
    print()
    print()




