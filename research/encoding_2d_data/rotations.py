import os

from typing import Iterable, List

# From https://journals.plos.org/plosone/article/file?id=10.1371/journal.pone.0136487&type=printable
# 9
# 0 is white, 1 is black
data = """
000000000
011111110
010000110
010010110
010000010
010001010
010011010
011111110
000000000
"""

# Column size for data+checksum
BITS_PER_CHUNK = int(os.getenv("QR_BITS_PER_CHUNK", 5))
# Number of bits total (minus checksums)
# rows * (cols - 2)
MAX_BIT_SIZE = (BITS_PER_CHUNK*(BITS_PER_CHUNK-2))
MAX_DATA = 2**MAX_BIT_SIZE

# Total row width is BITS_PER_CHUNK + the 2 bits on each side for the square
length = BITS_PER_CHUNK+4
size = length**2

# 0, 0 in top-left
bit_set_at_position = lambda n, x, y: n & 1 << (size-(y*length + x + 1)) != 0
bc = bit_set_at_position


def checksum(cols: List[List[int]]) -> bool:
    w = len(cols)

    # Check parity of each column
    parities = cols[3][:3]
    for idx, parity in enumerate(parities):
        if (cols[idx].count(True) % 2 == 1) != parity:
            print("[-] Parity error on column", idx)
            return False
    
    # Check parity of each section
    sec1 = cols[0][:3] + cols[1][:3] + cols[2][:3]

    if (sec1.count(True) % 2 == 1) != cols[3][3]:
        print("[-] Parity error on section 1")
        return False

    sec2 = cols[0][3:] + cols[1][3:] + cols[2][3:]
    if (sec2.count(True) % 2 == 1) != cols[3][4]:
        print("[-] Parity error on section 2")
        return False
    
    # Check checksums
    if cols[3] != cols[4][::-1]:
        print("[-] Checksum cols error")
        return False

    return True


def decode(data: int):
    columns = []
    for cnum in range(2, 7):
        columns.append([bc(data, cnum, rnum) for rnum in range(2, 7)])
    for _ in range(4):
        columns = list(zip(*columns[::-1]))
        check = checksum(columns)
        if not check:
            continue
        else:
            print("[+] Checksum passed")
            num = columns[0] + columns[1] + columns[2]
            num = int("".join(map(lambda b: "1" if b else "0", num)), base=2)
            print("[+] Number:", num)
            break

def iter_bits(n: int) -> Iterable[bool]:
    while n > 0:
        yield n & 1 == 1
        n >>= 1

def encode(data: int):
    if data > MAX_DATA:
        raise ValueError(f"Data too large, max {MAX_DATA}")

    final = data.to_bytes(length=(MAX_BIT_SIZE//8)+1, byteorder="big")
    print(bin(int(final.hex(), base=16)))
    print(list(iter_bits(data)))
    return final


def main():
    data = 18242
    print(encode(data))

    # num = int(data.replace("\n", ""), base=2)
    # decode(num)

if __name__ == "__main__":
    main()