# Research

This directory contains our research into data encoding.

`2d-decoding`: Rectangle detection
`2d-data`: 2D data processing
`codebar`: Decoding 1D barcodes
`error-correction`: Error correction

In order to run the code, you will need to install the requirements in
`../requirements.txt`.

Because of the way python packaging works, you will need to run the code from
this directory or higher. For example see `2d-data.py`.

To import code from directories using dashes or other illegal character, you
will want to use the following:

```python
import importlib
importlib.import_module("2d-decoding")
```

as opposed to

```python
import 2d-decoding
```
