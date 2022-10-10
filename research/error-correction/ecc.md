# Research - Error Correction Codes

The goal of this research project is to look at differnt types of error correctio, how they're useful, and easy of implementation.

The project will include written research notes as well as code.

## Goals

- Index of error correction codes, their properties, and their use cases
- Implementation of a few error correction codes
- Comparison of error correction codes and rankings of their usefulness for our vidual data format projects
  - Notable when it comes to what types of error correction make sense in 2D barcodes (also has to do with coloured codes, in the way that a colour being off can be more than 1 bit incorrect)

## Lessons

- Currently, Hamming codes aern't good enough to fix full bar errors on the codebar system, due to the fact that the scanner is miscounting bars rather than the hamming code implementation being incorrect
- If errors occur in the metadata, the hamming code can't fix it, so extra works needs to be put here to be sure meta data isnt lost
  - Is that why QR codes have many repeated copies of their meta data?
- Anecdotally, Hamming codes to help with acuracy on not-very broken scans with a webcam
- With a perfect file, it always corrects errors as expected
