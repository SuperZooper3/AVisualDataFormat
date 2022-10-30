import os


width = int(os.getenv("QR_BITS_PER_CHUNK", 5))

def chunkify(data, chunk_size):
    for i in range(0, len(data), chunk_size):
        yield data[i:i+chunk_size]


def encode(data: int):
    # Length (whole square minus corners)
    data_len = width**2 - 4

    # 1. From number to list of 0/1
    bins = list(map(int, [c for c in bin(data)[2:].zfill(data_len)]))
    # 2. 
    bins.insert(0, 1)
    bins.insert(width-1, 1)
    bins.insert(width**2 - width, 0)
    bins.insert(width**2 - 1, 0)

    chunked = list(chunkify(bins, width))
    if len(chunked) > width:
        raise ValueError("Data too large")

    # Add Rotation Bits
    _pprint(chunked)
    return [i for x in chunked for i in x]

def _pprint(data):
    for row in data:
        print("".join(map(str, row)))

if __name__ == "__main__":
    encode(12)
