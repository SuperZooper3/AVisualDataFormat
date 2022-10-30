# CEETag

*BEETag but better*

## Lessons learnt

This format of encoding is useful for small amounts of data, but becomes quite
cumbersome for larger amounts of data. The main issue is that with larger
square sizes, the checksum can no longer be used to detect errors and becomes
less useful. The enconding also doesn't include any error correction.

## Cool Stuff

### Rotation

Rotation of tags is handled by the encoder, which will assure that the code is
valid in only one rotation and that codes will have a hamming distance of 3 [[1]](https://en.wikipedia.org/wiki/Hamming_distance), so being resistant to minor errors.
