# Research - Codebar

The goal of this research is to get used to the workings of a very basic standard encoder/ decoder system, very much inspired by the original [codebar](https://en.wikipedia.org/wiki/Codabar).

## Lessons Learned

Since this was a research project, the main goal was to build skills and knowledge on how basic visual data encoding works. The following are the main lessons learned:

- Filters are crucial to get right if we want to be able to analyze images correctly
  - But basic filtering isn't enough, smoothing and other mathematical operations are needed to get the best results
- Processing data in a more global way is better than naively processing local data
  - Ex: to reduce errors, it would be better to scan chunks of rows at once rather than just single pixel slices
- Strict data layouts make implementation easier
  - The handoff is that there can be a lot of wasted data
- Checksums / error correction codes need to have very large redundancy to be effective
  - In our scenario, checksums were simple enough than many random images had "valid" barcodes
- Rotating an image to scan it multiple times is computationally expensive
- Writing tests is cool
- Documentation is kinda cool
- Ignoring files that cause merge conflicts is kinda cool too

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
- 8 bits of "data length", encoding a number `n` the length of the data chunks in bytes (big endian)
- floor(log2(n))+1 bits of "checksum data" (stored in big endian)
  - the checksum data is equal to (the sum of (every integer from 1 to 8n raised to the power of the bit at that position(1 being the leftmost bit))) % 2**(floor(log2(n))+1)
- n bytes of "payload data"
- 4 bits of "end region": 0101
  - This is to easily identify reversed codes, as they should always start with 1011

Total size of barcode: 18 + 8n + floor(log2(n)) + 1 bits, n being the number of bytes in the payload

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
   1. This could require informing the reader about the length of the barcode by adding a `length` block to the barcode spec **DONE**
2. Reduce false positives
   1. This could be done by adding a checksum to the barcode spec **DONE**
3. Read a code in a real picture
   1. Requires less naively reading the image data **done**
   2. Looking more for black and white instead of just the closest value
4. Handle rotated barcodes
   1. This should be done by scanning each image multiple times with different scan angles **DONE**
   2. **Must ensure that there are no backwards readings**. Potentially done by making the start and end strings different and non-symmetrical **DONE**
