# Research - Codebar

The goal of this research is to get used to the workings of a very basic standard encoder/ decoder system, very much inpsired by the original [codebar](https://en.wikipedia.org/wiki/Codabar).

## The Specification

(For this specification, 1 indicates a black bar, and 0 indicates a white bar)

The specification is very simple, and is as follows:

- All barcodes start with a start and end string of 101
- Data is encoded as raw binary of any type
- Bars must have a consistend width, within a tollerance of 20%

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
   1. Requires less naively reading the image data, and looking more for black and white instead of just the closeste value
4. Handle rotated barcodes
   1. This should be done by scanning each image multiple times with differnt scan angles
   2. **Must ensure that there are no backwards readings**. Potentially done by making the start and end strings different and non-symmetrical

## Technical TODOs:

- [ ] Make the reader able to deal with whitespace before and after the barcode
- [ ] Make the reader scan down an image instead of just assuming the barcode is at the top
- [ ] Add tollerance calculation to bar counts in regions (scanner)