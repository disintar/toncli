from bitstring import BitString
import math
from typing import Optional


def deserialize(data: str, cut_start: Optional[int] = None, cut_end: Optional[int] = None) -> str:
    """
    Deserialize cell (warning: it's not full deserialization, it's only for get methods thrue lite client)

    :param data: HEX data
    :param cut_start: Data bits cut start
    :param cut_end: Data bits cut end
    :return: Return BIN
    """
    _bytes = BitString(hex=data)

    # 3.1.4. Standard cell representation

    # Two descriptor bytes d1 and d2 are serialized first. Byte d1 equals
    # r+8s+32l, where 0 ≤ r ≤ 4 is the quantity of cell references contained
    # in the cell, 0 ≤ l ≤ 3 is the level of the cell, and 0 ≤ s ≤ 1 is 1 for
    # exotic cells and 0 for ordinary cells.

    d1 = int(_bytes.bytes[0])

    l = d1 // 32  # level of cell
    s = (d1 % 32) // 8  # is cell exotic
    r = ((d1 % 32) % 8)  # refs

    # _bytes[1] Byte d2 equals bb/8c+db/8e, where
    # 0 ≤ b ≤ 1023 is the quantity of data bits in c.

    b = math.ceil((_bytes.bytes[1]) / 2)  # data bits
    data = _bytes.bin[2 * 8:]  # cut d1 & d2
    data = data[:b * 8]  # up to data end

    if int(_bytes.bytes[1]) % 2 != 0:
        to_cut = 0

        for i in reversed(data):
            if int(i) == 1:
                to_cut += 1
                break
            else:
                to_cut += 1

        data = data[:-1 * to_cut]

    cell_bits_length = len(data)
    if not cut_start:
        return data
    else:
        return data[cut_start:cut_end]


if __name__ == "__main__":
    print(deserialize("015300000000000000002003bf5f88fb118ac18af94fee62930bf5ab60682b3c03d72c9a6f45f841ac7dcc04"))
