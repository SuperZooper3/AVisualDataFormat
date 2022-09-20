# Research - Codebar

The goal of this research is to get used to the workings of a very basic standard encoder/ decoder system, very much inspired by the original [codebar](https://en.wikipedia.org/wiki/Codabar).

## The Specification

(For this specification, 1 indicates a black bar, and 0 indicates a white bar)

The specification is as follows:

### Data Layout

- 4 bits of "start region": 1011
- 2 bits of "data type" :
  - 00: numeric
  - 01: ascii
  - 10: utf-8
  - 11: raw binary
- 8 bits of "data length" , encoding a number `n` the length of the data chunks in bytes (big endian)
- log2(n) bits of "checksum data"
  - the checksum data is equal to the number of 1s in the data chunks % 2^log2(n)
- n bytes of "payload data"
- 4 bits of "end region": 0101
  - This is so to easily identify reversed codes, as they should always start with 1011

Total size of barcode: 18 + 8n + log2(n) bits, n being the number of bytes in the payload

### Printer / Reader Expectations

- Bars must have a consistent width, within a tolerance of 20%

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
