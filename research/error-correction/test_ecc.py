import random
import hamming


def test_hamming_random_no_changes(tests=1000):
    for i in range(tests):
        size = random.randint(1, 2**10)
        payload = [random.randint(0, 1) for _ in range(size)]
        data = hamming.hamming_encode(payload)
        assert hamming.hamming_decode(data) == payload


def test_hamming_random_one_change(tests=1000):
    for i in range(tests):
        size = random.randint(1, 2**10)
        payload = [random.randint(0, 1) for _ in range(size)]
        data = hamming.hamming_encode(payload)

        # Flip a random bit
        n = random.randint(0, len(data)-1)
        data[n] = 0 if data[n] == 1 else 1

        assert hamming.hamming_decode(data) == payload

def test_hamming_random_two_changes(tests=1000):
    for i in range(tests):
        size = random.randint(1, 2**10)
        payload = [random.randint(0, 1) for _ in range(size)]
        data = hamming.hamming_encode(payload)

        # Flip two random bits
        n1 = random.randint(0, len(data)-1)
        data[n1] = 0 if data[n1] == 1 else 1

        n2 = random.randint(0, len(data)-1)
        while n2 == n1: # make sure its a different one
            n2 = random.randint(0, len(data)-1)

        data[n2] = 0 if data[n2] == 1 else 1

        # except an error
        try:
            hamming.hamming_decode(data)
            assert False
        except ValueError:
            pass

