import os


width = int(os.getenv("QR_BITS_PER_CHUNK", 5))

def chunkify(data, chunk_size):
    for i in range(0, len(data), chunk_size):
        yield data[i:i+chunk_size]


def encode(data: int):
    data_w = width - 2

    # 1. Split data into chunks
    bins = list(map(int, bin(data)[2:].zfill(data_w**2)))
    chunked = list(chunkify(bins, data_w))
    if len(chunked) > data_w:
        raise ValueError("Data too large")

    # Add Rotation Bits
    encoded = ([[0 for _ in range(width)]]
                + list(map(lambda x: [0] + x + [0], chunked))
                + [[0 for _ in range(width)]])
    encoded[0][0] = 1
    encoded[0][-1] = 1
    _pprint(encoded)
    return [i for x in encoded for i in x]

def _pprint(data):
    for row in data:
        print("".join(map(str, row)))

if __name__ == "__main__":
    encode(12)
