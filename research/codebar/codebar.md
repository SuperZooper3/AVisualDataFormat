# Research - Codebar

The goal of this research is to get used to the workings of a very basic standard encoder/ decoder system, very much inspired by the original [codebar](https://en.wikipedia.org/wiki/Codabar).

## The Specification

(For this specification, 1 indicates a black bar, and 0 indicates a white bar)

The specification is very simple, and is as follows:

- All barcodes start with a start and end string of 101
- Data is encoded as raw binary of any type
- Bars must have a consistent width, within a tolerance of 20%

### Improvement thoughts

- Start is 1011 and end is 0101(no backwards readings)
- Have 2 bits after the checksum that indicate the data type(0 is extended ascii, 1 is UTF-8, 2 is a straight-up integer(positive), 3 is TBD(maybe negative integer but why tf would you need that in a barcode))
- For the next part, we define data bits as all bits that aren't the start or end 4 or the checksum bits. Right after the start 1011 bits, we have n checksum bits that are equal to the amount of 1s in the data bits mod 2**n. n is equal the log2 of the amount of data bits, rounded up to the integer

## The Code

The code is broken into 4 parts:

- Encoder
  - Turn any data into a binary array for printing
- Decoder
  - Reverse the encoder to get the string back out of the binary array
- Printer
  - Turns the data into a valid barcode
- Reader
  - Decodes a barcode into it's raw data

## Improvements

Currently the encoder and decoder are made to be able to take in any data and turn them into binary for printers or readers.

The reader can have it's resilience improved in a couple ways:

1. Accept whitespace before or after a valid barcode
   1. This could require informing the reader about the length of the barcode by adding a `length` block to the barcode spec
2. Reduce false positives
   1. This could be done by adding a checksum to the barcode spec
3. Read a code in a real picture
   1. Requires less naively reading the image data, and looking more for black and white instead of just the closest value
4. Handle rotated barcodes
   1. This should be done by scanning each image multiple times with different scan angles
   2. **Must ensure that there are no backwards readings**. Potentially done by making the start and end strings different and non-symmetrical

## Technical TODOs

- [X] Make the reader able to deal with whitespace before
- [ ] Deal with whitespace after the barcode
- [ ] Make the reader scan down an image instead of just assuming the barcode is at the top
- [ ] Add tolerance calculation to bar counts in regions (scanner)
