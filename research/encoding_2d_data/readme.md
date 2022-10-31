# CEETag

*BEETag but better*

## Encoding 2D data

The data is encoded as a 1D list of binary 0s and 1s. It assumes that the data
will be encoded in a square grid, left to right, top to bottom. The data will be
zero-padded on the left.  
To ensure that the data can be decoded correctly, the top left and top right
corners will be set to 1 and hold no data.  
The data is encoder takes in an integer which it will convert to binary.

## Decoding 2D data

The decoder will take in a 2D array of 0s and 1s and returns an integer. The
decoder starts of by rotating the array until the top corners are 1. It then
removes the corners and converts the remaining binary to an integer.
